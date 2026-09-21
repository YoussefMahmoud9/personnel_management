# Data And Import Specification

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Import Pipeline

```text
Excel
↓
Workbook loading
↓
Validation
↓
Sheet mapping
↓
Military number normalization
↓
Master matching
↓
Create/update master
↓
Committee record
↓
History insertion
↓
Deduplication
↓
Conflict detection
↓
Record Source
↓
Synchronization
```

## Workbook Loading

Implemented in `personnel_management/importers/excel_importer.py`. `load_workbook(excel_file=None)` resolves the committee file path through Frappe file handling. `get_committee(committee_name)` loads the committee by `committee_name`.

## Expected Sheets And Columns

### details

Required columns: `name`, `rakm3askry`, `sela7`, `taqreer1`, `taqreer2`, `taqreer3`, `tab3ya`, `taree5_sarf_ratb_3aly`, `taree5_tareeqy_waited`, `address`, `darga`, `fe2a`, `wazefa`, `servcice_year_number`, `birthday`, `taree5_ttawo3`, `age`, `halaa_egtma3ya`, `image_path`

### taree5_tarqy_darga

Required columns: `taree5tarqydarga`, `rakm3askry`

### h7alaagtma3ya

Required columns: `h7alaagtma3yaid`, `h7alaagtma3ya`, `numberofgirls`, `namesofgirls`, `numberofboys`, `namesofboys`, `rakm3askry`

### waheda

Required columns: `waheda`, `rakm3askry`

### lagnatbya

Required columns: `no3ellegna`, `tash5ees`, `qrar`, `rakm3askry`, `dateoflagna`

### safr

Required columns: `place`, `dateoftravel`, `dateofreturn`, `causeoftravel`, `rakm3askry`

### height

Required columns: `height`, `rakm3askry`, `dateofheight`

### weight

Required columns: `weight`, `rakm3askry`, `dateofweight`

### k3obat

Required columns: `typeof3koaba`, `dateof3koba`, `causeof3koba`, `palceof3koba`, `rakm3askry`

### h7agz

Required columns: `rakm3askry`, `placeof7agz`, `dateof7agz`, `timeof7agz`, `causeof7agz`

### h7abs

Required columns: `rakm3askry`, `placeof7abzs`, `dateof7abs`, `timeof7abs`, `causeof7abs`

### ma7kma

Required columns: `rakm3askry`, `placeofma7kma`, `dateofma7kma`, `timeofma7kma`, `causeofma7kma`


## Column Mapping

| Sheet | Target | Actual mapping / notes |
| --- | --- | --- |
| details | Navy Personnel | rakm3askry -> military_number; name -> full_name; birthday -> birth_date; image_path -> image; sela7 -> weapon; tab3ya -> unit; darga -> rank; fe2a -> category; wazefa -> job; taree5_sarf_ratb_3aly -> high_salary_date; taree5_tareeqy_waited -> promotion_promise_date; taree5_ttawo3 -> volunteer_date; halaa_egtma3ya -> social_status; reports and address mapped directly |
| taree5_tarqy_darga | Personnel Promotion | taree5tarqydarga -> promotion_date; rakm3askry -> military_number |
| h7alaagtma3ya | Navy Personnel family fields | h7alaagtma3ya -> social_status; numberofgirls -> number_of_girls; namesofgirls -> names_of_girls; numberofboys -> number_of_boys; namesofboys -> names_of_boys |
| waheda | Personnel Unit History | waheda -> unit; rakm3askry -> military_number |
| lagnatbya | Personnel Medical Committee | no3ellegna -> committee_type; tash5ees -> diagnosis; qrar -> decision; dateoflagna -> committee_date |
| safr | Personnel Travel | place -> place; dateoftravel -> travel_date; dateofreturn -> return_date; causeoftravel -> cause |
| height | Personnel Measurement | height -> height; dateofheight -> height_date |
| weight | Personnel Measurement | weight -> weight; dateofweight -> weight_date |
| k3obat | Personnel punishment | typeof3koaba -> type; dateof3koba -> date; causeof3koba -> cause; palceof3koba -> data_zhgc |
| h7agz | Personnel Detention | placeof7agz -> place; dateof7agz -> start_date; causeof7agz -> cause; timeof7agz -> duration |
| h7abs | Personnel Imprisonment | placeof7abzs -> place; dateof7abs -> start_date; causeof7abs -> cause; timeof7abs -> duration |
| ma7kma | Personnel Military Court | placeofma7abs -> place in code, but EXPECTED_COLUMNS requires placeofma7kma. Status: implementation conflict; actual mapper uses placeofma7abs, validation expects placeofma7kma. dateofma7kma -> date; causeofma7abs -> cause; timeofma7abs -> duration |


## What Mapped / Unmatched Means

- Mapped: row was converted to target fields and has a valid military number present in the authoritative `details` sheet.
- Unmatched: row was skipped because the military number is missing, invalid, or absent from the `details` index, or because the mapper rejected a required value such as empty unit/height/weight.

## Validation Passed

Validation passed means required sheets and required columns exist and row-level mapping summary could be computed. It does not mean import was run.

## Import Stops Versus Continues

- Missing required sheet/column raises an error and stops validation/import.
- Unmatched rows are counted and skipped.
- Duplicate history rows are not appended; source may be added to existing row.
- Conflicts are recorded and import continues.

## Export Behavior

Export is implemented in `personnel_management/services/exporter.py`. The output filename is `personnel_export.xlsx`.

Export modes are controlled by `/app/personnel_export-1`:

- All personnel: no filter.
- Committee: `committee_name` filters through `Personnel Committee Record`.
- Selected: sends JSON list of military numbers.

Export sheets mirror the workbook sheet names:

| Sheet | Generated By |
| --- | --- |
| details | exporter.py row builder |
| taree5_tarqy_darga | exporter.py row builder |
| h7alaagtma3ya | exporter.py row builder |
| waheda | exporter.py row builder |
| lagnatbya | exporter.py row builder |
| safr | exporter.py row builder |
| height | exporter.py row builder |
| weight | exporter.py row builder |
| k3obat | exporter.py row builder |
| h7agz | exporter.py row builder |
| h7abs | exporter.py row builder |
| ma7kma | exporter.py row builder |


## Implementation Conflict Found

`EXPECTED_COLUMNS['ma7kma']` requires `placeofma7kma`, but `map_military_court_row()` reads `placeofma7abs`. Actual implementation takes precedence at runtime; validation and mapping may disagree for the military court place column.
