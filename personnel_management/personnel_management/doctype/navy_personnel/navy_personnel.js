// Copyright (c) 2026, Youssef and contributors
// For license information, please see license.txt

frappe.ui.form.on("Navy Personnel", {
	setup(frm) {
		set_sorted_personnel_reference_queries(frm);
	},

	refresh(frm) {
		calculate_derived_dates(frm);
	},

	birth_date(frm) {
		calculate_derived_dates(frm);
	},

	high_salary_date(frm) {
		calculate_derived_dates(frm);
	},

	committee_records_add(frm, cdt, cdn) {
		const row = locals[cdt][cdn];

		if (!row.personnel && !frm.is_new()) {
			frappe.model.set_value(cdt, cdn, "personnel", frm.doc.name);
		}
	},
});

function set_sorted_personnel_reference_queries(frm) {
	const reference_fields = {
		unit: "Navy Unit",
		job: "Navy Job",
		rank: "Navy Rank",
		weapon: "Navy Weapon",
	};

	Object.keys(reference_fields).forEach((fieldname) => {
		frm.set_query(fieldname, () => ({
			doctype: reference_fields[fieldname],
			order_by: "name asc",
		}));
	});
}

function calculate_derived_dates(frm) {
	frm.set_value("age", calculate_completed_years(frm.doc.birth_date));
	frm.set_value(
		"service_year_number",
		calculate_completed_years(frm.doc.high_salary_date),
	);
}

function calculate_completed_years(start_date) {
	if (!start_date) {
		return null;
	}

	const start = frappe.datetime.str_to_obj(start_date);
	const today = frappe.datetime.str_to_obj(frappe.datetime.get_today());

	if (start > today) {
		return 0;
	}

	let years = today.getFullYear() - start.getFullYear();
	const has_anniversary_passed =
		today.getMonth() > start.getMonth() ||
		(today.getMonth() === start.getMonth() && today.getDate() >= start.getDate());

	if (!has_anniversary_passed) {
		years -= 1;
	}

	return years;
}

frappe.ui.form.on("Personnel Committee Record", {
	personnel(frm, cdt, cdn) {
		fill_committee_record_from_personnel(cdt, cdn);
	},
});

function fill_committee_record_from_personnel(cdt, cdn) {
	const row = locals[cdt][cdn];

	if (!row.personnel) {
		return;
	}

	frappe.db
		.get_value("Navy Personnel", row.personnel, [
			"military_number",
			"full_name",
			"rank",
			"category",
			"age",
			"service_year_number",
			"weapon",
			"job",
			"unit",
			"report_1",
			"report_2",
			"report_3",
		])
		.then((r) => {
			const personnel = r.message;

			if (!personnel) {
				return;
			}

			const values = {
				military_number: personnel.military_number,
				committee_name_value: personnel.full_name,
				rank: personnel.rank,
				category: personnel.category,
				age: personnel.age,
				service_year_number: personnel.service_year_number,
				weapon: personnel.weapon,
				job: personnel.job,
				unit: personnel.unit,
				report_1: personnel.report_1,
				report_2: personnel.report_2,
				report_3: personnel.report_3,
			};

			Object.keys(values).forEach((fieldname) => {
				frappe.model.set_value(cdt, cdn, fieldname, values[fieldname] || null);
			});
		});
}
