# Data Model And Relationships

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Master Model

```text
Navy Personnel
 ├── Promotions              -> Personnel Promotion child rows
 ├── Measurements            -> Personnel Measurement child rows
 ├── Medical Committees      -> Personnel Medical Committee child rows
 ├── Unit History            -> Personnel Unit History child rows
 ├── Travel History          -> Personnel Travel child rows
 ├── Punishments             -> Personnel punishment child rows
 ├── Detentions              -> Personnel Detention child rows
 ├── Imprisonments           -> Personnel Imprisonment child rows
 ├── Military Courts         -> Personnel Military Court child rows
 ├── Committee Records       -> Personnel Committee Record child rows
 └── Record Sources          -> Personnel Record Source child rows
```

## Relationship Table

| From | Field | Relationship |
| --- | --- | --- |
| Navy Personnel | promotions | Table -> Personnel Promotion |
| Navy Personnel | measurements | Table -> Personnel Measurement |
| Navy Personnel | medical_committees | Table -> Personnel Medical Committee |
| Navy Personnel | unit_history | Table -> Personnel Unit History |
| Navy Personnel | travel_history | Table -> Personnel Travel |
| Navy Personnel | punishments | Table -> Personnel punishment |
| Navy Personnel | detentions | Table -> Personnel Detention |
| Navy Personnel | imprisonments | Table -> Personnel Imprisonment |
| Navy Personnel | military_courts | Table -> Personnel Military Court |
| Navy Personnel | committee_records | Table -> Personnel Committee Record |
| Navy Personnel | record_sources | Table -> Personnel Record Source |
| Personnel Committee Record | personnel | Link -> Navy Personnel |
| Personnel Committee Record | committee | Link -> Personnel Committee |
| Personnel Data Conflict | personnel | Link -> Navy Personnel |
| Personnel Data Conflict | conflict_options | Table -> Personnel Conflict Option |
| Personnel Conflict Option | source_committee | Link -> Personnel Committee |
| Personnel Record Source | committee | Link -> Personnel Committee |


## Frappe Child Table Mechanics

Every child row has Frappe system fields such as `parent`, `parenttype`, `parentfield`, `idx`, and `name`. They are not listed in every child DocType JSON field list, but Frappe uses them to store rows inside the parent document.

- `parent`: name of the parent Navy Personnel or conflict document.
- `parenttype`: parent DocType.
- `parentfield`: fieldname of the Table field on the parent.
- `idx`: row order in the child table.
- `name`: generated unique child row identifier.

## Text ER Diagram

```text
Personnel Committee <---- Personnel Committee Record ----> Navy Personnel
        ^                                                  |
        |                                                  | child tables
        |                                                  v
Personnel Record Source ---- record_type/record_name ---> History Child Row

Navy Personnel <---- Personnel Data Conflict ---- Personnel Conflict Option
                                              |
                                              v
                                      source_committee -> Personnel Committee
```

## Provenance

`Personnel Record Source` does not link through a Frappe Link field to every possible child DocType. Instead it stores `record_type` and `record_name` as data fields. This lets one table refer to many child DocTypes. The importer only creates source rows after a child row has a valid generated `name`.

## Current Identity

The master identity is `Navy Personnel.military_number`, and the DocType uses `autoname = field:military_number`. Import matching uses the cleaned military number from Excel.
