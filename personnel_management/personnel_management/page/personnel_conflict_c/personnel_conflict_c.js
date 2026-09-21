// frappe.pages['personnel_conflict_c'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'Personnel Conflict Center',
// 		single_column: true
// 	});
// }

frappe.pages["personnel_conflict_c"].on_page_load = function (wrapper) {
	new PersonnelConflictCenter(wrapper);
};

class PersonnelConflictCenter {
	constructor(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: __("Personnel Conflict Center"),
			single_column: true,
		});

		this.render();
		this.load_conflicts();
	}

	render() {
		$(this.page.body).html(`
            <div style="padding: 20px;">

                <div class="conflict-header" style="margin-bottom: 20px;">
                    <h4>${__("Unresolved Conflicts")}</h4>
                    <p class="text-muted">
                        ${__("Review conflicts that could not be resolved automatically.")}
                    </p>
                </div>

                <div class="conflict-list">
                    <div class="text-muted">
                        ${__("Loading conflicts...")}
                    </div>
                </div>

            </div>
        `);
	}

	load_conflicts() {
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Personnel Data Conflict",
				filters: {
					status: "Unresolved",
				},
				fields: [
					"name",
					"military_number",
					"conflict_type",
					"field_or_record",
					"description",
					"creation",
				],
				order_by: "creation desc",
				limit_page_length: 100,
			},
			callback: (r) => {
				this.render_conflicts(r.message || []);
			},
		});
	}

	render_conflicts(conflicts) {
		const container = $(this.page.body).find(".conflict-list");

		if (!conflicts.length) {
			container.html(`
                <div class="alert alert-success">
                    ${__("No unresolved conflicts.")}
                </div>
            `);
			return;
		}

		let html = `
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>${__("Military Number")}</th>
                            <th>${__("Conflict Type")}</th>
                            <th>${__("Record")}</th>
                            <th>${__("Description")}</th>
                            <th>${__("Action")}</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

		conflicts.forEach((conflict) => {
			html += `
                <tr>
                    <td>${frappe.utils.escape_html(conflict.military_number || "")}</td>
                    <td>${frappe.utils.escape_html(conflict.conflict_type || "")}</td>
                    <td>${frappe.utils.escape_html(conflict.field_or_record || "")}</td>
                    <td>${frappe.utils.escape_html(conflict.description || "")}</td>
                    <td>
                        <button
                            class="btn btn-sm btn-primary"
                            data-name="${conflict.name}">
                            ${__("Review")}
                        </button>
                    </td>
                </tr>
            `;
		});

		html += `
                    </tbody>
                </table>
            </div>
        `;

		container.html(html);

		container.find("button[data-name]").on("click", (e) => {
			const conflict_name = $(e.currentTarget).data("name");

			frappe.set_route("Form", "Personnel Data Conflict", conflict_name);
		});
	}
}
