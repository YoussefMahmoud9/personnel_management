import re
from pathlib import Path

import pandas as pd
import frappe
from frappe import _
from frappe.utils.file_manager import get_file_path

from personnel_management.services import deduplication


# ============================================================
# Basic normalization helpers
# ============================================================

ARABIC_DIGITS = str.maketrans(
    "٠١٢٣٤٥٦٧٨٩",
    "0123456789",
)


def clean_text(value):
    """Return a clean string, or None for empty values."""
    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value or value == ".":
        return None

    return value


def clean_military_number(value):
    """
    Normalize military numbers without changing their actual digits.

    Examples:
        201813490158.0  -> 201813490158
        \\201813490158   -> 201813490158
        Arabic digits    -> ASCII digits
    """
    value = clean_text(value)

    if value is None:
        return None

    value = value.translate(ARABIC_DIGITS)
    value = value.lstrip("\\").strip()

    if value.endswith(".0"):
        value = value[:-2]

    return value


def clean_number(value):
    """Convert numeric-looking values to float, otherwise None."""
    value = clean_text(value)

    if value is None:
        return None

    value = value.translate(ARABIC_DIGITS)

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def clean_duration(value):
    """
    Convert duration values such as:
        30
        ٧ يوم
        15 يوم
    into an integer number of days.
    """
    value = clean_text(value)

    if value is None:
        return None

    value = value.translate(ARABIC_DIGITS)

    match = re.search(r"-?\d+", value)

    if not match:
        return None

    duration = int(match.group())

    if duration < 0 or duration > 3650:
        return None

    return duration


def clean_date(value):
    """
    Normalize the mixed date formats found in the source workbook.
    """
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            return None
        return value.date()

    value = str(value).strip()

    if not value or value == ".":
        return None

    value = value.translate(ARABIC_DIGITS)

    # Known invalid placeholder.
    if value.startswith("1/1/1111"):
        return None

    formats = [
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M:%S",
    ]

    for date_format in formats:
        try:
            return pd.to_datetime(
                value,
                format=date_format,
                errors="raise",
            ).date()
        except (ValueError, TypeError):
            pass

    # Final fallback for other Excel/date representations.
    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return None

    return parsed.date()


# ============================================================
# Workbook loading
# ============================================================

def load_workbook(excel_file=None):
    """Load the authoritative Excel workbook."""
    if not excel_file:
        frappe.throw(
            _("An Excel file must be attached to the Personnel Committee before importing.")
        )

    excel_path = Path(get_file_path(excel_file))

    if not excel_path.exists():
        frappe.throw(_("Excel file not found: {0}").format(excel_path))

    return pd.read_excel(
        excel_path,
        sheet_name=None,
    )

# ============================================================
# Workbook validation
# ============================================================

EXPECTED_SHEETS = {
    "details",
    "taree5_tarqy_darga",
    "h7alaagtma3ya",
    "waheda",
    "lagnatbya",
    "safr",
    "height",
    "weight",
    "k3obat",
    "h7agz",
    "h7abs",
    "ma7kma",
}


def validate_workbook(workbook):
    """
    Verify that the source workbook contains all required sheets.
    """
    actual_sheets = set(workbook.keys())

    missing = EXPECTED_SHEETS - actual_sheets

    if missing:
        raise ValueError(
            _("Missing required sheets: {0}").format(sorted(missing))
        )

    return True


# ============================================================
# Sheet column validation
# ============================================================

