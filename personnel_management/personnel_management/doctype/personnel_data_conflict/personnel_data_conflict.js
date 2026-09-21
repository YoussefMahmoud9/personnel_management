// Copyright (c) 2026, Youssef and contributors
// For license information, please see license.txt

frappe.ui.form.on("Personnel Data Conflict", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Resolved") {
			return;
		}

		(frm.doc.conflict_options || []).forEach((option) => {
			frm.add_custom_button(
				__("Resolve with {0}", [option.option]),
				() => {
					frappe.prompt(
						[
							{
								fieldname: "resolution_notes",
								fieldtype: "Small Text",
								label: __("Resolution Notes"),
							},
						],
						(values) => {
							frappe.call({
								method: "personnel_management.services.conflict_resolution.resolve_conflict",
								args: {
									conflict_name: frm.doc.name,
									selected_option: option.option,
									resolution_notes: values.resolution_notes,
								},
								freeze: true,
								freeze_message: __("Resolving conflict..."),
								callback: () => {
									frappe.show_alert({
										message: __("Conflict resolved."),
										indicator: "green",
									});
									frm.reload_doc();
								},
							});
						},
						__("Resolve Conflict"),
						__("Resolve"),
					);
				},
				__("Resolve"),
			);
		});
	},
});
