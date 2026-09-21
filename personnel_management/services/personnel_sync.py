import frappe


def sync_committee_records(doc, method=None):
    field_map = {
        "full_name": "committee_name_value",
        "rank": "rank",
        "category": "category",
        "age": "age",
        "weapon": "weapon",
        "job": "job",
        "unit": "unit",
        "service_year_number": "service_year_number",
        "report_1": "report_1",
        "report_2": "report_2",
        "report_3": "report_3",
    }

    for committee_record in doc.get("committee_records"):
        values = {
            committee_field: doc.get(personnel_field)
            for personnel_field, committee_field in field_map.items()
        }

        frappe.db.set_value(
            "Personnel Committee Record",
            committee_record.name,
            values,
            update_modified=False,
        )