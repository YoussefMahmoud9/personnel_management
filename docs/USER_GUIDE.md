# User Guide

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Before You Start

You need a Frappe user account and a role that allows the action you want. If a button or page is missing, your role may not have access or the browser may need cache clearing after an update.

## Workflow: Find Personnel

**Goal:** Find and open a person.

**Before you start:** Know at least one search value such as military number, name, unit, rank, or committee.

1. Open `Navy Personnel` from search/workspace.
2. Use the list search or filters.
3. Use the custom committee filter if you need people in one committee.
4. Click a row to open the record.

**Expected result:** The person's master form opens.

**Common mistakes:** Searching by committee using a normal field filter will not work unless using the custom committee control; committee membership is stored in a child table.

**What not to do:** Do not create a second person for the same military number.

## Workflow: View A Personnel Record

**Goal:** Understand one person.

1. Open the Navy Personnel record.
2. Review current fields: full name, rank, category, unit, weapon, job, reports.
3. Review historical tables: promotions, measurements, medical committees, unit history, travel, punishments, detentions, imprisonments, military courts.
4. Review committee records to see committee membership.
5. Review record sources to see provenance where present.

**Expected result:** You can distinguish current data from history and provenance.

## Workflow: Edit A Personnel Record

**Goal:** Correct current master data.

1. Open the Navy Personnel record.
2. Edit allowed fields.
3. If changing `birth_date`, `age` recalculates.
4. If changing `high_salary_date`, `service_year_number` recalculates.
5. Save.

**Expected result:** Master values save and the sync hook updates committee records.

**What not to do:** Do not manually edit child rows to force a conflict resolution; use the conflict workflow where applicable.

## Workflow: Upload Photos

**Goal:** Attach a personnel or family image.

1. Open Navy Personnel.
2. Use `image` for personnel photo or `family_photo` for family photo.
3. Upload an image.
4. Save the record.

**Expected result:** Server code stores the file using the military number.

**Common mistakes:** Uploading before a valid military number exists can prevent normalization.

## Workflow: Create A Committee

**Goal:** Create an import committee.

1. Open `Personnel Committee`.
2. Click New.
3. Enter `committee_name`.
4. Attach an Excel file to `excel_file` if importing.
5. Save.

**Expected result:** Committee can be validated/imported.

## Workflow: Validate Workbook

**Goal:** Check workbook without changing data.

1. Open a saved Personnel Committee.
2. Confirm `excel_file` is attached.
3. Click `Validate Workbook`.
4. Review the validation summary.

**Expected result:** Validation result appears. No personnel/history/conflict records are modified.

## Workflow: Import Workbook

**Goal:** Commit workbook data into the app.

1. Validate workbook first.
2. Click `Import Workbook`.
3. Wait for completion.
4. Read the import summary.
5. Open Conflict Center if conflicts were created.

**Expected result:** Personnel, committee records, history, sources, and conflicts are updated according to importer logic.

**Danger:** Import modifies production data. Do not use it as a test.

## Workflow: Resolve Conflict

1. Open Conflict Center.
2. Click `Review` for an unresolved conflict.
3. On the Personnel Data Conflict form, click `Resolve with Option 1` or `Resolve with Option 2`.
4. Enter optional resolution notes.
5. Confirm.

**Expected result:** Matching historical row is updated and conflict becomes Resolved.

## Workflow: Export

1. Open `/app/personnel_export-1`.
2. Choose Export Mode: all, committee, or selected.
3. If committee, select a committee.
4. If selected, search/filter/select personnel.
5. Click `Export to Excel`.

**Expected result:** Browser downloads `personnel_export.xlsx`.

## Reports, Statistics, And Dashboards

The app source contains Query Report `Personnel by Unit`.

The site also has private dashboard/statistics pages for a site user:

- `Statistics`
- `Personnel Charts & Dashboard`
- `Detentions Charts & Dashboards`
- `Military Courts Charts & Dashboards`
- `Imprisonments Charts & Dashboards`
- `Travel Charts & Dashboards`
- `Medical Committees Charts & Dashboards`

Use these pages to view counts and charts by unit/rank for personnel and history categories. See [Dashboards, Reports, And Statistics](DASHBOARDS_REPORTS_AND_STATISTICS.md).
