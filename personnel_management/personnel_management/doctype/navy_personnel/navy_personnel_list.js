frappe.listview_settings["Navy Personnel"] = {
	onload(listview) {
		add_committee_filter(listview);
	},

	refresh(listview) {
		render_committee_counts(listview);
	},
};

function add_committee_filter(listview) {
	if (listview.personnel_committee_filter) {
		return;
	}

	const wrapper = listview.$page.find(".standard-filter-section");
	const filter_wrapper = $('<div class="col-md-2 personnel-committee-filter">').appendTo(
		wrapper,
	);

	listview.personnel_committee_filter = frappe.ui.form.make_control({
		parent: filter_wrapper,
		only_input: true,
		render_input: true,
		df: {
			fieldname: "personnel_committee_filter",
			fieldtype: "Link",
			label: __("Committee"),
			options: "Personnel Committee",
			placeholder: __("Committee"),
			change() {
				apply_committee_filter(
					listview,
					listview.personnel_committee_filter.get_value(),
				);
			},
		},
	});

	listview.personnel_committee_filter.refresh();
}

function apply_committee_filter(listview, committee) {
	listview.filter_area.remove("name").then(() => {
		if (!committee) {
			listview.refresh();
			return;
		}

		frappe.call({
			method:
				"personnel_management.personnel_management.doctype.navy_personnel.navy_personnel.get_personnel_for_committee",
			args: { committee },
			callback(r) {
				const personnel = r.message || [];
				const filter_value = personnel.length ? personnel : ["__no_matching_personnel__"];

				listview.filter_area.add([
					[listview.doctype, "name", "in", filter_value],
				]);
			},
		});
	});
}

function render_committee_counts(listview) {
	const personnel = (listview.data || []).map((row) => row.name).filter(Boolean);

	add_committee_count_header(listview);

	if (!personnel.length) {
		return;
	}

	frappe.call({
		method:
			"personnel_management.personnel_management.doctype.navy_personnel.navy_personnel.get_committee_summaries",
		args: {
			personnel_names: JSON.stringify(personnel),
		},
		callback(r) {
			const summaries = r.message || {};

			(listview.data || []).forEach((row) => {
				const summary = summaries[row.name] || { count: 0, committees: [] };
				add_committee_count_cell(listview, row.name, summary);
			});
		},
	});
}

function add_committee_count_header(listview) {
	const header = listview.$result.find(".list-row-head .level-left").first();

	if (!header.length || header.find(".personnel-committee-count-header").length) {
		return;
	}

	header.append(`
		<div class="list-row-col ellipsis hidden-xs text-muted personnel-committee-count-header">
			${__("Committees")}
		</div>
	`);
}

function add_committee_count_cell(listview, docname, summary) {
	const escaped_name = frappe.utils.escape_html(docname).replace(/'/g, "\\'");
	const row = listview.$result
		.find(`.list-row-checkbox[data-name='${escaped_name}']`)
		.closest(".list-row-container")
		.find(".level-left.ellipsis")
		.first();

	if (!row.length) {
		return;
	}

	row.find(".personnel-committee-count-cell").remove();

	const committees = summary.committees || [];
	const title = committees.length
		? committees.join("\n")
		: __("No committees");

	row.append(`
		<div class="list-row-col ellipsis hidden-xs personnel-committee-count-cell"
			title="${frappe.utils.escape_html(title)}">
			<span class="indicator-pill gray">${summary.count || 0}</span>
		</div>
	`);
}
