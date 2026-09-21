# Personnel Management Documentation Index

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Who Should Read What

| Reader | Start Here | Then Read |
| --- | --- | --- |
| Complete beginner | BEGINNER_TO_EXPERT_GUIDE.md | COMPLETE_SYSTEM_GUIDE.md, USER_GUIDE.md |
| Normal user | USER_GUIDE.md | BUTTONS_AND_UI_REFERENCE.md, TROUBLESHOOTING.md |
| System administrator | ADMIN_GUIDE.md | PERMISSIONS_AND_ROLES_REFERENCE.md, IMPORT_EXPORT_DETAILED_GUIDE.md |
| Developer | TECHNICAL_DOCUMENTATION.md | DOCTYPE_AND_FIELD_REFERENCE.md, DATA_MODEL_AND_RELATIONSHIPS.md |
| Senior Frappe developer | COMPLETE_SYSTEM_GUIDE.md | all reference documents, especially DATA_IMPORT_SPECIFICATION.md and CONFLICT_AND_DEDUPLICATION_REFERENCE.md |

## Complete Documentation Set

- [Complete System Guide](COMPLETE_SYSTEM_GUIDE.md) - master manual and end-to-end lifecycle.
- [Beginner To Expert Guide](BEGINNER_TO_EXPERT_GUIDE.md) - progressive teaching from zero knowledge to architecture.
- [User Guide](USER_GUIDE.md) - step-by-step application workflows.
- [Administrator Guide](ADMIN_GUIDE.md) - operations, roles, maintenance, safety.
- [Buttons And UI Reference](BUTTONS_AND_UI_REFERENCE.md) - implemented buttons, controls, pages, and standard relevant Frappe controls.
- [DocType And Field Reference](DOCTYPE_AND_FIELD_REFERENCE.md) - generated from DocType JSON metadata.
- [Permissions And Roles Reference](PERMISSIONS_AND_ROLES_REFERENCE.md) - role and permission matrix from JSON/Page/Report config.
- [Data Model And Relationships](DATA_MODEL_AND_RELATIONSHIPS.md) - parent/child tables, links, provenance, ER diagram.
- [Import Export Detailed Guide](IMPORT_EXPORT_DETAILED_GUIDE.md) - workbook sheets, mappings, validation, export sheets.
- [Conflict And Deduplication Reference](CONFLICT_AND_DEDUPLICATION_REFERENCE.md) - exact rules from `deduplication.py`.
- [Photo And File Management](PHOTO_AND_FILE_MANAGEMENT.md) - image storage and server-side enforcement.
- [Technical Documentation](TECHNICAL_DOCUMENTATION.md) - complete implementation architecture.
- [Developer Maintenance Guide](DEVELOPER_MAINTENANCE_GUIDE.md) - safe changes, tests, migrations.
- [Troubleshooting](TROUBLESHOOTING.md) - real problems and fixes based on implementation.
- [Data Import Specification](DATA_IMPORT_SPECIFICATION.md) - import data contract and source rules.
- [Dashboards, Reports, And Statistics](DASHBOARDS_REPORTS_AND_STATISTICS.md) - verified site private dashboards, chart records, number cards, and the standard report.

## Current App Inventory

| Component | Count | Source |
| --- | --- | --- |
| DocTypes | 20 | DocType JSON files |
| Fields | 118 | DocType JSON fields |
| Child Tables | 13 | DocType JSON istable |
| Pages | 3 | Page JSON files |
| Reports | 1 | Report JSON files |
| Source Workspace JSON | 0 | No workspace JSON in app source |
| Site Private Workspaces | 7 | Verified in `<site-name>` database |
| Source Dashboard Charts | 0 | No dashboard chart JSON in app source |
| Site Dashboard Charts | 12 personnel-related records | Verified in `<site-name>` database |
| Source Number Cards | 0 | No number card JSON in app source |
| Site Number Cards | 3 personnel-related records | Verified in `<site-name>` database |