EXPECTED_COLUMNS = {
    "details": {
        "name",
        "rakm3askry",
        "sela7",
        "taqreer1",
        "taqreer2",
        "taqreer3",
        "tab3ya",
        "taree5_sarf_ratb_3aly",
        "taree5_tareeqy_waited",
        "address",
        "darga",
        "fe2a",
        "wazefa",
        "servcice_year_number",
        "birthday",
        "taree5_ttawo3",
        "age",
        "halaa_egtma3ya",
        "image_path",
    },
    "taree5_tarqy_darga": {
        "taree5tarqydarga",
        "rakm3askry",
    },
    "h7alaagtma3ya": {
        "h7alaagtma3yaid",
        "h7alaagtma3ya",
        "numberofgirls",
        "namesofgirls",
        "numberofboys",
        "namesofboys",
        "rakm3askry",
    },
    "waheda": {
        "waheda",
        "rakm3askry",
    },
    "lagnatbya": {
        "no3ellegna",
        "tash5ees",
        "qrar",
        "rakm3askry",
        "dateoflagna",
    },
    "safr": {
        "place",
        "dateoftravel",
        "dateofreturn",
        "causeoftravel",
        "rakm3askry",
    },
    "height": {
        "height",
        "rakm3askry",
        "dateofheight",
    },
    "weight": {
        "weight",
        "rakm3askry",
        "dateofweight",
    },
    "k3obat": {
        "typeof3koaba",
        "dateof3koba",
        "causeof3koba",
        "palceof3koba",
        "rakm3askry",
    },
    "h7agz": {
        "rakm3askry",
        "placeof7agz",
        "dateof7agz",
        "timeof7agz",
        "causeof7agz",
    },
    "h7abs": {
        "rakm3askry",
        "placeof7abzs",
        "dateof7abs",
        "timeof7abs",
        "causeof7abs",
    },
    "ma7kma": {
        "rakm3askry",
        "placeofma7kma",
        "dateofma7kma",
        "timeofma7kma",
        "causeofma7kma",
    },
}


def validate_columns(workbook):
    """
    Verify that every required source column exists.
    Extra columns are allowed.
    """
    errors = []

    for sheet_name, required_columns in EXPECTED_COLUMNS.items():
        actual_columns = set(workbook[sheet_name].columns)

        missing = required_columns - actual_columns

        if missing:
            errors.append(
                f"{sheet_name}: missing {sorted(missing)}"
            )

    if errors:
        raise ValueError(
            _("Source workbook column validation failed:")
            + "\n"
            + "\n".join(errors)
        )

    return True


def get_committee(committee_name):
    if not committee_name:
        frappe.throw(_("Personnel Committee is required."))

    return frappe.get_doc(
        "Personnel Committee",
        {"committee_name": committee_name},
    )


# ============================================================
# Navy Personnel mapping
# ============================================================

def map_personnel_row(row):
    """
    Convert one `details` Excel row into a Navy Personnel
    document data dictionary.

    This function does not create or save anything.
    """

    military_number = clean_military_number(row.get("rakm3askry"))

    if not military_number:
        return None

    return {
        "doctype": "Navy Personnel",

        "military_number": military_number,
        "full_name": clean_text(row.get("name")),
        "birth_date": clean_date(row.get("birthday")),
        "age": clean_number(row.get("age")),
        "address": clean_text(row.get("address")),
        "image": clean_text(row.get("image_path")),

        "report_1": clean_text(row.get("taqreer1")),
        "report_2": clean_text(row.get("taqreer2")),
        "report_3": clean_text(row.get("taqreer3")),

        "weapon": clean_text(row.get("sela7")),
        "unit": clean_text(row.get("tab3ya")),
        "rank": clean_text(row.get("darga")),
        "category": clean_text(row.get("fe2a")),
        "job": clean_text(row.get("wazefa")),

        "service_year_number": clean_number(
            row.get("servcice_year_number")
        ),

        "high_salary_date": clean_date(
            row.get("taree5_sarf_ratb_3aly")
        ),

        "promotion_promise_date": clean_date(
            row.get("taree5_tareeqy_waited")
        ),

        "volunteer_date": clean_date(
            row.get("taree5_ttawo3")
        ),

        "social_status": clean_text(
            row.get("halaa_egtma3ya")
        ),
    }


# ============================================================
# Personnel reference helpers
# ============================================================

def build_personnel_index(details_df):
    """
    Build a lookup of valid military numbers from the
    authoritative `details` sheet.

    Returns:
        {
            "military_number": military_number
        }
    """
    index = {}

    for _, row in details_df.iterrows():
        military_number = clean_military_number(
            row.get("rakm3askry")
        )

        if military_number:
            index[military_number] = military_number

    return index


