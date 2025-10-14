
from frappe.core.doctype.file.file import URL_PREFIXES, File, decode_file_content
import os
import frappe
from frappe import _
from frappe.utils import get_files_path, get_url
from frappe.utils.file_manager import is_safe_path


class CustomFile(File):
	def validate_file_url(self):
		if self.is_remote_file or not self.file_url:
			return

		if not self.file_url.startswith(("/files/", "/private/files/", "/api/method/")):
			# Probably an invalid URL since it doesn't start with http either
			frappe.throw(
				frappe._("URL must start with http:// or https://"),
				title=frappe._("Invalid URL"),
			)

	def get_content(self) -> bytes:
		if self.is_folder:
			frappe.throw(frappe._("Cannot get file contents of a Folder"))

		if self.get("content"):
			self._content = self.content
			if self.decode:
				self._content = decode_file_content(self._content)
				self.decode = False
			# self.content = None # TODO: This needs to happen; make it happen somehow
			return self._content

		if self.file_url:
			self.validate_file_url()
   
		if self.file_url.startswith(("/files/", "/private/files/")):
			file_path = self.get_full_path()

			# read the file
			with open(file_path, mode="rb") as f:
				self._content = f.read()
				try:
					# for plain text files
					self._content = self._content.decode()
				except UnicodeDecodeError:
					# for .png, .jpg, etc
					pass

			return self._content

		elif self.file_url.startswith(("/api/method/")):
			from frappe_s3_attachment.controller import S3Operations
			s3_ops = S3Operations()
			frappe.log_error("@@@@ self.content_hash ",self.content_hash)
			obj = s3_ops.read_file_from_s3(self.content_hash)
			file_content = obj["Body"].read()
			self._content = file_content.decode("utf-8")
			return self._content


	def get_full_path(self):
		"""Returns file path from given file name"""

		file_path = self.file_url or self.file_name

		site_url = get_url()
		if "/files/" in file_path and file_path.startswith(site_url):
			file_path = file_path.split(site_url, 1)[1]

		if "/" not in file_path:
			if self.is_private:
				file_path = f"/private/files/{file_path}"
			else:
				file_path = f"/files/{file_path}"

		if file_path.startswith("/private/files/"):
			file_path = get_files_path(*file_path.split("/private/files/", 1)[1].split("/"), is_private=1)

		elif file_path.startswith("/files/"):
			file_path = get_files_path(*file_path.split("/files/", 1)[1].split("/"))

		elif file_path.startswith(URL_PREFIXES):
			pass

		elif not self.file_url:
			frappe.throw(_("There is some problem with the file url: {0}").format(file_path))

		if not is_safe_path(file_path) and not file_path.startswith(("/api/method/")):
			frappe.throw(_("Cannot access file path {0}").format(file_path))

		if os.path.sep in self.file_name:
			frappe.throw(_("File name cannot have {0}").format(os.path.sep))

		return file_path

	