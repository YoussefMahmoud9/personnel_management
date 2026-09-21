import frappe
from frappe import _


@frappe.whitelist()
def switch_language(language):
	if frappe.session.user == "Guest":
		frappe.throw(_("Please log in before changing language."))

	if language not in ("ar", "en"):
		frappe.throw(_("Unsupported language."))

	frappe.db.set_value(
		"User",
		frappe.session.user,
		"language",
		language,
		update_modified=False,
	)
	frappe.clear_cache(user=frappe.session.user)

	return language
