# Administrator Guide

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Administrator Responsibilities

- Maintain users and roles.
- Create committees.
- Attach and validate workbooks.
- Run imports only when intended.
- Review conflicts.
- Maintain reference masters.
- Run migrations/cache/build commands after updates.
- Protect production data with backups and read-only audits.

## Users And Roles

Use Frappe's User and Role tools. This app defines/uses these roles in DocType/Page/Report metadata:

- `Navy Personnel User`
- `Navy Personnel Editor`
- `Navy Personnel Admin`
- `System Manager`

See [Permissions And Roles Reference](PERMISSIONS_AND_ROLES_REFERENCE.md).

## Creating Committees

1. Open `Personnel Committee`.
2. Create a record with `committee_name`.
3. Attach workbook to `excel_file`.
4. Save.

## Safe Import Procedure

1. Confirm backup exists.
2. Open committee.
3. Validate workbook.
4. Only import after validation.
5. Review summary.
6. Resolve conflicts.
7. Run read-only audit if needed.

## Dangerous Operations

- Full import: creates/updates data.
- Manual SQL updates/deletes: bypass Frappe document rules.
- Child-row cleanup: must also handle record sources.
- Permission changes: can expose sensitive personnel data.

## Safe Operations

- Workbook validation.
- Read-only reports.
- Read-only audit SQL.
- Export.
- Cache clear/build/restart.

## Backups

Use standard bench backup commands for the site before high-risk operations. Exact backup policy is environment-specific and not defined in this app source.

## Maintenance Commands Verified In This Environment

```bash
cd <bench-path>
bench --site <site-name> migrate
bench --site <site-name> clear-cache
bench restart
bench build --app personnel_management
```

## Testing After Updates

- Python: `python3 -m py_compile <file.py>`
- JS: `node --check <file.js>`
- Validate workbook without importing.
- Open key pages/forms.
- Verify permissions with test users where available.

## Cleanup Policy

Only clean records with an explicit rule. For duplicate child rows, keep one row and delete only the source rows that reference deleted child row names. Do not delete resolved conflicts unless explicitly approved.
