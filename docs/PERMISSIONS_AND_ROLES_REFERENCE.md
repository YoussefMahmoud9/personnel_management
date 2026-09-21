# Permissions And Roles Reference

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## User Levels

| Business Level | Frappe Role | Purpose |
| --- | --- | --- |
| User 1 | Navy Personnel User | View-only personnel/report access where configured. |
| User 2 | Navy Personnel Editor | View/edit people, import/export according to DocType permissions. |
| User 3 | Navy Personnel Admin | Editor capabilities plus committee administration and Conflict Center page access. |
| User 4 | System Manager | System-level administration and customization. |


## Feature Matrix

| Feature | User 1 | User 2 | User 3 | User 4 |
| --- | --- | --- | --- | --- |
| Read Navy Personnel | ✅ | ✅ | ✅ | ✅ |
| Write Navy Personnel | ❌ | ✅ | ✅ | ✅ |
| Create Navy Personnel | ❌ | ✅ | ✅ | ✅ |
| Delete Navy Personnel | ❌ | ✅ | ❌ | ✅ |
| Import Navy Personnel | ❌ | ✅ | ✅ | ✅ |
| Export Navy Personnel | ❌ | ✅ | ✅ | ✅ |
| Read Personnel Committee | ✅ | ✅ | ✅ | ✅ |
| Write/Create Personnel Committee | ❌ | ❌ | ✅ | ✅ |
| Delete Personnel Committee | ❌ | ❌ | ❌ | ✅ |
| Personnel Export page personnel_export-1 | ❌ | ✅ | ✅ | ✅ |
| Conflict Center page | ❌ | ❌ | ✅ | ✅ |
| Customize DocTypes/fields | ❌ | ❌ | ❌ | ✅ via System Manager/Frappe |


## Page Permissions

| Page | Title | Roles In Page JSON | Source |
| --- | --- | --- | --- |
| personnel_conflict_c | Personnel Conflict Center | Navy Personnel Admin, System Manager | personnel_management/personnel_management/page/personnel_conflict_c/personnel_conflict_c.json |
| personnel_export | Personnel Export | No roles in Page JSON | personnel_management/personnel_management/page/personnel_export/personnel_export.json |
| personnel_export-1 | Personnel Export | Navy Personnel Editor, Navy Personnel Admin, System Manager | personnel_management/personnel_management/page/personnel_export_1/personnel_export_1.json |


## Report Permissions

| Report | Type | Roles | Query |
| --- | --- | --- | --- |
| Personnel by Unit | Query Report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor | SELECT <br>    unit AS "Unit", <br>    COUNT(*) AS "Personnel Count" <br>FROM `tabNavy Personnel` <br>WHERE unit IS NOT NULL AND unit != '' <br>GROUP BY unit <br>ORDER BY COUNT(*) DESC |


## DocType Permission Rules

## Navy Job
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
## Navy Personnel
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 0 |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
## Navy Rank
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
## Navy Unit
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
## Navy Weapon
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
## Personnel Committee
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Navy Personnel User | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Editor | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Navy Personnel Admin | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
## Personnel Data Conflict
| Role | read | write | create | delete | submit | cancel | amend | report | export | import | share | print | email |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Navy Personnel User | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Navy Personnel Editor | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Navy Personnel Admin | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| System Manager | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |


## Important Frappe Behavior

- Child table DocTypes normally do not have independent permissions; access is controlled through the parent document.
- Page role lists restrict page access, but backend whitelisted functions may still require separate permission logic if added.
- `System Manager` often has broader Frappe platform access beyond this app's JSON files.
