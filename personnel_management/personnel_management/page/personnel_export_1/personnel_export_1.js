// frappe.pages['personnel_export-1'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'Personnel Export',
// 		single_column: true
// 	});
// }

frappe.pages["personnel_export-1"].on_page_load = function (wrapper) {
	new PersonnelExportPage(wrapper);
};

class PersonnelExportPage {
	constructor(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: __("Personnel Export"),
			single_column: true,
		});

		this.personnel = [];
		this.selected_personnel = new Set();

		this.render();
	}

	render() {
		$(this.page.body).html(`
            <div style="padding: 20px;">

                <div class="form-group">
                    <label>${__("Export Mode")}</label>
                    <select class="form-control export-mode">
                        <option value="all">${__("All Personnel")}</option>
                        <option value="committee">${__("Specific Committee")}</option>
                        <option value="selected">${__("Selected Personnel")}</option>
                    </select>
                </div>

                <div class="form-group committee-group" style="display:none;">
                    <label>${__("Committee")}</label>
                    <select class="form-control committee-select">
                        <option value="">${__("Loading committees...")}</option>
                    </select>
                </div>

                <div class="form-group personnel-group" style="display:none;">
                    <label>${__("Selected Personnel")}</label>

                    <div class="row" style="margin-bottom: 10px;">
                        <div class="col-sm-4">
                            <input
                                class="form-control personnel-search"
                                placeholder="${frappe.utils.escape_html(__("Search military number or name"))}"
                            />
                        </div>
                        <div class="col-sm-3">
                            <select class="form-control unit-filter">
                                <option value="">${__("All Units")}</option>
                            </select>
                        </div>
                        <div class="col-sm-3">
                            <select class="form-control rank-filter">
                                <option value="">${__("All Ranks")}</option>
                            </select>
                        </div>
                        <div class="col-sm-2">
                            <button class="btn btn-default btn-block clear-selected-personnel">
                                ${__("Clear")}
                            </button>
                        </div>
                    </div>

                    <div style="margin-bottom: 10px;">
                        <button class="btn btn-default btn-sm select-visible-personnel">
                            ${__("Select Shown")}
                        </button>
                        <span class="text-muted selected-personnel-count" style="margin-left: 10px;"></span>
                    </div>

                    <div class="table-responsive" style="max-height: 420px; overflow: auto;">
                        <table class="table table-bordered table-hover personnel-selection-table">
                            <thead>
                                <tr>
                                    <th style="width: 40px;"></th>
                                    <th>${__("Military Number")}</th>
                                    <th>${__("Full Name")}</th>
                                    <th>${__("Unit")}</th>
                                    <th>${__("Rank")}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td colspan="5" class="text-muted">${__("Loading personnel...")}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <button class="btn btn-primary export-btn">
                    ${__("Export to Excel")}
                </button>

            </div>
        `);

		this.load_committees();
		this.load_personnel();
		this.bind_events();
	}

	load_committees() {
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Personnel Committee",
				fields: ["name", "committee_name"],
				order_by: "committee_name asc",
				limit_page_length: 0,
			},
			callback: (r) => {
				const select = $(this.page.body).find(".committee-select");

				select.empty();
				select.append(`<option value="">${__("Select Committee")}</option>`);

				(r.message || []).forEach((committee) => {
					select.append(
						$("<option>", {
							value: committee.name,
							text: committee.committee_name,
						}),
					);
				});
			},
		});
	}

	bind_events() {
		$(this.page.body)
			.find(".export-mode")
			.on("change", (e) => {
				const mode = e.target.value;

				$(this.page.body)
					.find(".committee-group")
					.toggle(mode === "committee");

				$(this.page.body)
					.find(".personnel-group")
					.toggle(mode === "selected");
			});

		$(this.page.body)
			.find(".personnel-search, .unit-filter, .rank-filter")
			.on("input change", () => this.render_personnel_table());

		$(this.page.body)
			.find(".select-visible-personnel")
			.on("click", () => this.select_visible_personnel());

		$(this.page.body)
			.find(".clear-selected-personnel")
			.on("click", () => {
				this.selected_personnel.clear();
				this.render_personnel_table();
			});

		$(this.page.body).on("change", ".personnel-select", (e) => {
			const military_number = e.target.value;

			if (e.target.checked) {
				this.selected_personnel.add(military_number);
			} else {
				this.selected_personnel.delete(military_number);
			}

			this.update_selected_count();
		});

		$(this.page.body)
			.find(".export-btn")
			.on("click", () => this.export_data());
	}

	load_personnel() {
		frappe.call({
			method: "personnel_management.services.exporter.get_export_personnel_options",
			callback: (r) => {
				this.personnel = r.message || [];
				this.populate_personnel_filters();
				this.render_personnel_table();
			},
		});
	}

	populate_personnel_filters() {
		const units = this.unique_values("unit");
		const ranks = this.unique_values("rank");

		const unit_filter = $(this.page.body).find(".unit-filter");
		const rank_filter = $(this.page.body).find(".rank-filter");

		units.forEach((unit) => {
			unit_filter.append($("<option>", { value: unit, text: unit }));
		});

		ranks.forEach((rank) => {
			rank_filter.append($("<option>", { value: rank, text: rank }));
		});
	}

	unique_values(fieldname) {
		return [
			...new Set(
				this.personnel
					.map((row) => row[fieldname])
					.filter((value) => value),
			),
		].sort((a, b) => a.localeCompare(b, "ar"));
	}

	filtered_personnel() {
		const search = ($(this.page.body).find(".personnel-search").val() || "")
			.trim()
			.toLowerCase();
		const unit = $(this.page.body).find(".unit-filter").val();
		const rank = $(this.page.body).find(".rank-filter").val();

		return this.personnel.filter((row) => {
			if (unit && row.unit !== unit) {
				return false;
			}

			if (rank && row.rank !== rank) {
				return false;
			}

			if (!search) {
				return true;
			}

			return [row.military_number, row.full_name]
				.filter(Boolean)
				.some((value) => String(value).toLowerCase().includes(search));
		});
	}

	render_personnel_table() {
		const rows = this.filtered_personnel();
		const tbody = $(this.page.body).find(".personnel-selection-table tbody");

		tbody.empty();

		if (!rows.length) {
			tbody.append(
				`<tr><td colspan="5" class="text-muted">${__("No personnel found.")}</td></tr>`,
			);
			this.update_selected_count();
			return;
		}

		rows.forEach((row) => {
			const military_number = frappe.utils.escape_html(row.military_number || "");

			tbody.append(`
                <tr>
                    <td>
                        <input
                            type="checkbox"
                            class="personnel-select"
                            value="${military_number}"
                            ${this.selected_personnel.has(row.military_number) ? "checked" : ""}
                        />
                    </td>
                    <td>${military_number}</td>
                    <td>${frappe.utils.escape_html(row.full_name || "")}</td>
                    <td>${frappe.utils.escape_html(row.unit || "")}</td>
                    <td>${frappe.utils.escape_html(row.rank || "")}</td>
                </tr>
            `);
		});

		this.update_selected_count();
	}

	select_visible_personnel() {
		this.filtered_personnel().forEach((row) => {
			if (row.military_number) {
				this.selected_personnel.add(row.military_number);
			}
		});

		this.render_personnel_table();
	}

	update_selected_count() {
		$(this.page.body)
			.find(".selected-personnel-count")
			.text(
				__(
					"{0} selected / {1} shown",
					[this.selected_personnel.size, this.filtered_personnel().length],
				),
			);
	}

	export_data() {
		const mode = $(this.page.body).find(".export-mode").val();

		let military_numbers = null;
		let committee_name = null;

		if (mode === "committee") {
			committee_name = $(this.page.body).find(".committee-select").val();

			if (!committee_name) {
				frappe.msgprint(__("Please select a committee."));
				return;
			}
		}

		if (mode === "selected") {
			military_numbers = Array.from(this.selected_personnel);

			if (!military_numbers.length) {
				frappe.msgprint(__("Please select at least one personnel record."));
				return;
			}
		}

		let url = "/api/method/personnel_management.services.exporter.export_personnel";

		const params = [];

		if (military_numbers) {
			params.push(
				"military_numbers=" + encodeURIComponent(JSON.stringify(military_numbers)),
			);
		}

		if (committee_name) {
			params.push("committee_name=" + encodeURIComponent(committee_name));
		}

		if (params.length) {
			url += "?" + params.join("&");
		}

		window.open(url);
	}
}
