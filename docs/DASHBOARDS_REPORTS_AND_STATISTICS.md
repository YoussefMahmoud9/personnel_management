# Dashboards, Reports, And Statistics

> Truth Mode: This document describes the actual current dashboard/statistics/report configuration inspected read-only from `<site-name>`, plus the related source files in `apps/personnel_management`. Do not treat the current chart numbers shown in the UI as fixed documentation values; they change when the database changes.

## Source Versus Site Configuration

### Application Source

The repository contains:

| Repository definition type | Count | Location |
| --- | ---: | --- |
| Dashboard / Workspace JSON | 0 | No Workspace JSON files in the app source |
| Dashboard Chart JSON | 0 | No Dashboard Chart JSON files in the app source |
| Number Card JSON | 0 | No Number Card JSON files in the app source |
| Query Report JSON | 1 | `personnel_management/personnel_management/report/personnel_by_unit/personnel_by_unit.json` |

### Site-Level Configuration

The site database `<site-name>` contains:

| Site-level record type | Count inspected | Storage |
| --- | ---: | --- |
| Private Workspace dashboard/statistics pages | 7 | `tabWorkspace` |
| Dashboard Chart records used by these pages | 12 | `tabDashboard Chart` |
| Number Cards used by Statistics | 3 | `tabNumber Card` |
| Query Reports used by dashboard charts | 12 | `tabReport` plus `tabHas Role` |

Why this matters: a developer cloning only the app repository receives the committed source files, but these private site-created Workspace, Dashboard Chart, and Number Card records are stored in `<site-name>` database metadata. They are not currently exported as app JSON fixtures in this repository.

## Dashboard Index

| Dashboard | Route | Purpose | Charts / Cards | Access |
| --- | --- | --- | ---: | --- |
| Statistics | private workspace route | High-level counts and quick lists | 3 number cards, 3 quick lists | Private user-specific Workspace |
| Personnel Charts & Dashboard | private workspace route | Personnel distribution by unit/rank | 2 charts | Private user-specific Workspace |
| Detentions Charts & Dashboards | private workspace route | Detention record distribution by unit/rank | 2 charts | Private user-specific Workspace |
| Military Courts Charts & Dashboards | private workspace route | Military court record distribution by unit/rank | 2 charts | Private user-specific Workspace |
| Imprisonments Charts & Dashboards | private workspace route | Imprisonment record distribution by unit/rank | 2 charts | Private user-specific Workspace |
| Travel Charts & Dashboards | private workspace route | Travel record distribution by unit/rank | 2 charts | Private user-specific Workspace |
| Medical Committees Charts & Dashboards | private workspace route | Medical committee record distribution by unit/rank | 2 charts | Private user-specific Workspace |

## Access And Security

All seven dashboard pages are Workspace records with:

- `public = 0`
- `for_user = <private-user>`
- `owner = <private-user>`
- no app-source Workspace JSON definition

No Workspace role rows were verified for these private pages. Because the records are private for `Administrator`, role-level access for generic non-Administrator users is not established from the metadata.

| Dashboard | User 1: Navy Personnel User | User 2: Navy Personnel Editor | User 3: Navy Personnel Admin | User 4: System Manager |
| --- | --- | --- | --- | --- |
| Statistics | Not verified | Not verified | Not verified | Not verified |
| Personnel Charts & Dashboard | Not verified | Not verified | Not verified | Not verified |
| Detentions Charts & Dashboards | Not verified | Not verified | Not verified | Not verified |
| Military Courts Charts & Dashboards | Not verified | Not verified | Not verified | Not verified |
| Imprisonments Charts & Dashboards | Not verified | Not verified | Not verified | Not verified |
| Travel Charts & Dashboards | Not verified | Not verified | Not verified | Not verified |
| Medical Committees Charts & Dashboards | Not verified | Not verified | Not verified | Not verified |

