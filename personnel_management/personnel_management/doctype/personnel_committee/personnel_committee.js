// Copyright (c) 2026, Youssef and contributors
// For license information, please see license.txt

frappe.ui.form.on("Personnel Committee", {
	onload_post_render(frm) {
		frm.trigger("add_workbook_buttons");
	},

	refresh(frm) {
		frm.trigger("add_workbook_buttons");
		frm.trigger("add_view_personnel_button");
	},

	add_view_personnel_button(frm) {
		if (!frm.doc.name || frm.doc.__islocal) {
			return;
		}

		frm.remove_custom_button(__("View Personnel"));

		frm.add_custom_button(__("View Personnel"), () => {
			frappe.call({
				method:
					"personnel_management.personnel_management.doctype.navy_personnel.navy_personnel.get_personnel_for_committee",
				args: {
					committee: frm.doc.name,
				},
				callback(r) {
					const personnel = r.message || [];

					frappe.route_options = {
						name: [
							"in",
							personnel.length ? personnel : ["__no_matching_personnel__"],
						],
					};
					frappe.set_route("List", "Navy Personnel", "List");
				},
			});
		});
	},

	add_workbook_buttons(frm) {
		if (!frm.doc.name || frm.doc.__islocal) {
			return;
		}

		frm.remove_custom_button(__("Validate Workbook"));
		frm.remove_custom_button(__("Import Workbook"));

		frm.add_custom_button(__("Validate Workbook"), () => {
			frappe.call({
				method: "personnel_management.importers.excel_importer.validate_committee_workbook",
				args: {
					committee_name: frm.doc.committee_name,
				},
				freeze: true,
				freeze_message: __("Validating workbook..."),
				callback: (r) => {
					if (!r.message) {
						return;
					}

					const summary = r.message.summary || {};
					const rows = Object.keys(summary)
						.map((key) => {
							const item = summary[key];
							return `
								<tr>
									<td>${frappe.utils.escape_html(key)}</td>
									<td class="text-right">${item.source_rows || 0}</td>
									<td class="text-right">${item.matched || 0}</td>
									<td class="text-right">${item.unmatched || 0}</td>
								</tr>
							`;
						})
						.join("");

					const warnings = (r.message.warnings || [])
						.map((warning) => `<li>${frappe.utils.escape_html(warning)}</li>`)
						.join("");

					frappe.msgprint({
						title: __("Workbook Validation Passed"),
						indicator: "green",
						message: `
							<table class="table table-bordered">
								<thead>
									<tr>
										<th>${__("Sheet")}</th>
										<th class="text-right">${__("Rows")}</th>
										<th class="text-right">${__("Mapped")}</th>
										<th class="text-right">${__("Unmatched")}</th>
									</tr>
								</thead>
								<tbody>${rows}</tbody>
							</table>
							${warnings ? `<p><b>${__("Warnings")}</b></p><ul>${warnings}</ul>` : ""}
						`,
					});
				},
			});
		});

		frm.add_custom_button(__("Import Workbook"), () => {
			frappe.confirm(
				__(
					"This will update personnel, history records, committee records, and conflicts from the attached workbook. Continue?",
				),
				() => {
					frappe.call({
						method: "personnel_management.importers.excel_importer.import_personnel_data",
						args: {
							committee_name: frm.doc.committee_name,
						},
						freeze: true,
						freeze_message: __("Importing workbook..."),
						callback: (r) => {
							if (!r.message) {
								return;
							}

							frappe.msgprint({
								title: __("Import Complete"),
								indicator: "green",
								message: `<pre>${frappe.utils.escape_html(
									JSON.stringify(r.message, null, 2),
								)}</pre>`,
							});
							frm.reload_doc();
						},
					});
				},
			);
		});
	},
});
