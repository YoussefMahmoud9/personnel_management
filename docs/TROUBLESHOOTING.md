# Troubleshooting

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Import Fails: Personnel Committee is required

**Possible cause:** Import/validation called without `committee_name`.
**Verify:** Check the button call or server method arguments.
**Solution:** Open a saved Personnel Committee and use its buttons.
**Expected result:** The method receives committee name.

## Import Fails: Excel file not found

**Possible cause:** `excel_file` points to a missing file or bad File URL.
**Verify:** Open committee and File record.
**Solution:** Attach the correct workbook again.

## Validation Reports Missing Sheet Or Column

**Possible cause:** Workbook does not contain required sheet/column names.
**Verify:** Compare against [Import Export Detailed Guide](IMPORT_EXPORT_DETAILED_GUIDE.md).
**Solution:** Correct workbook structure.

## Rows Are Unmatched

**Possible cause:** Military number missing/invalid or not present in `details`; mapper rejected required value.
**Verify:** Validation mapping summary.
**Solution:** Fix source workbook or add the person to `details`.

## Duplicate Records Appear

**Possible cause:** Older imports before a dedup rule, missing identity fields, or a history type where only exact duplicates are recognized.
**Verify:** Read-only duplicate audit by current rules.
**Solution:** Use explicit cleanup rule; do not manually delete without preserving record-source logic.

## Conflict Appears

**Possible cause:** Incoming history has same deterministic identity but different conflict fields.
**Verify:** Open Personnel Data Conflict and compare options.
**Solution:** Resolve with the correct option.

## Conflict Resolution Says History Record Could Not Be Found

**Possible cause:** Target child row no longer exists or option identity no longer matches after manual edits.
**Verify:** Check child table row identity fields and conflict option JSON.
**Solution:** Developer/admin investigation required.

## Photo Does Not Appear

**Possible cause:** Missing file, invalid extension, bad path, no military number, or browser cache.
**Verify:** Check field value and public file path.
**Solution:** Re-upload valid image and save.

## Permission Denied

**Possible cause:** Role lacks DocType/Page permission.
**Verify:** See [Permissions And Roles Reference](PERMISSIONS_AND_ROLES_REFERENCE.md).
**Solution:** Assign correct role or adjust permission intentionally.

## Page Unavailable

**Possible cause:** Page role restriction or cache/build issue.
**Verify:** Page JSON roles and browser console.
**Solution:** clear-cache, build assets if JS changed, verify role.

## Translation Not Changing

**Possible cause:** User language not changed, cache, missing translation string.
**Verify:** Check user language and `translations/ar.csv`.
**Solution:** Use language toggle, reload, clear cache/build if needed.

## Browser Still Shows Old JS

**Solution:**

```bash
bench build --app personnel_management
bench --site <site-name> clear-cache
bench restart
```

Then hard refresh browser.
