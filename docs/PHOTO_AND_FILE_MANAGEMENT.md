# Photo And File Management

> Truth Mode: This document describes the current source files in `apps/personnel_management` as inspected during documentation generation. Site-only records that are not present as app JSON are marked Not Verified. Actual implementation takes precedence over this documentation.


## Source File

`personnel_management/personnel_management/doctype/navy_personnel/navy_personnel.py`

## Personnel Photo

| Item | Implementation |
| --- | --- |
| Field | image |
| Field type | Attach Image |
| URL pattern | /files/Personnel/<military_number>.<extension> |
| Filesystem folder | sites/<site>/public/files/Personnel/ |
| Server function | normalize_personnel_photo() |
| File record | ensure_file_record() creates/updates Frappe File metadata |


## Family Photo

| Item | Implementation |
| --- | --- |
| Field | family_photo |
| Field type | Attach Image |
| URL pattern | /files/Personnel/Family/<military_number>.<extension> |
| Filesystem folder | sites/<site>/public/files/Personnel/Family/ |
| Legacy field | family_image is hidden and cleared when family_photo normalizes |
| Server function | normalize_personnel_photo() |


## Allowed Extensions

`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.tif`, `.tiff`, `.jfif`

## Behavior

- If no value is supplied, code searches for exactly one existing file whose stem matches the military number in the target folder.
- If no image exists, the field remains empty.
- If an uploaded file has an invalid extension or cannot be found, normalization returns empty.
- Re-upload replaces same-person files in the same target folder and removes old File records for that field/path.
- Personnel photo and family photo use different folders and do not replace each other.
- The original valid image extension is preserved.

## Security / Operational Notes

Photos are stored under public files, so they are served as public site files. This is standard for the current implementation; changing privacy would require code changes and migration of file paths.
