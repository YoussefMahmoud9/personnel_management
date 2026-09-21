# Complete System Guide

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## What Is This System?

Personnel Management is a custom Frappe/ERPNext application for managing Egyptian Navy personnel information. It stores one authoritative master record for each person, imports structured Excel workbooks attached to committees, preserves historical records, tracks source/provenance, detects deterministic duplicates and conflicts, resolves conflicts manually, and exports personnel data back to Excel.

## What Problem It Solves

The app centralizes personnel information that may arrive repeatedly from committee workbooks. Without a master system, repeated imports can create duplicate people, duplicate history rows, and uncertainty about which source is correct. This app uses `military_number` as the identity key and stores current data, historical data, source evidence, and conflicts in connected Frappe records.

## Who Uses It

- View-only users inspect personnel, reports, and allowed records.
- Editors maintain Navy Personnel records and export/import where permitted.
- Admin users create committees, validate/import workbooks, and review conflicts.
- System Managers maintain DocTypes, roles, permissions, and app configuration.

## Core Concepts

| Concept | Meaning in this app | Why it exists |
| --- | --- | --- |
| Personnel record | One `Navy Personnel` master document representing one real person. | Provides a single authoritative current record. |
| Military number | Business identity stored in `military_number` and used as `Navy Personnel` autoname. | Prevents fuzzy matching and identifies one real person. |
| Committee | A `Personnel Committee` document with a name and optional Excel attachment. | Gives imports and membership a committee context. |
| Committee Record | A `Personnel Committee Record` child row under Navy Personnel. | Stores the current-data snapshot for one person inside one committee. |
| Historical records | Child rows such as detentions, promotions, travel, measurements, courts. | Preserves time/event history separately from current master fields. |
| Record Source | A `Personnel Record Source` child row. | Links an imported child row to the originating committee. |
| Conflict | A `Personnel Data Conflict` document with `Personnel Conflict Option` rows. | Preserves competing source values for manual review. |
| Deduplication | Deterministic comparisons in `services/deduplication.py`. | Avoids repeated rows while keeping real distinct events. |


## Complete Lifecycle

```text
Excel Workbook
    ↓
Validation
    ↓
Committee
    ↓
Import
    ↓
Master Personnel
    ↓
Historical Records
    ↓
Record Sources
    ↓
Deduplication / Conflict Detection
    ↓
Conflict Center
    ↓
Manual Resolution
    ↓
Current Master Data
    ↓
Committee Views
    ↓
Reports / Dashboard / Export
```

### 1. Excel Workbook

The workbook is attached to `Personnel Committee.excel_file`. The importer reads that attachment only. There is no current hardcoded workbook fallback in the source.

### 2. Validation

`validate_committee_workbook(committee_name)` loads the workbook, checks required sheets, checks required columns, and returns a summary. It does not create or update personnel/history/conflict data.

### 3. Committee

The committee document supplies the import context. Source records and committee membership reference this committee.

### 4. Import

`import_personnel_data(committee_name)` reads workbook sheets, builds a military-number index from `details`, creates or updates Navy Personnel, upserts committee records, imports histories, records sources, and creates/reuses conflicts.

### 5. Master Personnel

`Navy Personnel` is authoritative for current values such as name, rank, unit, job, reports, age, and service years.

### 6. Historical Records

Historical data is stored as child rows under Navy Personnel. Child tables inherit parent behavior and are saved with the parent document.

### 7. Record Sources

After a child row has a valid generated `name`, the importer adds a `Personnel Record Source` row pointing to that child row and committee.

### 8. Deduplication And Conflict Detection

For supported histories, `deduplication.py` decides duplicate, conflict, or new. Duplicates add provenance to existing rows. Conflicts create/reuse `Personnel Data Conflict`.

### 9. Conflict Center

The custom page `personnel_conflict_c` lists unresolved conflicts and routes users to the conflict form.

### 10. Manual Resolution

Conflict form buttons call `resolve_conflict()`, update the matching child row with the selected option, mark the conflict resolved, and preserve conflict options.

### 11. Current Master Data And Committee Views

Master updates trigger `personnel_sync.sync_committee_records`, keeping committee records aligned with current authoritative master fields.

### 12. Reports / Dashboard / Export

The app source contains one Query Report: `Personnel by Unit`.

The site database also contains private user-specific Workspace pages for Statistics and category dashboards. These include number cards, quick lists, and Dashboard Chart records for personnel, detentions, military courts, imprisonments, travel, and medical committees. See [Dashboards, Reports, And Statistics](DASHBOARDS_REPORTS_AND_STATISTICS.md).

## Possible Alternatives — Not Current Implementation

- Separate standalone history DocTypes instead of child tables. Current implementation uses child tables under Navy Personnel, so history rows save with the parent and use child `parent`, `parenttype`, and `parentfield`.
- Fuzzy matching by names. Current implementation does not do this; military number is required.
- Import preview with rollback. Current source implements workbook validation, not a full transactional dry-run preview.
