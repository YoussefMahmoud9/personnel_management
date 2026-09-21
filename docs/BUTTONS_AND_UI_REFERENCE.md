# Buttons And UI Reference

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Custom Buttons And Controls

| Name | Location | Who can see/use it | Backend/service | Data affected | Purpose/Risk |
| --- | --- | --- | --- | --- | --- |
| Language toggle | Desk navbar, global JS | Logged-in users; Guest excluded by JS | personnel_management.api.switch_language | User.language via frappe.db.set_value | Switches between Arabic/English and reloads. Risk: changes current user language. |
| Validate Workbook | Personnel Committee form | Users who can open saved Personnel Committee form and load JS; server permissions still apply | personnel_management.importers.excel_importer.validate_committee_workbook | Read-only workbook validation | Checks workbook sheets/columns/mappings. No data write expected. |
| Import Workbook | Personnel Committee form | Users who can access form/button; import method is whitelisted | personnel_management.importers.excel_importer.import_personnel_data | Navy Personnel, child history, committee records, record sources, conflicts | Runs real import. Dangerous because it writes production data. |
| View Personnel | Personnel Committee form | Users who can access committee form | get_personnel_for_committee() then frappe route to Navy Personnel list | No data write | Filters Navy Personnel list to committee members. |
| Resolve with Option 1/2/etc. | Personnel Data Conflict form | Only unresolved existing conflict forms; page access depends on DocType permissions | personnel_management.services.conflict_resolution.resolve_conflict | Updates matching child row and conflict status/options | Manual conflict resolution. Risk: selected option overwrites target history fields. |
| Review | Conflict Center page | Roles in page JSON: Navy Personnel Admin, System Manager | frappe.set_route to Personnel Data Conflict form | No direct write | Opens selected conflict for review. |
| Export Mode select | Personnel Export page personnel_export-1 | Page roles: Navy Personnel Editor/Admin/System Manager | Client-side page state | No write | Chooses all/committee/selected export mode. |
| Committee select | Personnel Export page committee mode | Same as page | export_personnel committee_name parameter | No write; export file generated | Filters export to committee membership. |
| Personnel search | Personnel Export page selected mode | Same as page | get_export_personnel_options() for options | No write | Filters selectable table by military number/name. |
| Unit filter | Personnel Export page selected mode | Same as page | Client-side filter | No write | Filters selectable table by unit. |
| Rank filter | Personnel Export page selected mode | Same as page | Client-side filter | No write | Filters selectable table by rank. |
| Select Shown | Personnel Export page selected mode | Same as page | Client-side Set | No write | Selects all currently filtered rows. |
| Clear | Personnel Export page selected mode | Same as page | Client-side Set | No write | Clears selected personnel. |
| Export to Excel | Personnel Export pages | Depends on page access | personnel_management.services.exporter.export_personnel | No DB write; creates response download | Downloads personnel_export.xlsx. Error if no personnel found. |
| Committee filter | Navy Personnel list | Users who can access Navy Personnel list | get_personnel_for_committee() | No write | Filters list by child committee membership. |
| Photo upload controls | Navy Personnel form fields image/family_photo | Users with write access to Navy Personnel | Frappe File + navy_personnel.py normalization on save | File records and public files | Uploads/replaces images using military number naming. |


## Relevant Standard Frappe Controls

| Control | Location | Meaning In This App | Risk |
| --- | --- | --- | --- |
| New | List/Form toolbar | Creates a new record when role permits create. | Can create duplicate/business-invalid records if used carelessly. |
| Save | Form toolbar | Runs client/server validation and stores the document. | Triggers Navy Personnel sync and photo normalization. |
| Delete | Form menu/button if permitted | Deletes a document through Frappe. | Dangerous; may affect linked/child data. |
| Search bar | Desk navbar/list views | Finds pages, DocTypes, records. | No direct data risk. |
| List filters | List view | Filters records by permitted fields. | Invalid custom field filters can cause Frappe query errors. |
| Attach/Upload | Attach fields | Creates/links File records. | Wrong file can be attached; photo save normalizes if source is valid. |


## Error / Validation Messages From Source

- `Personnel Committee is required.`
- `Excel file not found: 0`
- `Source workbook column validation failed:`
- `Missing required sheets: 0`
- `Saved history record could not be found.`
- `Existing duplicate history record could not be found.`
- `This conflict is already resolved.`
- `Selected option was not found.`
- `The conflicting history record could not be found.`
- `No personnel records found.`
- `Please log in before changing language.`
- `Unsupported language.`
