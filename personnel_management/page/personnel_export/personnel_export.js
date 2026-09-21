frappe.pages["personnel-export"].on_page_load = function (wrapper) {
	new PersonnelExportPage(wrapper);
};

class PersonnelExportPage {
	constructor(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: __("Personnel Export"),
			single_column: true,
		});

		this.render();
	}

	render() {
		$(this.page.body).html(`
            <div style="padding: 20px;">
                <div class="form-group">
                    <label>${__("Military Numbers")}</label>
                    <textarea
                        class="form-control military-numbers"
                        rows="4"
                        placeholder="${frappe.utils.escape_html(__("Enter military numbers, one per line"))}">
                    </textarea>
                </div>

                <button class="btn btn-primary export-btn">
                    ${__("Export to Excel")}
                </button>
            </div>
        `);

		this.bind_events();
	}

	bind_events() {
		$(this.page.body)
			.find(".export-btn")
			.on("click", () => this.export_data());
	}

	export_data() {
		const value = $(this.page.body).find(".military-numbers").val().trim();

		const military_numbers = value ? value.split(/\s+/).filter(Boolean) : null;

		frappe.call({
			method: "personnel_management.services.exporter.export_personnel",
			args: {
				military_numbers: military_numbers,
			},
			freeze: true,
			freeze_message: __("Preparing Excel file..."),
			callback: function () {
				window.open(
					"/api/method/personnel_management.services.exporter.export_personnel" +
						"?military_numbers=" +
						encodeURIComponent(JSON.stringify(military_numbers)),
				);
			},
		});
	}
}
