(function () {
	const personnel_dashboard_labels = {
		"Detentions Charts & Dashboard": "Detentions Charts & Dashboard",
		"Detentions Charts & Dashboards": "Detentions Charts & Dashboards",
		"Detentions Charts & Dashboards-Administrator":
			"Detentions Charts & Dashboards",
		"Imprisonments Charts & Dashboard": "Imprisonments Charts & Dashboard",
		"Imprisonments Charts & Dashboards": "Imprisonments Charts & Dashboards",
		"Imprisonments Charts & Dashboards -Administrator":
			"Imprisonments Charts & Dashboards",
		"Medical Committees Charts & Dashboard":
			"Medical Committees Charts & Dashboard",
		"Medical Committees Charts & Dashboards":
			"Medical Committees Charts & Dashboards",
		"Medical Committees Charts & Dashboards-Administrator":
			"Medical Committees Charts & Dashboards",
		"Military Courts Charts & Dashboard": "Military Courts Charts & Dashboard",
		"Military Courts Charts & Dashboards": "Military Courts Charts & Dashboards",
		"Military Courts Charts & Dashboards-Administrator":
			"Military Courts Charts & Dashboards",
		"Personnel Charts & Dashboard": "Personnel Charts & Dashboard",
		"Personnel Charts & Dashboard -Administrator": "Personnel Charts & Dashboard",
		"Travel Charts & Dashboard": "Travel Charts & Dashboard",
		"Travel Charts & Dashboards": "Travel Charts & Dashboards",
		"Travel Charts & Dashboards -Administrator": "Travel Charts & Dashboards",
		"Detentions By Rank": "Detentions By Rank",
		"Detentions By Unit": "Detentions By Unit",
		"Detentions by Rank": "Detentions by Rank",
		"Detentions by Unit": "Detentions by Unit",
		"ImprisonmentsBy Rank": "Imprisonments By Rank",
		"Imprisonments By Rank": "Imprisonments By Rank",
		"Imprisonments by Rank": "Imprisonments by Rank",
		"Imprisonmentsby Unit": "Imprisonments by Unit",
		"Imprisonments by Unit": "Imprisonments by Unit",
		"Medical CommitteesBy Rank": "Medical Committees By Rank",
		"Medical Committees By Rank": "Medical Committees By Rank",
		"Medical Committees by Rank": "Medical Committees by Rank",
		"Medical Committeesby Unit": "Medical Committees by Unit",
		"Medical Committees by Unit": "Medical Committees by Unit",
		"Military CourtsBy Rank": "Military Courts By Rank",
		"Military Courts By Rank": "Military Courts By Rank",
		"Military Courts by Rank": "Military Courts by Rank",
		"Military Courtsby Unit": "Military Courts by Unit",
		"Military Courts By Unit": "Military Courts By Unit",
		"Military Courts by Unit": "Military Courts by Unit",
		"Personnel By Rank": "Personnel By Rank",
		"Personnel by Rank": "Personnel by Rank",
		"Personnel by Unit": "Personnel by Unit",
		"Travel By Rank": "Travel By Rank",
		"travel By Rank": "Travel By Rank",
		"Travel by Rank": "Travel by Rank",
		"Travel By Unit": "Travel By Unit",
		"Travel by Unit": "Travel by Unit",
	};

	function current_language() {
		return frappe.boot.lang || (frappe.boot.user && frappe.boot.user.language) || "en";
	}

	function next_language() {
		return current_language().startsWith("ar") ? "en" : "ar";
	}

	function button_label() {
		return next_language() === "ar" ? "العربية" : "English";
	}

	function add_language_button() {
		if (!frappe.ui || !frappe.ui.toolbar || frappe.session.user === "Guest") {
			return;
		}

		$(".personnel-language-toggle").remove();

		const $button = $(`
			<button class="btn btn-default btn-sm personnel-language-toggle" type="button">
				${frappe.utils.escape_html(button_label())}
			</button>
		`);

		$button.on("click", () => {
			const language = next_language();

			frappe.call({
				method: "personnel_management.api.switch_language",
				args: { language },
				freeze: true,
				freeze_message: __("Switching language..."),
				callback: () => {
					window.location.reload();
				},
			});
		});

		$(".navbar .navbar-collapse").append($button);
	}

	function normalize_label(text) {
		return (text || "").replace(/\s+/g, " ").trim();
	}

	function translate_personnel_dashboard_labels() {
		const selectors = [
			".layout-main-section span",
			".layout-main-section h1",
			".layout-main-section h2",
			".layout-main-section h3",
			".layout-main-section h4",
			".layout-main-section .ce-header",
			".layout-main-section .widget-title",
			".layout-main-section .chart-title",
			".sidebar-item-label",
			".standard-sidebar-label",
		].join(",");

		$(selectors).each(function () {
			const label = normalize_label($(this).text());
			const source = personnel_dashboard_labels[label];

			if (!source) {
				return;
			}

			const translated = __(source);

			if (label !== normalize_label(translated)) {
				$(this).text(translated);
			}
		});
	}

	function setup_dashboard_label_translation() {
		translate_personnel_dashboard_labels();

		if (window.personnel_dashboard_translation_observer) {
			return;
		}

		window.personnel_dashboard_translation_observer = new MutationObserver(() => {
			translate_personnel_dashboard_labels();
		});

		window.personnel_dashboard_translation_observer.observe(document.body, {
			childList: true,
			subtree: true,
		});
	}

	$(document).on("toolbar_setup", add_language_button);
	$(document).on("page-change route-change", translate_personnel_dashboard_labels);
	$(add_language_button);
	$(setup_dashboard_label_translation);
})();
