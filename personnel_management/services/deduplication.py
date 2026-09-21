"""
Deterministic deduplication rules for personnel history records.
"""

import frappe


IDENTITY_FIELDS_BY_RECORD = {
    "detentions": ("start_date", "place"),
    "imprisonments": ("start_date", "place"),
    "punishments": ("date", "data_zhgc", "type"),
    "medical_committees": ("committee_date", "committee_type"),
    "promotions": ("promotion_date",),
    "travel_history": ("travel_date", "return_date", "place"),
}


def identity_fields_for_record(field_or_record, record):
    if field_or_record == "measurements":
        if record.get("height_date"):
            return ("height_date",)

        if record.get("weight_date"):
            return ("weight_date",)

        return ()

    return IDENTITY_FIELDS_BY_RECORD.get(field_or_record, ())


def same_identity(field_or_record, first, second):
    identity_fields = identity_fields_for_record(field_or_record, first)

    if not identity_fields:
        return False

    if any(not first.get(field) or not second.get(field) for field in identity_fields):
        return False

    return all(
        str(first.get(field)) == str(second.get(field))
        for field in identity_fields
    )


def parse_conflict_value(value):
    if isinstance(value, dict):
        return value

    return frappe.parse_json(value)


def existing_equivalent_conflict(personnel, field_or_record, *records):
    conflicts = frappe.get_all(
        "Personnel Data Conflict",
        filters={
            "personnel": personnel,
            "field_or_record": field_or_record,
        },
        pluck="name",
    )

    for conflict_name in conflicts:
        conflict = frappe.get_doc("Personnel Data Conflict", conflict_name)

        for option in conflict.conflict_options:
            option_value = parse_conflict_value(option.value)

            for record in records:
                if same_identity(field_or_record, option_value, record):
                    return conflict

    return None


def compare_records(existing, incoming, identity_fields, conflict_fields):
    """
    Compare two historical records.

    Returns:
        "duplicate" -> same identity and same conflict fields
        "conflict"  -> same identity but conflicting fields
        "distinct"  -> different event
    """

    if any(
        not existing.get(field) or not incoming.get(field)
        for field in identity_fields
    ):
        return "distinct"

    same_identity = all(
        existing.get(field) == incoming.get(field)
        for field in identity_fields
    )

    if not same_identity:
        return "distinct"

    same_conflict_fields = all(
        existing.get(field) == incoming.get(field)
        for field in conflict_fields
    )

    if same_conflict_fields:
        return "duplicate"

    return "conflict"


def compare_detentions(existing, incoming):
    """
    Detention:
    Same date + place + cause = duplicate.
    Same date + place + different cause = conflict.
    Otherwise = distinct.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("start_date", "place"),
        conflict_fields=("cause",),
    )


def compare_imprisonments(existing, incoming):
    """
    Imprisonment uses the same rules as detention.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("start_date", "place"),
        conflict_fields=("cause",),
    )


def compare_punishments(existing, incoming):
    """
    Punishment:
    Same date + place + type + cause = duplicate.
    Same date + place + type + different cause = conflict.
    Otherwise = distinct.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("date", "data_zhgc", "type"),
        conflict_fields=("cause",),
    )


def compare_medical_committees(existing, incoming):
    """
    Medical Committee:
    Same date + type + diagnosis + decision = duplicate.
    Same date + type with different diagnosis/decision = conflict.
    Otherwise = distinct.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("committee_date", "committee_type"),
        conflict_fields=("diagnosis", "decision"),
    )


def compare_promotions(existing, incoming):
    """
    Promotion:
    Same promotion date = duplicate.
    Different promotion date = distinct.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("promotion_date",),
        conflict_fields=(),
    )

def compare_travel(existing, incoming):
    """
    Travel:
    Same travel date + return date + place + cause = duplicate.
    Same travel date + return date + place + different cause = conflict.
    Otherwise = distinct.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("travel_date", "return_date", "place"),
        conflict_fields=("cause",),
    )