For role permissions on the underlying DocTypes and reports, see [Permissions And Roles Reference](PERMISSIONS_AND_ROLES_REFERENCE.md).

## Dashboard Navigation

Open each dashboard directly through its private workspace route route or through the Frappe Desk private workspace UI if it is visible to the current user.

The dashboard pages are Frappe Workspace pages. Their content is stored as Workspace `content` JSON containing headers, charts, number cards, spacers, and quick-list references.

Documented interactions:

- Charts render as standard Frappe Dashboard Chart widgets.
- Labels and values refresh from the current database/report results when the workspace/chart is loaded.
- The documentation does not verify any custom click-through behavior from chart segments to records.
- No page-specific filters were found in the Workspace content for these dashboards.
- Dashboard Chart records have `filters_json = {}` for the inspected chart records.

## Statistics Page

### Metadata

| Property | Value |
| --- | --- |
| Workspace record | `Statistics-<private-user>` |
| Title | `Statistics` |
| Route | private workspace route |
| Public | `0` |
| For user | `Administrator` |
| Owner | `Administrator` |
| Created | `2026-09-17 13:18:42.140860` |
| Last modified | `2026-09-17 13:38:44.714396` |

### Purpose

The Statistics page gives a high-level entry point for personnel counts, committee counts, unresolved conflict counts, and quick lists for recent or active operational records.

### Statistics And Cards

| Statistic | Purpose | Value Represents | Source DocType | Calculation | Filter | Unique or Non-Unique | Refresh Behavior | Limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Total Personnel | Shows size of the personnel master list | Number of `Navy Personnel` documents | `Navy Personnel` | Count documents | none | Unique master personnel documents | Dynamic when card loads/refreshes | Counts master records, not committee memberships or history rows |
| Total Committees | Shows number of committee records | Number of `Personnel Committee` documents | `Personnel Committee` | Count documents | none | Unique committee documents | Dynamic when card loads/refreshes | Does not show active-only committees; no filter is configured |
| Unresolved Conflicts | Shows unresolved import conflicts | Number of `Personnel Data Conflict` documents with unresolved status | `Personnel Data Conflict` | Count documents | `status = Unresolved` | Unique conflict documents | Dynamic when card loads/refreshes | Does not count resolved conflicts |

### Quick Lists

Workspace content references these quick lists:

- `Recent Navy Personnel`
- `Active Personnel Committees`
- `Unresolved Conflicts`

Status: the quick-list names are verified in Workspace content. A table named `tabQuick List` was not present on this site during inspection, so the backing quick-list metadata was not separately verified.

## Personnel Charts & Dashboard

### Metadata

| Property | Value |
| --- | --- |
| Workspace record | `Personnel Charts & Dashboard -<private-user>` |
| Title | `Personnel Charts & Dashboard` |
| Route | private workspace route |
| Public | `0` |
| For user | `Administrator` |
| Owner | `Administrator` |
| Created | `2026-09-17 13:40:53.684122` |
| Last modified | `2026-09-17 15:09:18.098220` |

### Personnel by Unit

| Item | Value |
| --- | --- |
| Chart name | `Personnel by Unit` |
| Displayed title | `Personnel by Unit` |
| Chart type | Bar |
| Source | Report Dashboard Chart |
| Source report | `Personnel by Unit` |
| Source DocType | `Navy Personnel` |
| X-axis | `unit` / report column `Unit` |
| Y-axis | `Personnel Count` |
| Aggregation | `COUNT(*)` |
| Grouping | `GROUP BY unit` |
| Filters | unit is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: unique `Navy Personnel` master records grouped by their current `unit`.

What it tells you: the distribution of current personnel master records across units.

What it does not tell you: it does not count historical unit assignments from `Personnel Unit History`, committee membership, or repeated history rows.

### Personnel By Rank

