from frappe import _


def get_data():
	return [
		{
			"label": _("Personnel"),
			"items": [
				{
					"type": "doctype",
					"name": "Navy Personnel",
					"description": _("Authoritative personnel master records."),
				},
				{
					"type": "doctype",
					"name": "Personnel Committee",
					"description": _("Committee setup and attached Excel import files."),
				},
				{
					"type": "doctype",
					"name": "Personnel Committee Record",
					"description": _("Current personnel snapshots per committee."),
				},
			],
		},
		{
			"label": _("Workflow"),
			"items": [
				{
					"type": "page",
					"name": "personnel_conflict_c",
					"label": _("Conflict Center"),
					"description": _("Review unresolved import conflicts."),
				},
				{
					"type": "page",
					"name": "personnel_export",
					"label": _("Personnel Export"),
					"description": _("Export personnel data to Excel."),
				},
			],
		},
		{
			"label": _("Audit"),
			"items": [
				{
					"type": "doctype",
					"name": "Personnel Data Conflict",
					"description": _("Import conflicts and resolution history."),
				},
			],
		},
	]
