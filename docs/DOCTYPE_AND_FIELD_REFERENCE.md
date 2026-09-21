# DocType And Field Reference

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Summary

| Item | Count |
| --- | --- |
| DocTypes | 20 |
| Fields | 118 |
| Child Tables | 13 |


## Navy Job
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/navy_job/navy_job.json |
| Module | Personnel Management |
| Type | Standalone DocType |
| Is Child Table | 0 |
| Naming / autoname | field:job_name |
| Title field | job_name |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Reference master for job Link values. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| job_name | Job Name | Data | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
## Navy Personnel
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/navy_personnel/navy_personnel.json |
| Module | Personnel Management |
| Type | Standalone DocType |
| Is Child Table | 0 |
| Naming / autoname | field:military_number |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Authoritative master record for one person, identified by military_number. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| military_number | Military Number | Data | 1 |  |  |  | Primary business identity for one person. |  |  |
| full_name | Full Name | Data | 1 |  |  |  | Person name. |  |  |
| birth_date | Birth Date | Date | 1 |  |  |  | Date used to calculate age. |  |  |
| address | Address | Small Text | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| image | Image | Attach Image | 0 |  |  | Frappe File attachment | Frappe file attachment field. | navy_personnel.py photo normalization | Stored as /files/Personnel/<military_number>.<extension> by server code. |
| weapon | Weapon | Link | 1 |  | Navy Weapon | Link -> Navy Weapon | Reference to Navy Weapon. | navy_personnel.js sorted Link queries |  |
| unit | Unit | Link | 1 |  | Navy Unit | Link -> Navy Unit | Reference to Navy Unit. | navy_personnel.js sorted Link queries |  |
| rank | Rank | Link | 1 |  | Navy Rank | Link -> Navy Rank | Reference to Navy Rank. | navy_personnel.js sorted Link queries |  |
| category | Category | Data | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| job | Job | Link | 1 |  | Navy Job | Link -> Navy Job | Reference to Navy Job. | navy_personnel.js sorted Link queries |  |
| service_year_number | Service Year Number | Float | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py calculate_derived_dates(); navy_personnel.js live calculation |  |
| high_salary_date | High Salary Date | Date | 1 |  |  |  | Date used to calculate service_year_number. |  |  |
| social_status | Social Status | Select | 1 |  | متزوج<br>ارمل<br>مطلق<br>اعزب |  | Arabic social status selection. |  | Select options exactly: متزوج, ارمل, مطلق, اعزب. |
| age | Age | Float | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py calculate_derived_dates(); navy_personnel.js live calculation |  |
| promotions | Promotions | Table | 0 |  | Personnel Promotion | Table -> Personnel Promotion | Child table storing Personnel Promotion rows. |  |  |
| measurements | Measurements | Table | 0 |  | Personnel Measurement | Table -> Personnel Measurement | Child table storing Personnel Measurement rows. |  |  |
| medical_committees | Medical Committees | Table | 0 |  | Personnel Medical Committee | Table -> Personnel Medical Committee | Child table storing Personnel Medical Committee rows. |  |  |
| unit_history | Unit History | Table | 0 |  | Personnel Unit History | Table -> Personnel Unit History | Child table storing Personnel Unit History rows. |  |  |
| travel_history | Travel History  | Table | 0 |  | Personnel Travel | Table -> Personnel Travel | Child table storing Personnel Travel rows. |  |  |
| punishments | Punishments | Table | 0 |  | Personnel punishment | Table -> Personnel punishment | Child table storing Personnel punishment rows. |  |  |
| detentions | Detentions | Table | 0 |  | Personnel Detention | Table -> Personnel Detention | Child table storing Personnel Detention rows. |  |  |
| imprisonments | Imprisonments | Table | 0 |  | Personnel Imprisonment | Table -> Personnel Imprisonment | Child table storing Personnel Imprisonment rows. |  |  |
| military_courts | Military Courts | Table | 0 |  | Personnel Military Court | Table -> Personnel Military Court | Child table storing Personnel Military Court rows. |  |  |
| volunteer_date | Volunteer Date | Date | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| service_information_section | Service Information | Section Break | 0 |  |  |  | UI section separator; stores no business value. |  |  |
| personnel_history_section | Personnel History | Section Break | 0 |  |  |  | UI section separator; stores no business value. |  |  |
| committee_records | Committee Records | Table | 0 |  | Personnel Committee Record | Table -> Personnel Committee Record | Child table storing Personnel Committee Record rows. |  |  |
| reports_section | Reports | Section Break | 0 |  |  |  | UI section separator; stores no business value. |  |  |
| report_1 | Report 1 | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| report_2 | Report 2 | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| report_3 | Report 3 | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| promotion_promise_date | Promotion Promise Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| family_information_section | Family Information | Section Break | 0 |  |  |  | UI section separator; stores no business value. |  |  |
| number_of_girls | Number of Girls | Int | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| names_of_girls | Names of Girls | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| number_of_boys | Number of Boys | Int | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| names_of_boys | Names of Boys | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| record_sources | Record Sources | Table | 0 |  | Personnel Record Source | Table -> Personnel Record Source | Child table storing Personnel Record Source rows. |  |  |
| family_photo | Family Photo | Attach Image | 0 |  |  | Frappe File attachment | Frappe file attachment field. | navy_personnel.py photo normalization | Stored as /files/Personnel/Family/<military_number>.<extension> by server code. |
| family_image | Family Image  | Attach Image | 0 |  |  | Frappe File attachment | Frappe file attachment field. | navy_personnel.py photo normalization | Legacy/hidden field in JSON. Code clears it when family_photo is normalized. |
### Permission Rules
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 |
## Navy Rank
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/navy_rank/navy_rank.json |
| Module | Personnel Management |
| Type | Standalone DocType |
| Is Child Table | 0 |
| Naming / autoname | field:rank_name |
| Title field | rank_name |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Reference master for rank Link values. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rank_name | Rank Name | Data | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
## Navy Unit
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/navy_unit/navy_unit.json |
| Module | Personnel Management |
| Type | Standalone DocType |
| Is Child Table | 0 |
| Naming / autoname | field:unit_name |
| Title field | unit_name |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Reference master for unit Link values. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unit_name | Unit Name | Data | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
## Navy Weapon
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/navy_weapon/navy_weapon.json |
| Module | Personnel Management |
| Type | Standalone DocType |
| Is Child Table | 0 |
| Naming / autoname | field:weapon_name |
| Title field | weapon_name |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Reference master for weapon Link values. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| weapon_name | Weapon Name | Data | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
## Personnel Child
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_child/personnel_child.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Child table for family counts/names. Status: present in source but not currently used by Navy Personnel table fields. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| number_of_girls | Number of Girls | Int | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| names_of_girls | Names of Girls | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| number_of_boys | Number of Boys | Int | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| names_of_boys | Names of Boys | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Committee
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_committee/personnel_committee.json |
| Module | Personnel Management |
| Type | Standalone DocType |
| Is Child Table | 0 |
| Naming / autoname | field:committee_name |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Committee/import context with an attached Excel file. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| personnel_committee_section | Personnel Committee | Section Break | 0 |  |  |  | UI section separator; stores no business value. |  |  |
| committee_name | Committee Name | Data | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| excel_file | Excel File | Attach | 0 |  |  | Frappe File attachment | Frappe file attachment field. |  |  |
| created_date | Created Date | Date | 0 | Today |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| active | Active | Check | 0 | 0 |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
## Personnel Committee Record
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_committee_record/personnel_committee_record.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Child-table snapshot of a person inside a committee. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| personnel | Personnel | Link | 1 |  | Navy Personnel | Link -> Navy Personnel | Reference to Navy Personnel. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| committee | Committee | Link | 1 |  | Personnel Committee | Link -> Personnel Committee | Reference to Personnel Committee. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| section_break_mxpq |  | Section Break | 0 |  |  |  | UI section separator; stores no business value. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| rank | Rank | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| committee_name_value | Name | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| category | Category | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| age | Age | Float | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| service_year_number | Service Year number | Float | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| weapon | Weapon | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| job | Job | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| military_number | Military Number | Data | 1 |  |  |  | Primary business identity for one person. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| unit | Unit | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| section_break_soue |  | Section Break | 0 |  |  |  | UI section separator; stores no business value. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| report_1 | Report 1 | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| report_2 | Report 2 | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
| report_3 | Report 3 | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | navy_personnel.py normalize_committee_records(); personnel_sync.py; importer upsert_committee_record() |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Conflict Option
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_conflict_option/personnel_conflict_option.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Child row storing one source option for a conflict. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| option | Option | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py marks selected |  |
| value | Value | Long Text | 1 |  |  |  | JSON/text representation of conflict option values. | deduplication.py create_conflict(); conflict_resolution.py marks selected |  |
| source_committee | Source Committee | Link | 1 |  | Personnel Committee | Link -> Personnel Committee | Reference to Personnel Committee. | deduplication.py create_conflict(); conflict_resolution.py marks selected |  |
| selected | Selected | Check | 0 | 0 |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py marks selected |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Data Conflict
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_data_conflict/personnel_data_conflict.json |
| Module | Personnel Management |
| Type | Standalone DocType |
| Is Child Table | 0 |
| Naming / autoname | CONF-.### |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Standalone conflict document created when deterministic import rules find conflicting history data. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| personnel | Personnel | Link | 1 |  | Navy Personnel | Link -> Navy Personnel | Reference to Navy Personnel. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| military_number | Military Number | Data | 1 |  |  |  | Primary business identity for one person. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| conflict_type | Conflict Type | Data | 1 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| status | Status | Select | 1 |  | Unresolved<br>Resolved |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| description | Description | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| selected_option | Selected Option | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| resolution_notes | Resolution Notes | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| resolved_by | Resolved By  | Link | 0 |  | User | Link -> User | Reference to User. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| resolved_on | Resolved On | Datetime | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| field_or_record | Filed / Record | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
| conflict_options | Conflict Options | Table | 0 |  | Personnel Conflict Option | Table -> Personnel Conflict Option | Child table storing Personnel Conflict Option rows. | deduplication.py create_conflict(); conflict_resolution.py resolve_conflict() |  |
### Permission Rules
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
## Personnel Detention
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_detention/personnel_detention.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Detention history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| place | Place | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| start_date | Start Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| cause | Cause | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| duration | Duration | Int | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Imprisonment
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_imprisonment/personnel_imprisonment.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Imprisonment history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| place | Place | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| start_date | Start Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| cause | Cause | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| duration | Duration | Int | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Measurement
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_measurement/personnel_measurement.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Height/weight measurement history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| height | Height | Float | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| height_date | Height Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| weight | Weight | Float | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| weight_date | Weight Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Medical Committee
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_medical_committee/personnel_medical_committee.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Medical committee history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| committee_type | Committee Type | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| diagnosis | Diagnosis | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| decision | Decision | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| committee_date | Committee Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Military Court
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_military_court/personnel_military_court.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Military court history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| place | Place | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| date | Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| cause | Cause | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| duration | Duration | Int | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Promotion
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_promotion/personnel_promotion.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Promotion history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| promotion_date | Promotion Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel punishment
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_punishment/personnel_punishment.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Punishment history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| type | Type | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| date | Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| cause | Cause | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| data_zhgc | Place | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Record Source
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_record_source/personnel_record_source.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Child-table provenance row linking imported records to a committee source. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| committee | Committee | Link | 1 |  | Personnel Committee | Link -> Personnel Committee | Reference to Personnel Committee. | excel_importer.py add_record_source() |  |
| record_type | Record Type | Data | 1 |  |  |  | DocType of the sourced record. | excel_importer.py add_record_source() |  |
| record_name | Record Name | Data | 1 |  |  |  | Actual child row name referenced by provenance. | excel_importer.py add_record_source() |  |
| record_display | Record | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. | excel_importer.py add_record_source() |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Travel
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_travel/personnel_travel.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Travel history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| place | Place | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| travel_date | Travel Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| return_date | Return Date | Date | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
| cause | Cause | Small Text | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.

## Personnel Unit History
| Property | Value |
| --- | --- |
| Source file | personnel_management/personnel_management/doctype/personnel_unit_history/personnel_unit_history.json |
| Module | Personnel Management |
| Type | Child Table |
| Is Child Table | 1 |
| Naming / autoname | Standard child/table naming |
| Title field | Not specified |
| Is Submittable | 0 |
| Track Changes | 0 |
| Purpose | Unit history child row. |
| Field | Label | Field Type | Required | Default | Options | Linked DocType / Storage | Description / Usage | Controlled By | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unit | Unit | Data | 0 |  |  |  | Field meaning inferred from label and usage; no separate field description in source. |  |  |
### Permission Rules

No independent permission rows in this DocType JSON. For child tables, permissions are inherited through the parent document.