| Item | Value |
| --- | --- |
| Chart name | `Personnel By Rank` |
| Displayed title | `Personnel By Rank` |
| Chart type | Bar |
| Source | Report Dashboard Chart |
| Source report | `Personnel by Rank` |
| Source DocType | `Navy Personnel` |
| X-axis | `rank` / report column `Rank` |
| Y-axis | `Personnel Count` |
| Aggregation | `COUNT(*)` |
| Grouping | `GROUP BY rank` |
| Filters | rank is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: unique `Navy Personnel` master records grouped by their current `rank`.

What it tells you: the distribution of current personnel master records across ranks.

What it does not tell you: it does not count promotions, history rows, or historical ranks.

## Detentions Charts & Dashboards

### Metadata

| Property | Value |
| --- | --- |
| Workspace record | `Detentions Charts & Dashboards-<private-user>` |
| Title | `Detentions Charts & Dashboards` |
| Route | private workspace route |
| Public | `0` |
| For user | `Administrator` |
| Owner | `Administrator` |
| Created | `2026-09-17 15:04:51.576429` |
| Last modified | `2026-09-17 15:18:41.189151` |

Important title note: the Workspace header text includes labels such as `Personnel by Unit` and `Personnel By Rank`, but the embedded chart records are `Detentions by Unit` and `Detentions By Rank`. The chart configuration is the authoritative source for what is counted.

### Detentions by Unit

| Item | Value |
| --- | --- |
| Chart name | `Detentions by Unit` |
| Chart type | Donut |
| Source report | `Detentions by Unit` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Detention` |
| X-axis | `unit` / report column `Unit` |
| Y-axis | `Detention Count` |
| Aggregation | `COUNT(pd.name)` |
| Grouping | `GROUP BY np.unit` |
| Filters | Navy Personnel unit is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: detention child records grouped by the current unit of the parent Navy Personnel record.

What it tells you: which current units have the most detention records attached to their personnel.

What it does not tell you: it does not necessarily show the number of unique personnel detained. One person can have multiple detention records, so that person can contribute multiple counts.

### Detentions By Rank

| Item | Value |
| --- | --- |
| Chart name | `Detentions By Rank` |
| Chart type | Donut |
| Source report | `Detentions by Rank` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Detention` |
| X-axis | `rank` / report column `Rank` |
| Y-axis | `Detention Count` |
| Aggregation | `COUNT(pd.name)` |
| Grouping | `GROUP BY np.rank` |
| Filters | Navy Personnel rank is not null and not empty |
| Roles on report | System Manager |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: detention child records grouped by the current rank of the parent Navy Personnel record.

What it tells you: distribution of detention records across current ranks.

What it does not tell you: it does not count unique personnel unless each person has exactly one detention record. It also uses current rank, not necessarily rank at the time of detention.

## Military Courts Charts & Dashboards

### Metadata

| Property | Value |
| --- | --- |
| Workspace record | `Military Courts Charts & Dashboards-<private-user>` |
| Title | `Military Courts Charts & Dashboards` |
| Route | private workspace route |
| Public | `0` |
| For user | `Administrator` |
| Owner | `Administrator` |
| Created | `2026-09-17 15:05:19.514262` |
| Last modified | `2026-09-17 15:25:20.241575` |

### Military Courts by Unit

| Item | Value |
| --- | --- |
| Chart name in Workspace | `Military Courts by Unit` |
| Dashboard Chart record | `Military Courts By Unit` |
| Chart type | Donut |
| Source report | `Military Courts by Unit` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Military Court` |
| X-axis | `unit` / report column `Unit` |
| Y-axis | `Court Count` |
| Aggregation | `COUNT(mc.name)` |
| Grouping | `GROUP BY np.unit` |
| Filters | Navy Personnel unit is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: military court child records grouped by current unit.

What it tells you: where military court records are concentrated by current unit.

What it does not tell you: it does not necessarily count unique personnel. One person can have multiple military court rows.

### Military Courts By Rank

| Item | Value |
| --- | --- |
| Chart name | `Military Courts By Rank` / report `Military Courts by Rank` |
| Chart type | Donut |
| Source report | `Military Courts by Rank` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Military Court` |
| X-axis | `rank` / report column `Rank` |
| Y-axis | `Court Count` |
| Aggregation | `COUNT(mc.name)` |
| Grouping | `GROUP BY np.rank` |
| Filters | Navy Personnel rank is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: military court child records grouped by current rank.