def resolve_personnel(military_number, personnel_index):
    """
    Resolve a history row against the authoritative personnel
    master.

    Returns the military number if it exists, otherwise None.

    No fuzzy matching is performed.
    """
    military_number = clean_military_number(military_number)

    if not military_number:
        return None

    return personnel_index.get(military_number)


# ============================================================
# History mapping
# ============================================================

def map_promotion_row(row, personnel_index):
    """
    Map one promotion history row.

    Returns:
        {
            "military_number": "...",
            "promotion_date": date
        }

    Returns None when the military number is missing or
    does not exist in the authoritative details sheet.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    return {
        "military_number": military_number,
        "promotion_date": clean_date(
            row.get("taree5tarqydarga")
        ),
    }





def map_family_row(row, personnel_index):
    """
    Map one family/social-status row.

    Family information is stored directly on Navy Personnel.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    return {
        "military_number": military_number,
        "social_status": clean_text(
            row.get("h7alaagtma3ya")
        ),
        "number_of_girls": clean_number(
            row.get("numberofgirls")
        ),
        "names_of_girls": clean_text(
            row.get("namesofgirls")
        ),
        "number_of_boys": clean_number(
            row.get("numberofboys")
        ),
        "names_of_boys": clean_text(
            row.get("namesofboys")
        ),
    }



def map_unit_history_row(row, personnel_index):
    """
    Map one unit-history row.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    unit = clean_text(row.get("waheda"))

    if not unit:
        return None

    return {
        "military_number": military_number,
        "unit": unit,
    }


def map_medical_committee_row(row, personnel_index):
    """
    Map one medical committee history row.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    return {
        "military_number": military_number,
        "committee_type": clean_text(
            row.get("no3ellegna")
        ),
        "diagnosis": clean_text(
            row.get("tash5ees")
        ),
        "decision": clean_text(
            row.get("qrar")
        ),
        "committee_date": clean_date(
            row.get("dateoflagna")
        ),
    }


def map_travel_row(row, personnel_index):
    """
    Map one travel history row.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    return {
        "military_number": military_number,
        "place": clean_text(
            row.get("place")
        ),
        "travel_date": clean_date(
            row.get("dateoftravel")
        ),
        "return_date": clean_date(
            row.get("dateofreturn")
        ),
        "cause": clean_text(
            row.get("causeoftravel")
        ),
    }


def map_height_row(row, personnel_index):
    """
    Map one height measurement row.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    height = clean_number(row.get("height"))

    if height is None:
        return None

    return {
        "military_number": military_number,
        "height": height,
        "height_date": clean_date(
            row.get("dateofheight")
        ),
    }


