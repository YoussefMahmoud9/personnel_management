import os
import json
from pathlib import Path
from urllib.parse import unquote

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


PHOTO_FIELDS = {
	"image": {
		"directory": ("Personnel",),
		"url_prefix": "/files/Personnel",
	},
	"family_photo": {
		"directory": ("Personnel", "Family"),
		"url_prefix": "/files/Personnel/Family",
	},
}

LEGACY_PHOTO_FIELDS = {
	"family_photo": "family_image",
}

IMAGE_EXTENSIONS = {
	".jpg",
	".jpeg",
	".png",
	".gif",
	".webp",
	".bmp",
	".tif",
	".tiff",
	".jfif",
}


class NavyPersonnel(Document):
	def validate(self):
		self.calculate_derived_dates()
		self.normalize_photo_fields()
		self.normalize_committee_records()

	def calculate_derived_dates(self):
		self.age = calculate_completed_years(self.birth_date)
		self.service_year_number = calculate_completed_years(self.high_salary_date)

	def normalize_photo_fields(self):
		if not self.military_number:
			return

		for fieldname in PHOTO_FIELDS:
			value = self.get(fieldname)
			legacy_field = LEGACY_PHOTO_FIELDS.get(fieldname)

			if not value and legacy_field:
				value = self.get(legacy_field)

			normalized = normalize_personnel_photo(
				doctype=self.doctype,
				docname=self.name,
				military_number=self.military_number,
				fieldname=fieldname,
				file_value=value,
			)

			self.set(fieldname, normalized)

			if legacy_field:
				self.set(legacy_field, None)

	def normalize_committee_records(self):
		for row in self.get("committee_records"):
			if not row.personnel and not self.is_new():
				row.personnel = self.name

			if not row.personnel:
				continue

			source = get_personnel_snapshot_source(
				row.personnel,
				current_doc=self,
			)

			if not source:
				continue

			apply_personnel_snapshot_to_committee_record(row, source)


def get_personnel_snapshot_source(personnel, current_doc=None):
	if current_doc and personnel == current_doc.name:
		return current_doc

	if not frappe.db.exists("Navy Personnel", personnel):
		return None

	return frappe.get_doc("Navy Personnel", personnel)


def apply_personnel_snapshot_to_committee_record(row, source):
	row.military_number = source.military_number
	row.committee_name_value = source.full_name
	row.rank = source.rank
	row.category = source.category
	row.age = source.age
	row.service_year_number = source.service_year_number
	row.weapon = source.weapon
	row.job = source.job
	row.unit = source.unit
	row.report_1 = source.report_1
	row.report_2 = source.report_2
	row.report_3 = source.report_3


def calculate_completed_years(start_date, reference_date=None):
	if not start_date:
		return None

	start = getdate(start_date)
	reference = getdate(reference_date or today())

	if start > reference:
		return 0

	years = reference.year - start.year

	if (reference.month, reference.day) < (start.month, start.day):
		years -= 1

	return years


def normalize_personnel_photo(
	doctype,
	docname,
	military_number,
	fieldname,
	file_value,
):
	settings = PHOTO_FIELDS[fieldname]

	file_value = unquote(str(file_value).strip()) if file_value else None

	if not file_value:
		existing_url = find_existing_photo_by_military_number(
			field_settings=settings,
			military_number=military_number,
		)

		if existing_url:
			ensure_file_record(
				doctype=doctype,
				docname=docname,
				fieldname=fieldname,
				file_url=existing_url,
				file_name=Path(existing_url).name,
			)

		return existing_url

	extension = get_image_extension(file_value)

	if not extension:
		return None

	target_url = f"{settings['url_prefix']}/{military_number}{extension}"
	target_path = get_public_file_path(settings["directory"], f"{military_number}{extension}")

	if file_value == target_url:
		if target_path.exists():
			ensure_file_record(
				doctype=doctype,
				docname=docname,
				fieldname=fieldname,
				file_url=target_url,
				file_name=target_path.name,
			)
			return target_url

		return None

	source_path = get_source_path(
		file_value=file_value,
		field_settings=settings,
		military_number=military_number,
		extension=extension,
	)

	if not source_path or not source_path.exists():
		return None

	move_personnel_photo(
		source_path=source_path,
		target_path=target_path,
	)

	target_url = f"{settings['url_prefix']}/{target_path.name}"
	ensure_file_record(
		doctype=doctype,
		docname=docname,
		fieldname=fieldname,
		file_url=target_url,
		file_name=target_path.name,
	)

	return target_url


def get_image_extension(file_value):
	extension = Path(file_value.split("?", 1)[0]).suffix

	if not extension or extension.lower() not in IMAGE_EXTENSIONS:
		return None

	return extension


def get_public_file_path(directory, filename):
	return Path(frappe.get_site_path("public", "files", *directory, filename))


def get_source_path(file_value, field_settings, military_number, extension):
	if file_value.startswith("/files/"):
		return Path(frappe.get_site_path("public", *file_value.strip("/").split("/")))

	if "/" in file_value:
		return None

	source_name = Path(file_value).name

	if Path(source_name).stem != military_number:
		return None

	source_path = get_public_file_path(field_settings["directory"], source_name)

	if source_path.exists():
		return source_path

	target_path = get_public_file_path(field_settings["directory"], f"{military_number}{extension}")

	if target_path.exists():
		return target_path

	return None