What it tells you: distribution of military court records across current ranks.

What it does not tell you: it does not count unique personnel, and it does not show rank at the historical court date.

## Imprisonments Charts & Dashboards

### Metadata

| Property | Value |
| --- | --- |
| Workspace record | `Imprisonments Charts & Dashboards -<private-user>` |
| Title | `Imprisonments Charts & Dashboards` |
| Route | private workspace route |
| Public | `0` |
| For user | `Administrator` |
| Owner | `Administrator` |
| Created | `2026-09-17 15:05:43.015199` |
| Last modified | `2026-09-17 15:19:58.843526` |

### Imprisonments by Unit

| Item | Value |
| --- | --- |
| Chart name | `Imprisonments by Unit` |
| Chart type | Donut |
| Source report | `Imprisonments by Unit` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Imprisonment` |
| X-axis | `unit` / report column `Unit` |
| Y-axis | `Imprisonment Count` |
| Aggregation | `COUNT(pi.name)` |
| Grouping | `GROUP BY np.unit` |
| Filters | Navy Personnel unit is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: imprisonment child records grouped by current unit.

What it tells you: distribution of imprisonment records across current units.

What it does not tell you: it does not necessarily count unique personnel imprisoned.

### Imprisonments By Rank

| Item | Value |
| --- | --- |
| Chart name | `Imprisonments By Rank` / report `Imprisonments by Rank` |
| Chart type | Donut |
| Source report | `Imprisonments by Rank` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Imprisonment` |
| X-axis | `rank` / report column `Rank` |
| Y-axis | `Imprisonment Count` |
| Aggregation | `COUNT(pi.name)` |
| Grouping | `GROUP BY np.rank` |
| Filters | Navy Personnel rank is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: imprisonment child records grouped by current rank.

What it tells you: distribution of imprisonment records across current ranks.

What it does not tell you: it does not count unique people if one person has multiple imprisonment rows.

## Travel Charts & Dashboards

### Metadata

| Property | Value |
| --- | --- |
| Workspace record | `Travel Charts & Dashboards -<private-user>` |
| Title | `Travel Charts & Dashboards` |
| Route | private workspace route |
| Public | `0` |
| For user | `Administrator` |
| Owner | `Administrator` |
| Created | `2026-09-17 15:05:55.248429` |
| Last modified | `2026-09-17 15:30:46.868659` |

Important name note: Workspace content references `Travel by Unit` and `travel By Rank`, while Dashboard Chart records are `Travel By Unit` and `Travel By Rank`. The capitalization mismatch is real site metadata.

### Travel by Unit

| Item | Value |
| --- | --- |
| Chart name in Workspace | `Travel by Unit` |
| Dashboard Chart record | `Travel By Unit` |
| Chart type | Percentage |
| Source report | `Travel by Unit` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Travel` |
| X-axis | `unit` / report column `Unit` |
| Y-axis | `Travel Count` |
| Aggregation | `COUNT(pt.name)` |
| Grouping | `GROUP BY np.unit` |
| Filters | Navy Personnel unit is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: travel history child records grouped by current unit.

What it tells you: distribution of travel records across current units.

What it does not tell you: it does not count unique personnel who traveled; one person can have multiple travel rows.

### Travel By Rank

| Item | Value |
| --- | --- |
| Chart name in Workspace | `travel By Rank` |
| Dashboard Chart record | `Travel By Rank` |
| Chart type | Percentage |
| Source report | `Travel by Rank` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Travel` |
| X-axis | `rank` / report column `Rank` |
| Y-axis | `Travel Count` |
| Aggregation | `COUNT(pt.name)` |
| Grouping | `GROUP BY np.rank` |
| Filters | Navy Personnel rank is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: travel history child records grouped by current rank.

