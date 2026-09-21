# Beginner To Expert Guide

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Level 0 - Absolute Beginner

### What Frappe Is

Frappe is the web framework that runs this app. It gives the system forms, lists, permissions, pages, reports, database tables, file attachments, and server APIs.

### What ERPNext Is

ERPNext is a large application built on Frappe. This custom app runs in the same bench/site environment as ERPNext. This app does not modify ERPNext core.

### Basic Terms Using This App

| Term | Simple Meaning | Example in this app |
| --- | --- | --- |
| DocType | A blueprint for records and database table. | `Navy Personnel` |
| Record / Document | One saved item of a DocType. | One person with military number 201... |
| Field | One piece of information on a record. | `full_name`, `rank`, `unit` |
| Link field | A field that points to another DocType. | `unit` links to `Navy Unit` |
| Child Table | A table inside a parent record. | Detentions inside Navy Personnel |
| Role | A named access level. | `Navy Personnel Editor` |
| Permission | Rules saying who can read/write/create/delete. | Editor can write Navy Personnel |
| Workspace | Navigation page grouping links. | Personnel Management workspace: source JSON not present; module config exists. |
| Report | A view that calculates or lists data. | `Personnel by Unit` |
| Query Report | A report powered by SQL. | Personnel count grouped by unit |
| Dashboard Chart | A chart widget in Desk. | No dashboard chart JSON in source; translation JS references dashboard labels. |
| Attach Image | File/image upload field. | `image`, `family_photo` |
| Import | Reading Excel into records. | Committee Import Workbook |
| Export | Writing records to Excel. | Personnel Export page |


## Level 1 - Application User

1. Log in to the Frappe site.
2. Use the search bar or workspace links to open `Navy Personnel`, `Personnel Committee`, Conflict Center, or Export.
3. Use list filters to find people by military number, name, unit, rank, or committee filter.
4. Open a person to view current data and historical child tables.
5. Edit only fields you are allowed to edit.
6. Use committee forms to validate/import workbooks if your role allows.
7. Use Conflict Center to review unresolved conflicts if your role allows.
8. Use `/app/personnel_export-1` to export all, committee, or selected personnel.

## Level 2 - Administrator

Administrators maintain roles, committees, imports, conflict review, backups, and safe cleanup. They should use workbook validation before import and should not delete production rows without a specific cleanup rule.

## Level 3 - Developer

Developers work with:

- DocType JSON in `personnel_management/personnel_management/doctype/`
- Python controllers beside DocType JSON.
- Client JS beside forms/lists/pages.
- Services in `personnel_management/services/`.
- Importer in `personnel_management/importers/excel_importer.py`.
- Hooks in `personnel_management/hooks.py`.

## Level 4 - Expert

Expert work requires understanding the whole data flow: master identity, child table persistence, Frappe document lifecycle, hooks, provenance, deterministic deduplication, conflict persistence, file records, and role boundaries. For safe modification, change one mechanism at a time and verify using py_compile/node checks plus read-only data audits.

## Installation / Setup From Zero

### Existing Verified Project Setup

The app exists at:

```text
<bench-path>/apps/personnel_management
```

The site used during development is:

```text
<site-name>
```

Commands used in this environment include:

```bash
cd <bench-path>
bench --site <site-name> migrate
bench --site <site-name> clear-cache
bench restart
bench --site <site-name> mariadb -e "SELECT 1"
```

### Generic Frappe Setup Information

Status: Environment-specific / not fully verified in this repository. A new installation generally requires Linux/WSL2, Python, Node/Yarn, MariaDB, Redis, wkhtmltopdf where needed, Bench, a Frappe site, ERPNext if desired, then app installation. Use official Frappe documentation for exact commands for your operating system and Frappe version.