def find_existing_photo_by_military_number(field_settings, military_number):
	directory = Path(frappe.get_site_path("public", "files", *field_settings["directory"]))

	if not directory.exists():
		return None

	matches = [
		path
		for path in directory.iterdir()
		if path.is_file()
		and path.stem == military_number
		and path.suffix.lower() in IMAGE_EXTENSIONS
	]

	if len(matches) != 1:
		return None

	return f"{field_settings['url_prefix']}/{matches[0].name}"


def move_personnel_photo(source_path, target_path):
	source_path = Path(source_path)
	target_path = Path(target_path)

	target_path.parent.mkdir(parents=True, exist_ok=True)
	remove_existing_photo_files_for_same_person(target_path)

	if source_path.resolve() == target_path.resolve():
		return

	if target_path.exists():
		target_path.unlink()

	os.replace(source_path, target_path)


def remove_existing_photo_files_for_same_person(target_path):
	target_path = Path(target_path)

	for path in target_path.parent.iterdir():
		if (
			path.is_file()
			and path != target_path
			and path.stem == target_path.stem
			and path.suffix.lower() in IMAGE_EXTENSIONS
		):
			path.unlink()

			file_url = "/files/" + path.relative_to(frappe.get_site_path("public", "files")).as_posix()

			for file_name in frappe.get_all(
				"File",
				filters={"file_url": file_url},
				pluck="name",
			):
				frappe.delete_doc(
					"File",
					file_name,
					ignore_permissions=True,
					force=True,
				)


def ensure_file_record(doctype, docname, fieldname, file_url, file_name):
	clear_other_photo_file_records(
		doctype=doctype,
		docname=docname,
		fieldname=fieldname,
		file_url=file_url,
	)

	existing = frappe.db.get_value(
		"File",
		{
			"file_url": file_url,
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
		},
		"name",
	)

	if existing:
		frappe.db.set_value(
			"File",
			existing,
			{
				"file_name": file_name,
				"attached_to_field": fieldname,
				"is_private": 0,
			},
			update_modified=False,
		)
		return existing

	file_doc = frappe.get_doc(
		{
			"doctype": "File",
			"file_name": file_name,
			"file_url": file_url,
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
			"attached_to_field": fieldname,
			"is_private": 0,
		}
	)
	file_doc.flags.ignore_permissions = True
	file_doc.flags.copy_from_existing_file = True
	file_doc.insert(ignore_permissions=True)

	return file_doc.name


def clear_other_photo_file_records(doctype, docname, fieldname, file_url):
	for file_name in frappe.get_all(
		"File",
		filters=[
			["attached_to_doctype", "=", doctype],
			["attached_to_name", "=", docname],
			["attached_to_field", "=", fieldname],
			["file_url", "!=", file_url],
		],
		pluck="name",
	):
		frappe.delete_doc(
			"File",
			file_name,
			ignore_permissions=True,
			force=True,
		)


@frappe.whitelist()
def repair_personnel_photo_references():
	"""Normalize existing Navy Personnel photo fields without guessing identities."""
	report = {
		"updated": [],
		"cleared": [],
		"unchanged": [],
	}

	for row in frappe.get_all(
		"Navy Personnel",
		fields=["name", "military_number", "image", "family_photo", "family_image"],
		order_by="name",
	):
		updates = {}

		for fieldname in PHOTO_FIELDS:
			value = row.get(fieldname)

			if fieldname == "family_photo" and not value:
				value = row.get("family_image")

			normalized = normalize_personnel_photo(
				doctype="Navy Personnel",
				docname=row.name,
				military_number=row.military_number,
				fieldname=fieldname,
				file_value=value,
			)

			if normalized != value:
				updates[fieldname] = normalized

			if fieldname == "family_photo" and row.get("family_image"):
				updates["family_image"] = None

		if updates:
			frappe.db.set_value(
				"Navy Personnel",
				row.name,
				updates,
				update_modified=False,
			)

			if any(value is None for value in updates.values()):
				report["cleared"].append({"name": row.name, "updates": updates})
			else:
				report["updated"].append({"name": row.name, "updates": updates})
		else:
			report["unchanged"].append(row.name)

	frappe.db.commit()

	return report


@frappe.whitelist()
def get_personnel_for_committee(committee):
	if not committee:
		return []

	return frappe.get_all(
		"Personnel Committee Record",
		filters={"committee": committee},
		pluck="personnel",
		order_by="personnel asc",
	)


@frappe.whitelist()
def get_committee_summaries(personnel_names):
	if isinstance(personnel_names, str):
		personnel_names = json.loads(personnel_names)

	personnel_names = [name for name in personnel_names if name]

	if not personnel_names:
		return {}

	rows = frappe.get_all(
		"Personnel Committee Record",
		filters={"personnel": ["in", personnel_names]},
		fields=["personnel", "committee"],
		order_by="committee asc",
	)

	summaries = {
		personnel: {
			"count": 0,
			"committees": [],
		}
		for personnel in personnel_names
	}

	for row in rows:
		if row.committee not in summaries[row.personnel]["committees"]:
			summaries[row.personnel]["committees"].append(row.committee)

	for summary in summaries.values():
		summary["count"] = len(summary["committees"])

	return summaries