What it tells you: distribution of travel records across current ranks.

What it does not tell you: it does not count unique travelers and does not preserve historical rank at the travel date.

## Medical Committees Charts & Dashboards

### Metadata

| Property | Value |
| --- | --- |
| Workspace record | `Medical Committees Charts & Dashboards-<private-user>` |
| Title | `Medical Committees Charts & Dashboards` |
| Route | private workspace route |
| Public | `0` |
| For user | `Administrator` |
| Owner | `Administrator` |
| Created | `2026-09-17 15:06:19.239044` |
| Last modified | `2026-09-21 08:59:29.943280` |

### Medical Committees by Unit

| Item | Value |
| --- | --- |
| Chart name | `Medical Committees by Unit` |
| Chart type | Bar |
| Source report | `Medical Committees by Unit` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Medical Committee` |
| X-axis | `unit` / report column `Unit` |
| Y-axis | `Medical Committee Count` |
| Aggregation | `COUNT(pm.name)` |
| Grouping | `GROUP BY np.unit` |
| Filters | Navy Personnel unit is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: medical committee child records grouped by current unit.

What it tells you: distribution of medical committee records across current units.

What it does not tell you: it does not count unique personnel; one person can have multiple medical committee rows.

### Medical Committees By Rank

| Item | Value |
| --- | --- |
| Chart name in Workspace | `Medical Committees By Rank` |
| Dashboard Chart record | `Medical Committees by Rank` |
| Chart type | Bar |
| Source report | `Medical Committees by Rank` |
| Source DocType | `Navy Personnel` joined to child table `Personnel Medical Committee` |
| X-axis | `rank` / report column `Rank` |
| Y-axis | `Medical Committee Count` |
| Aggregation | `COUNT(pm.name)` |
| Grouping | `GROUP BY np.rank` |
| Filters | Navy Personnel rank is not null and not empty |
| Roles on report | System Manager, Navy Personnel User, Navy Personnel Admin, Navy Personnel Editor |
| Public/private | Dashboard Chart `is_public = 0`; Workspace private for Administrator |

What it measures: medical committee child records grouped by current rank. Rank labels such as `رقيب`, `مساعد أول`, or `مساعد` are data values from current `Navy Personnel.rank`; the exact values and counts change with database contents.

What it tells you: distribution of medical committee records across current ranks.

What it does not tell you: it does not count unique personnel and does not show rank at the historical committee date.

## Chart-To-Report Mapping

| Dashboard | Chart | Source Report | X Field | Y Field | Count Type |
| --- | --- | --- | --- | --- | --- |
| Personnel Charts & Dashboard | Personnel by Unit | Personnel by Unit | Unit / `unit` | Personnel Count | Unique `Navy Personnel` rows |
| Personnel Charts & Dashboard | Personnel By Rank | Personnel by Rank | Rank / `rank` | Personnel Count | Unique `Navy Personnel` rows |
| Detentions Charts & Dashboards | Detentions by Unit | Detentions by Unit | Unit / `np.unit` | Detention Count | `Personnel Detention` child records |
| Detentions Charts & Dashboards | Detentions By Rank | Detentions by Rank | Rank / `np.rank` | Detention Count | `Personnel Detention` child records |
| Military Courts Charts & Dashboards | Military Courts by Unit | Military Courts by Unit | Unit / `np.unit` | Court Count | `Personnel Military Court` child records |
| Military Courts Charts & Dashboards | Military Courts By Rank | Military Courts by Rank | Rank / `np.rank` | Court Count | `Personnel Military Court` child records |
| Imprisonments Charts & Dashboards | Imprisonments by Unit | Imprisonments by Unit | Unit / `np.unit` | Imprisonment Count | `Personnel Imprisonment` child records |
| Imprisonments Charts & Dashboards | Imprisonments By Rank | Imprisonments by Rank | Rank / `np.rank` | Imprisonment Count | `Personnel Imprisonment` child records |
| Travel Charts & Dashboards | Travel by Unit | Travel by Unit | Unit / `np.unit` | Travel Count | `Personnel Travel` child records |
| Travel Charts & Dashboards | travel By Rank | Travel by Rank | Rank / `np.rank` | Travel Count | `Personnel Travel` child records |
| Medical Committees Charts & Dashboards | Medical Committees by Unit | Medical Committees by Unit | Unit / `np.unit` | Medical Committee Count | `Personnel Medical Committee` child records |
| Medical Committees Charts & Dashboards | Medical Committees By Rank | Medical Committees by Rank | Rank / `np.rank` | Medical Committee Count | `Personnel Medical Committee` child records |

## Reports Used By Dashboards

All dashboard chart source reports are Query Reports with `ref_doctype = Navy Personnel`, `module = Personnel Management`, and `disabled = 0`.

### Personnel by Unit

Purpose: count current Navy Personnel master records by current unit.

```sql
SELECT
    unit AS "Unit",
    COUNT(*) AS "Personnel Count"
