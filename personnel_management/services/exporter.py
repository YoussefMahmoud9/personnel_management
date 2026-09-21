import io
from datetime import datetime

import frappe
from frappe import _
import pandas as pd


SHEET_MAP = {
    "details": "details",
    "taree5_tarqy_darga": "promotions",
    "h7alaagtma3ya": "family",
    "waheda": "unit_history",
    "lagnatbya": "medical_committees",
    "safr": "travel_history",
    "height": "measurements",
    "weight": "measurements",
    "k3obat": "punishments",
    "h7agz": "detentions",
    "h7abs": "imprisonments",
    "ma7kma": "military_courts",
}


def _clean(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    return value


def _personnel_list(military_numbers=None):
    if military_numbers:
        return [
            frappe.get_doc("Navy Personnel", number)
            for number in military_numbers
            if frappe.db.exists("Navy Personnel", number)
        ]

    names = frappe.get_all(
        "Navy Personnel",
        pluck="name",
        order_by="military_number asc",
    )

    return [
        frappe.get_doc("Navy Personnel", name)
        for name in names
    ]


def _details_rows(personnel):
    rows = []

    for person in personnel:
        rows.append({
            "name": person.full_name,
            "rakm3askry": person.military_number,
            "sela7": person.weapon,
            "taqreer1": person.report_1,
            "taqreer2": person.report_2,
            "taqreer3": person.report_3,
            "tab3ya": person.unit,
            "taree5_sarf_ratb_3aly": person.high_salary_date,
            "taree5_tareeqy_waited": person.promotion_promise_date,
            "address": person.address,
            "darga": person.rank,
            "fe2a": person.category,
            "wazefa": person.job,
            "servcice_year_number": person.service_year_number,
            "birthday": person.birth_date,
            "taree5_ttawo3": person.volunteer_date,
            "age": person.age,
            "halaa_egtma3ya": person.social_status,
            "image_path": person.image,
        })

    return rows


def _family_rows(personnel):
    rows = []

    for person in personnel:
        rows.append({
            "h7alaagtma3yaid": None,
            "h7alaagtma3ya": person.social_status,
            "numberofgirls": person.number_of_girls,
            "namesofgirls": person.names_of_girls,
            "numberofboys": person.number_of_boys,
            "namesofboys": person.names_of_boys,
            "rakm3askry": person.military_number,
        })

    return rows


def _promotion_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.promotions:
            rows.append({
                "taree5tarqydarga": row.promotion_date,
                "rakm3askry": person.military_number,
            })

    return rows


def _unit_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.unit_history:
            rows.append({
                "waheda": row.unit,
                "rakm3askry": person.military_number,
            })

    return rows


def _medical_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.medical_committees:
            rows.append({
                "no3ellegna": row.committee_type,
                "tash5ees": row.diagnosis,
                "qrar": row.decision,
                "rakm3askry": person.military_number,
                "dateoflagna": row.committee_date,
            })

    return rows


def _travel_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.travel_history:
            rows.append({
                "place": row.place,
                "dateoftravel": row.travel_date,
                "dateofreturn": row.return_date,
                "causeoftravel": row.cause,
                "rakm3askry": person.military_number,
            })

    return rows


def _measurement_rows(personnel):
    height_rows = []
    weight_rows = []

    for person in personnel:
        for row in person.measurements:
            height_rows.append({
                "height": row.height,
                "rakm3askry": person.military_number,
                "dateofheight": row.height_date,
            })

            weight_rows.append({
                "weight": row.weight,
                "rakm3askry": person.military_number,
                "dateofweight": row.weight_date,
            })

    return height_rows, weight_rows


def _punishment_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.punishments:
            rows.append({
                "typeof3koaba": row.type,
                "dateof3koba": row.date,
                "causeof3koaba": row.cause,
                "palceof3koaba": row.data_zhgc,
                "rakm3askry": person.military_number,
            })

    return rows


def _detention_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.detentions:
            rows.append({
                "rakm3askry": person.military_number,
                "placeof7agz": row.place,
                "dateof7agz": row.start_date,
                "timeof7agz": row.duration,
                "causeof7agz": row.cause,
            })

    return rows


def _imprisonment_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.imprisonments:
            rows.append({
                "rakm3askry": person.military_number,
                "placeof7abzs": row.place,
                "dateof7abs": row.start_date,
                "timeof7abs": row.duration,
                "causeof7abs": row.cause,
            })

    return rows


def _court_rows(personnel):
    rows = []

    for person in personnel:
        for row in person.military_courts:
            rows.append({
                "rakm3askry": person.military_number,
                "placeofma7abs": row.place,
                "dateofma7kma": row.date,
                "timeofma7abs": row.duration,
                "causeofma7abs": row.cause,
            })

    return rows


@frappe.whitelist()
def get_export_personnel_options():
    return frappe.get_all(
        "Navy Personnel",
        fields=["military_number", "full_name", "unit", "rank"],
        order_by="military_number asc, name asc",
        limit_page_length=0,
    )


@frappe.whitelist()
def export_personnel(military_numbers=None, committee_name=None):
    if isinstance(military_numbers, str):
        military_numbers = frappe.parse_json(military_numbers)

    if committee_name:
        committee_numbers = frappe.get_all(
            "Personnel Committee Record",
            filters={"committee": committee_name},
            pluck="military_number",
        )

        if military_numbers:
            military_numbers = list(
                set(military_numbers) & set(committee_numbers)
            )
        else:
            military_numbers = committee_numbers

    personnel = _personnel_list(military_numbers)

    if not personnel:
        frappe.throw(_("No personnel records found."))

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame(_details_rows(personnel)).to_excel(
            writer,
            sheet_name="details",
            index=False,
        )

        pd.DataFrame(_promotion_rows(personnel)).to_excel(
            writer,
            sheet_name="taree5_tarqy_darga",
            index=False,
        )

        pd.DataFrame(_family_rows(personnel)).to_excel(
            writer,
            sheet_name="h7alaagtma3ya",
            index=False,
        )

        pd.DataFrame(_unit_rows(personnel)).to_excel(
            writer,
            sheet_name="waheda",
            index=False,
        )

        pd.DataFrame(_medical_rows(personnel)).to_excel(
            writer,
            sheet_name="lagnatbya",
            index=False,
        )

        pd.DataFrame(_travel_rows(personnel)).to_excel(
            writer,
            sheet_name="safr",
            index=False,
        )

        height_rows, weight_rows = _measurement_rows(personnel)

        pd.DataFrame(height_rows).to_excel(
            writer,
            sheet_name="height",
            index=False,
        )

        pd.DataFrame(weight_rows).to_excel(
            writer,
            sheet_name="weight",
            index=False,
        )

        pd.DataFrame(_punishment_rows(personnel)).to_excel(
            writer,
            sheet_name="k3obat",
            index=False,
        )

        pd.DataFrame(_detention_rows(personnel)).to_excel(
            writer,
            sheet_name="h7agz",
            index=False,
        )

        pd.DataFrame(_imprisonment_rows(personnel)).to_excel(
            writer,
            sheet_name="h7abs",
            index=False,
        )

        pd.DataFrame(_court_rows(personnel)).to_excel(
            writer,
            sheet_name="ma7kma",
            index=False,
        )

    output.seek(0)

    frappe.local.response.filename = "personnel_export.xlsx"
    frappe.local.response.filecontent = output.read()
    frappe.local.response.type = "download"
