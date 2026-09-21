import frappe


REFERENCE_DOCTYPES = {
	"unit": ("Navy Unit", "unit_name"),
	"job": ("Navy Job", "job_name"),
	"rank": ("Navy Rank", "rank_name"),
	"weapon": ("Navy Weapon", "weapon_name"),
}


def execute():
	for source_field, (doctype, title_field) in REFERENCE_DOCTYPES.items():
		for value in get_existing_values(source_field):
			if not frappe.db.exists(doctype, value):
				frappe.get_doc(
					{
						"doctype": doctype,
						title_field: value,
					}
				).insert(ignore_permissions=True)


def get_existing_values(source_field):
	values = set()

	for doctype, fieldname in (
		("Navy Personnel", source_field),
		("Personnel Committee Record", source_field),
	):
		for value in frappe.get_all(
			doctype,
			filters=[[fieldname, "is", "set"]],
			pluck=fieldname,
		):
			value = str(value).strip()

			if value:
				values.add(value)

	return sorted(values)