def compare_height(existing, incoming):
    """
    Height:
    Same height date + same height = duplicate.
    Same height date + different height = conflict.
    Different date = distinct.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("height_date",),
        conflict_fields=("height",),
    )


def compare_weight(existing, incoming):
    """
    Weight:
    Same weight date + same weight = duplicate.
    Same weight date + different weight = conflict.
    Different date = distinct.
    """

    return compare_records(
        existing,
        incoming,
        identity_fields=("weight_date",),
        conflict_fields=("weight",),
    )    


def compare_unit_history(existing, incoming):
    """
    Unit History:
    Same non-empty unit for the same person = duplicate.
    Different unit = distinct.
    """

    if not existing.get("unit") or not incoming.get("unit"):
        return "distinct"

    if str(existing.get("unit")) == str(incoming.get("unit")):
        return "duplicate"

    return "distinct"


def compare_military_courts(existing, incoming):
    """
    Military Court:
    Fully identical saved court rows are duplicates.
    Any difference is distinct because no conflict rule is defined.
    """

    fields = ("place", "date", "cause", "duration")

    if not any(existing.get(field) or incoming.get(field) for field in fields):
        return "distinct"

    if all(str(existing.get(field) or "") == str(incoming.get(field) or "") for field in fields):
        return "duplicate"

    return "distinct"

def process_history_record(existing_records, incoming_record, compare_function):
    """
    Decide what to do with an incoming history record.

    Returns:
        "duplicate" -> existing record already represents the same event
        "conflict"  -> existing record may be the same event but has conflicting data
        "new"       -> no matching event found
    """

    for existing_record in existing_records:
        result = compare_function(existing_record, incoming_record)

        if result == "duplicate":
            return {
                "action": "duplicate",
                "existing": existing_record,
                "incoming": incoming_record,
            }

        if result == "conflict":
            return {
                "action": "conflict",
                "existing": existing_record,
                "incoming": incoming_record,
            }

    return {
        "action": "new",
        "existing": None,
        "incoming": incoming_record,
    }


def format_record_value(record):
    """
    Store the actual record without internal metadata.
    """

    clean_record = {
        key: value
        for key, value in record.items()
        if not key.startswith("_")
    }

    return frappe.as_json(clean_record)

def create_conflict(
    personnel,
    military_number,
    conflict_type,
    field_or_record,
    description,
    existing_value,
    existing_committee,
    incoming_value,
    incoming_committee,
):
    """
    Create an unresolved Personnel Data Conflict.
    """

    existing_record = parse_conflict_value(existing_value)
    incoming_record = parse_conflict_value(incoming_value)

    existing_conflict = existing_equivalent_conflict(
        personnel,
        field_or_record,
        existing_record,
        incoming_record,
    )

    if existing_conflict:
        return existing_conflict

    conflict = frappe.new_doc("Personnel Data Conflict")

    conflict.personnel = personnel
    conflict.military_number = military_number
    conflict.conflict_type = conflict_type
    conflict.field_or_record = field_or_record
    conflict.status = "Unresolved"
    conflict.description = description

    conflict.append("conflict_options", {
        "option": "Option 1",
        "value": existing_value,
        "source_committee": existing_committee,
        "selected": 0,
    })

    conflict.append("conflict_options", {
        "option": "Option 2",
        "value": incoming_value,
        "source_committee": incoming_committee,
        "selected": 0,
    })

    conflict.insert(ignore_permissions=True)

    return conflict


def process_and_handle_conflict(
    existing_records,
    incoming_record,
    compare_function,
    personnel,
    military_number,
    conflict_type,
    field_or_record,
    description,
    existing_committee,
    incoming_committee,
):
    """
    Process an incoming history record.

    Returns:
        duplicate -> existing record already exists
        conflict  -> unresolved conflict created
        new       -> new record should be added
    """

    for existing_record in existing_records:
        result = compare_function(existing_record, incoming_record)

        if result == "duplicate":
            return {
                "action": "duplicate",
                "record": existing_record,
            }

        if result == "conflict":
            actual_existing_committee = (
                existing_record.get("_source_committee")
                or existing_committee
            )

            conflict = create_conflict(
                personnel=personnel,
                military_number=military_number,
                conflict_type=conflict_type,
                field_or_record=field_or_record,
                description=description,
                existing_value=format_record_value(existing_record),
                existing_committee=actual_existing_committee,
                incoming_value=format_record_value(incoming_record),
                incoming_committee=incoming_committee,
            )

            return {
                "action": "conflict",
                "conflict": conflict.name,
            }

    return {
        "action": "new",
        "record": incoming_record,
    }
