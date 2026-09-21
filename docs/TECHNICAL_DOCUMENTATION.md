# Technical Documentation

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Architecture

```text
Desk UI / Frappe Forms / Custom Pages
    ↓
Client JS controls and frappe.call
    ↓
Whitelisted Python functions / DocType controllers
    ↓
Frappe Document API and database queries
    ↓
MariaDB tables generated from DocTypes
```

## Directory Structure

```text
personnel_management/hooks.py
personnel_management/api.py
personnel_management/config/personnel_management.py
personnel_management/importers/excel_importer.py
personnel_management/services/*.py
personnel_management/personnel_management/doctype/*
personnel_management/personnel_management/page/*
personnel_management/personnel_management/report/*
personnel_management/public/js/personnel_management.js
personnel_management/translations/ar.csv
```

## Hooks

- `app_include_js = /assets/personnel_management/js/personnel_management.js`
- `Navy Personnel.on_update -> personnel_management.services.personnel_sync.sync_committee_records`

## Services

| File | Purpose | Entry Points | Side Effects |
| --- | --- | --- | --- |
| excel_importer.py | Workbook validation/import; mapping; committee record upsert; record source creation | validate_committee_workbook(), import_personnel_data() | Writes many data records during import |
| deduplication.py | Deterministic duplicate/conflict logic | compare_*(), process_and_handle_conflict(), create_conflict() | Creates Personnel Data Conflict |
| conflict_resolution.py | Resolve selected conflict option | resolve_conflict() | Updates history child row and conflict |
| exporter.py | Excel export | get_export_personnel_options(), export_personnel() | Download response only |
| personnel_sync.py | Master to committee sync | sync_committee_records() | Updates Personnel Committee Record rows |
| api.py | Language switch | switch_language() | Updates User.language |


## Pages

| Page | Title | Source JS | Roles |
| --- | --- | --- | --- |
| personnel_conflict_c | Personnel Conflict Center | Navy Personnel Admin, System Manager | personnel_management/personnel_management/page/personnel_conflict_c/personnel_conflict_c.json |
| personnel_export | Personnel Export | No roles in Page JSON | personnel_management/personnel_management/page/personnel_export/personnel_export.json |
| personnel_export-1 | Personnel Export | Navy Personnel Editor, Navy Personnel Admin, System Manager | personnel_management/personnel_management/page/personnel_export_1/personnel_export_1.json |


## Report

`Personnel by Unit` is a Query Report on `Navy Personnel` using SQL grouped by `unit`. Roles: System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor.

## Site Dashboards And Statistics

The repository does not contain Workspace, Dashboard Chart, or Number Card JSON for the personnel dashboards. A read-only site metadata audit on `<site-name>` verified seven private user-specific Workspace records and related Dashboard Chart / Number Card records. See [Dashboards, Reports, And Statistics](DASHBOARDS_REPORTS_AND_STATISTICS.md).

## Client JavaScript

- `navy_personnel.js`: sorted link queries, live age/service calculations, committee-record autofill.
- `navy_personnel_list.js`: committee filter and committee count.
- `personnel_committee.js`: Validate Workbook, Import Workbook, View Personnel.
- `personnel_data_conflict.js`: Resolve with option buttons.
- `personnel_export_1.js`: export page with selection table.
- `public/js/personnel_management.js`: language toggle and dashboard label translation.

## Database Access Patterns

The app uses Frappe document APIs (`frappe.get_doc`, `frappe.new_doc`, `doc.save`, `frappe.get_all`, `frappe.db.set_value`) and some report SQL through Query Report metadata.

## Error Handling

Server errors use `frappe.throw()` or Python exceptions during workbook validation. Client calls show Frappe messages/alerts where implemented.

## Extension Points

- Add new history table: DocType JSON, Navy Personnel Table field, importer mapper, exporter rows, dedup rules if required, docs.
- Add new conflict rule: comparator in `deduplication.py`, importer mapping to comparator, conflict resolution identity verification.
- Add new reference master: DocType, Link field, patch for existing values, JS query if needed.
