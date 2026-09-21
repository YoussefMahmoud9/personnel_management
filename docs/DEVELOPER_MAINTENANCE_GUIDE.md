# Developer Maintenance Guide

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Safe Modification Strategy

1. Inspect current DocType JSON and code before editing.
2. Make the smallest focused change.
3. Do not rewrite importer/dedup logic casually.
4. Run syntax checks for modified files.
5. Use validation, read-only audits, and browser checks.
6. Avoid direct SQL writes unless there is no safe Frappe API route.

## Commands

```bash
python3 -m py_compile path/to/file.py
node --check path/to/file.js
bench --site <site-name> migrate
bench --site <site-name> clear-cache
bench build --app personnel_management
bench restart
```

## What Not To Edit Manually

- Production Excel source files unless explicitly required.
- Database rows through SQL for normal business edits.
- Generated child row names.
- Record source references without matching child-row cleanup.
- Resolved conflicts unless explicitly approved.

## Common Change Areas

| Area | Files | Checks |
| --- | --- | --- |
| Form behavior | doctype JS files | node --check and browser form test |
| Server validation | DocType Python controller | py_compile and save test |
| Importer | excel_importer.py, deduplication.py | py_compile and workbook validation; do not run real import as casual test |
| Export | exporter.py, export page JS | py_compile, node --check, export download test |
| Permissions | DocType/Page/Report JSON | migrate, cache clear, role test |
| Translations | translations/ar.csv, public JS | build/cache clear/hard refresh |


## Maintenance Risks

- Changing military number logic can break identity.
- Changing child-table fields can break importer/exporter mappings.
- Changing conflict identity rules can create duplicate or missing conflicts.
- Photo changes can orphan File records or public files.