FROM `tabNavy Personnel`
WHERE unit IS NOT NULL AND unit != ''
GROUP BY unit
ORDER BY COUNT(*) DESC
```

### Personnel by Rank

Purpose: count current Navy Personnel master records by current rank.

```sql
SELECT
    `rank` AS "Rank",
    COUNT(*) AS "Personnel Count"
FROM `tabNavy Personnel`
WHERE `rank` IS NOT NULL AND `rank` != ''
GROUP BY `rank`
ORDER BY COUNT(*) DESC
```

### Detentions by Unit / Rank

Purpose: count `Personnel Detention` child rows joined to Navy Personnel, grouped by the parent's current unit or rank.

The reports use `COUNT(pd.name)`, so they count detention records, not unique personnel.

### Imprisonments by Unit / Rank

Purpose: count `Personnel Imprisonment` child rows joined to Navy Personnel, grouped by the parent's current unit or rank.

The reports use `COUNT(pi.name)`, so they count imprisonment records, not unique personnel.

### Military Courts by Unit / Rank

Purpose: count `Personnel Military Court` child rows joined to Navy Personnel, grouped by the parent's current unit or rank.

The reports use `COUNT(mc.name)`, so they count court records, not unique personnel.

### Travel by Unit / Rank

Purpose: count `Personnel Travel` child rows joined to Navy Personnel, grouped by the parent's current unit or rank.

The reports use `COUNT(pt.name)`, so they count travel records, not unique personnel.

### Medical Committees by Unit / Rank

Purpose: count `Personnel Medical Committee` child rows joined to Navy Personnel, grouped by the parent's current unit or rank.

The reports use `COUNT(pm.name)`, so they count medical committee records, not unique personnel.

## Modification And Maintenance Notes

To safely modify these dashboards:

1. Remember the dashboard/workspace records are site-level database metadata, not source JSON in the repository.
2. Before changing chart logic, inspect the linked Query Report SQL.
3. Preserve the distinction between counting master personnel rows and counting child history records.
4. If you want these dashboards to travel with the app, export them as fixtures or add a controlled setup/migration process. Status: not currently implemented in this repository.
5. After changes, verify Workspace content, Dashboard Chart records, Report SQL, and Number Cards again.

Related references:

- [DocType And Field Reference](DOCTYPE_AND_FIELD_REFERENCE.md)
- [Permissions And Roles Reference](PERMISSIONS_AND_ROLES_REFERENCE.md)
- [Technical Documentation](TECHNICAL_DOCUMENTATION.md)
