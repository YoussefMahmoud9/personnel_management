import frappe
from frappe import _

from personnel_management.services.deduplication import same_identity


def values_match(first, second):
    if first in (None, "") and second in (None, ""):
        return True

    return str(first) == str(second)


@frappe.whitelist()
def resolve_conflict(conflict_name, selected_option, resolution_notes=None):
    conflict = frappe.get_doc("Personnel Data Conflict", conflict_name)

    if conflict.status == "Resolved":
        frappe.throw(_("This conflict is already resolved."))

    option = next(
        (row for row in conflict.conflict_options if row.option == selected_option),
        None,
    )

    if not option:
        frappe.throw(_("Selected option was not found."))

    selected_value = frappe.parse_json(option.value)

    personnel = frappe.get_doc("Navy Personnel", conflict.personnel)
    child_table = conflict.field_or_record

    matching_rows = []

    for row in personnel.get(child_table):
        matches = True

        for field, value in selected_value.items():
            if field.startswith("_"):
                continue

            if field == "military_number":
                continue

            if not values_match(row.get(field), value):
                matches = False
                break

        if matches:
            matching_rows.append(row)

    if not matching_rows:
        matching_rows = [
            row
            for row in personnel.get(child_table)
            if same_identity(child_table, row, selected_value)
        ]

    if not matching_rows:
        frappe.throw(_("The conflicting history record could not be found."))

    target = matching_rows[0]

    for field, value in selected_value.items():
        if field.startswith("_"):
            continue

        if field == "military_number":
            continue

        target.set(field, value)

    for row in conflict.conflict_options:
        row.selected = 1 if row.name == option.name else 0

    conflict.selected_option = selected_option
    conflict.status = "Resolved"
    conflict.resolution_notes = resolution_notes
    conflict.resolved_by = frappe.session.user
    conflict.resolved_on = frappe.utils.now_datetime()

    personnel.save(ignore_permissions=True)
    conflict.save(ignore_permissions=True)

    frappe.db.commit()

    return conflict.name
