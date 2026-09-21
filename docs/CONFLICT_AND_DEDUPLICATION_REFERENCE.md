# Conflict And Deduplication Reference

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Source Files

- `personnel_management/services/deduplication.py`
- `personnel_management/services/conflict_resolution.py`
- Import caller: `personnel_management/importers/excel_importer.py`

## Implemented Rules

| Record Type | Identity Key | Duplicate Condition | Conflict Condition | Missing/Distinct Behavior |
| --- | --- | --- | --- | --- |
| Detentions | start_date + place | same identity + same cause | same identity + different cause | missing identity => distinct; duration not identity |
| Imprisonments | start_date + place | same identity + same cause | same identity + different cause | same as detentions |
| Punishments | date + data_zhgc + type | same identity + same cause | same identity + different cause | missing identity => distinct |
| Medical Committees | committee_date + committee_type | same identity + same diagnosis + same decision | same identity + different diagnosis or decision | missing identity => distinct |
| Promotions | promotion_date | same promotion_date | none implemented | different date => distinct |
| Travel | travel_date + return_date + place | same identity + same cause | same identity + different cause | missing identity => distinct |
| Height | height_date | same date + same height | same date + different height | different date => distinct |
| Weight | weight_date | same date + same weight | same date + different weight | different date => distinct |
| Unit History | unit | same non-empty unit | none implemented | different unit => distinct |
| Military Courts | place + date + cause + duration | fully identical non-empty row | none implemented | any difference => distinct |


## What Happens To Duplicates

The importer does not append a duplicate child row. It finds the existing child row and calls `add_record_source()` so provenance for the duplicate source committee is preserved.

## What Happens To Conflicts

`create_conflict()` creates a `Personnel Data Conflict` with two `Personnel Conflict Option` child rows unless `existing_equivalent_conflict()` finds an equivalent resolved or unresolved conflict.

## How Conflicts Are Resolved

`resolve_conflict()` parses the chosen option, finds the matching child row using normalized exact matching or `same_identity()`, writes selected values into that child row, marks the selected option, and changes conflict status to `Resolved`.

## Not Implemented / Unknown

- Fuzzy matching is not implemented.
- Conflict rules for Unit History are not implemented; only duplicate detection by same non-empty unit exists.
- Conflict rules for Military Courts are not implemented; only fully identical duplicate detection exists.