def map_weight_row(row, personnel_index):
    """
    Map one weight measurement row.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    weight = clean_number(row.get("weight"))

    if weight is None:
        return None

    return {
        "military_number": military_number,
        "weight": weight,
        "weight_date": clean_date(
            row.get("dateofweight")
        ),
    }


def map_punishment_row(row, personnel_index):
    """
    Map one punishment row.
    """

    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )

    if not military_number:
        return None

    return {
        "military_number": military_number,
        "type": clean_text(row.get("typeof3koaba")),
        "date": clean_date(row.get("dateof3koba")),
        "cause": clean_text(row.get("causeof3koaba")),
        "data_zhgc": clean_text(row.get("palceof3koaba")),
    }


def map_detention_row(row, personnel_index):
    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )
    if not military_number:
        return None

    return {
        "military_number": military_number,
        "place": clean_text(row.get("placeof7agz")),
        "start_date": clean_date(row.get("dateof7agz")),
        "cause": clean_text(row.get("causeof7agz")),
        "duration": clean_duration(row.get("timeof7agz")),
    }


def map_imprisonment_row(row, personnel_index):
    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )
    if not military_number:
        return None

    return {
        "military_number": military_number,
        "place": clean_text(row.get("placeof7abzs")),
        "start_date": clean_date(row.get("dateof7abs")),
        "cause": clean_text(row.get("causeof7abs")),
        "duration": clean_duration(row.get("timeof7abs")),
    }

def map_military_court_row(row, personnel_index):
    military_number = resolve_personnel(
        row.get("rakm3askry"),
        personnel_index,
    )
    if not military_number:
        return None

    return {
    "military_number": military_number,
    "place": clean_text(row.get("placeofma7abs")),
    "date": clean_date(row.get("dateofma7kma")),
    "cause": clean_text(row.get("causeofma7abs")),
    "duration": clean_duration(row.get("timeofma7abs")),
    }


def get_mapping_summary(workbook):
    """
    Validate row-level mapping without creating or updating records.
    """
    validate_workbook(workbook)
    validate_columns(workbook)

    personnel_index = build_personnel_index(
        workbook["details"]
    )

    details_matched = 0

    for _, row in workbook["details"].iterrows():
        if map_personnel_row(row):
            details_matched += 1

    results = {
        "details": {
            "source_rows": len(workbook["details"]),
            "matched": details_matched,
            "unmatched": len(workbook["details"]) - details_matched,
        },
    }

    mappers = {
        "promotions": (
            "taree5_tarqy_darga",
            map_promotion_row,
        ),
        "family": (
            "h7alaagtma3ya",
            map_family_row,
        ),
        "unit_history": (
            "waheda",
            map_unit_history_row,
        ),
        "medical_committees": (
            "lagnatbya",
            map_medical_committee_row,
        ),
        "travel": (
            "safr",
            map_travel_row,
        ),
        "height": (
            "height",
            map_height_row,
        ),
        "weight": (
            "weight",
            map_weight_row,
        ),
        "punishments": (
            "k3obat",
            map_punishment_row,
        ),
        "detentions": (
            "h7agz",
            map_detention_row,
        ),
        "imprisonments": (
            "h7abs",
            map_imprisonment_row,
        ),
        "military_courts": (
            "ma7kma",
            map_military_court_row,
        ),
    }

    for name, (sheet_name, mapper) in mappers.items():
        matched = []

        for _, row in workbook[sheet_name].iterrows():
            mapped = mapper(row, personnel_index)
            if mapped:
                matched.append(mapped)

        results[name] = {
            "source_rows": len(workbook[sheet_name]),
            "matched": len(matched),
            "unmatched": len(workbook[sheet_name]) - len(matched),
        }

    return results


@frappe.whitelist()
def validate_committee_workbook(committee_name):
    """
    Validate a committee's attached workbook without modifying data.
    """
    committee = get_committee(committee_name)
    workbook = load_workbook(committee.excel_file)
    summary = get_mapping_summary(workbook)

    warnings = []

    for name, result in summary.items():
        if result["unmatched"]:
            warnings.append(
                f"{name}: {result['unmatched']} row(s) could not be mapped."
            )

    return {
        "valid": True,
        "committee": committee.name,
        "excel_file": committee.excel_file,
        "summary": summary,
        "warnings": warnings,
    }


def validate_all_mappings(committee_name):
    return validate_committee_workbook(committee_name)

def add_record_source(doc, record_type, record_name, committee_name):
    """
    Add committee provenance for a historical record.
    Avoid duplicate source entries.
    """

    for source in doc.record_sources:
        if (
            source.record_type == record_type
            and source.record_name == record_name
            and source.committee == committee_name
        ):
            return

    doc.append(
        "record_sources",
        {
            "record_type": record_type,
            "record_name": record_name,
            "committee": committee_name,
            "record_display": f"{record_type}: {record_name}",
        },
    )


def find_child_row_by_idx(doc, child_field, idx):
    for child_row in doc.get(child_field):
        if child_row.idx == idx:
            return child_row

    return None


def upsert_committee_record(doc, committee_name):
    """
    Create or update the committee snapshot from saved master values.
    """

    committee_record = None

    for row in doc.get("committee_records"):
        if row.personnel == doc.name and row.committee == committee_name:
            committee_record = row
            break

    if committee_record is None:
        committee_record = doc.append(
            "committee_records",
            {
                "personnel": doc.name,
                "committee": committee_name,
            },
        )

    committee_record.military_number = doc.military_number
    committee_record.committee_name_value = doc.full_name
    committee_record.rank = doc.rank
    committee_record.category = doc.category
    committee_record.age = doc.age
    committee_record.service_year_number = doc.service_year_number
    committee_record.weapon = doc.weapon
    committee_record.job = doc.job
    committee_record.unit = doc.unit
    committee_record.report_1 = doc.report_1
    committee_record.report_2 = doc.report_2
    committee_record.report_3 = doc.report_3

@frappe.whitelist()
def import_personnel_data(committee_name):
    committee = get_committee(committee_name)

    workbook = load_workbook(committee.excel_file)
    validate_workbook(workbook)
    validate_columns(workbook)

    personnel_index = build_personnel_index(
        workbook["details"]
    )

    summary = {
        "personnel_created": 0,
        "personnel_updated": 0,
        "history_added": 0,
        "duplicates": 0,
        "conflicts": 0,
        "unmatched": {},
    }

    # ========================================================
    # 1. Master personnel
    # ========================================================

    for _, row in workbook["details"].iterrows():
        mapped = map_personnel_row(row)

        if not mapped:
            continue

        military_number = mapped["military_number"]

        if frappe.db.exists("Navy Personnel", military_number):
            doc = frappe.get_doc(
                "Navy Personnel",
                military_number,
            )
            summary["personnel_updated"] += 1
        else:
            doc = frappe.new_doc("Navy Personnel")
            doc.name = military_number
            summary["personnel_created"] += 1

        for field, value in mapped.items():
            if field != "doctype":
                doc.set(field, value)

        doc.save(ignore_permissions=True)
        doc.reload()
        upsert_committee_record(
            doc,
            committee.name,
        )
        doc.save(ignore_permissions=True)

    # ========================================================
    # 2. Family / social information
    # ========================================================

    unmatched = 0

    for _, row in workbook["h7alaagtma3ya"].iterrows():
        mapped = map_family_row(
            row,
            personnel_index,
        )

        if not mapped:
            unmatched += 1
            continue

        military_number = mapped.pop(
            "military_number"
        )

        doc = frappe.get_doc(
            "Navy Personnel",
            military_number,
        )

        doc.social_status = mapped["social_status"]
        doc.number_of_girls = int(
            mapped["number_of_girls"] or 0
        )
        doc.names_of_girls = mapped["names_of_girls"]
        doc.number_of_boys = int(
            mapped["number_of_boys"] or 0
        )
        doc.names_of_boys = mapped["names_of_boys"]

        doc.save(ignore_permissions=True)

        summary["history_added"] += 1

    summary["unmatched"]["family"] = unmatched

    # ========================================================
    # 3. History tables
    # ========================================================

    history_mappers = {
        "promotions": (
            "taree5_tarqy_darga",
            map_promotion_row,
            "promotions",
            deduplication.compare_promotions,
        ),
        "medical_committees": (
            "lagnatbya",
            map_medical_committee_row,
            "medical_committees",
            deduplication.compare_medical_committees,
        ),
        "punishments": (
            "k3obat",
            map_punishment_row,
            "punishments",
            deduplication.compare_punishments,
        ),
        "detentions": (
            "h7agz",
            map_detention_row,
            "detentions",
            deduplication.compare_detentions,
        ),
        "imprisonments": (
            "h7abs",
            map_imprisonment_row,
            "imprisonments",
            deduplication.compare_imprisonments,
        ),
        "unit_history": (
            "waheda",
            map_unit_history_row,
            "unit_history",
            deduplication.compare_unit_history,
        ),
        "travel": (
            "safr",
            map_travel_row,
            "travel_history",
            deduplication.compare_travel,
        ),
        "height": (
            "height",
            map_height_row,
            "measurements",
            deduplication.compare_height,
        ),
        "weight": (
            "weight",
            map_weight_row,
            "measurements",
            deduplication.compare_weight,
        ),
        "military_courts": (
            "ma7kma",
            map_military_court_row,
            "military_courts",
            deduplication.compare_military_courts,
        ),
    }

    for name, (
        sheet_name,
        mapper,
        child_field,
        compare_function,
    ) in history_mappers.items():

        unmatched = 0

        for _, row in workbook[sheet_name].iterrows():

            mapped = mapper(
                row,
                personnel_index,
            )

            if not mapped:
                unmatched += 1
                continue

            military_number = mapped.pop(
                "military_number"
            )

            doc = frappe.get_doc(
                "Navy Personnel",
                military_number,
            )

            # ------------------------------------------------
            # History types without finalized deduplication
            # rules: preserve the record normally.
            # ------------------------------------------------

            if compare_function is None:

                child = doc.append(
                    child_field
                )

                for field, value in mapped.items():
                    child.set(
                        field,
                        value,
                    )

                child_idx = child.idx

                doc.save(
                    ignore_permissions=True
                )

                doc.reload()
                saved_child = find_child_row_by_idx(
                    doc,
                    child_field,
                    child_idx,
                )

                if saved_child is None:
                    frappe.throw(
                        _("Saved history record could not be found.")
                    )

                add_record_source(
                    doc,
                    saved_child.doctype,
                    saved_child.name,
                    committee.name,
                )

                doc.save(
                    ignore_permissions=True
                )

                summary["history_added"] += 1
                continue

            # ------------------------------------------------
            # History types with finalized deduplication rules
            # ------------------------------------------------

            existing_records = []

            for existing in doc.get(child_field):

                record = {
                    field: existing.get(field)
                    for field in mapped
                }

                record["_source_committee"] = None

                for source in doc.record_sources:
                    if (
                        source.record_type == existing.doctype
                        and source.record_name == existing.name
                    ):
                        record["_source_committee"] = (
                            source.committee
                        )
                        break

                existing_records.append(
                    record
                )

            # ------------------------------------------------
            # Compare incoming record against existing records
            # ------------------------------------------------

            result = (
                deduplication.process_and_handle_conflict(
                    existing_records=existing_records,
                    incoming_record=mapped,
                    compare_function=compare_function,
                    personnel=military_number,
                    military_number=military_number,
                    conflict_type=name,
                    field_or_record=child_field,
                    description=(
                        f"Conflict detected during "
                        f"{name} import."
                    ),
                    existing_committee=committee.name,
                    incoming_committee=committee.name,
                )
            )

            # ------------------------------------------------
            # Duplicate
            # ------------------------------------------------

            if result["action"] == "duplicate":

                existing_record = result["record"]

                existing_child = None

                for child_row in doc.get(child_field):

                    if all(
                        child_row.get(field)
                        == mapped.get(field)
                        for field in mapped
                    ):
                        existing_child = child_row
                        break

                if existing_child is None:
                    frappe.throw(
                        _(
                            "Existing duplicate history record could not be found."
                        )
                    )

                add_record_source(
                    doc,
                    existing_child.doctype,
                    existing_child.name,
                    committee.name,
                )

                doc.save(
                    ignore_permissions=True
                )

                summary["duplicates"] += 1
                continue

            # ------------------------------------------------
            # Conflict
            # ------------------------------------------------

            if result["action"] == "conflict":

                summary["conflicts"] += 1
                continue

            # ------------------------------------------------
            # New history record
            # ------------------------------------------------

            child = doc.append(
                child_field
            )

            for field, value in mapped.items():
                child.set(
                    field,
                    value,
                )

            child_idx = child.idx

            doc.save(
                ignore_permissions=True
            )

            doc.reload()
            saved_child = find_child_row_by_idx(
                doc,
                child_field,
                child_idx,
            )

            if saved_child is None:
                frappe.throw(
                    _("Saved history record could not be found.")
                )

            add_record_source(
                doc,
                saved_child.doctype,
                saved_child.name,
                committee.name,
            )

            doc.save(
                ignore_permissions=True
            )

            summary["history_added"] += 1

        summary["unmatched"][name] = unmatched

    frappe.db.commit()

    return summary
