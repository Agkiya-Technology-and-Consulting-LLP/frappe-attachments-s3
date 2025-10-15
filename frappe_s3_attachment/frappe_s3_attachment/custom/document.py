from frappe import Document
import frappe

class CustomDocument(Document):
	# def copy_attachments_from_amended_from(self):
	# 	"""Copy attachments from `amended_from`"""
	# 	from frappe.desk.form.load import get_attachments

	# 	# loop through attachments
	# 	for attach_item in get_attachments(self.doctype, self.amended_from):
	# 		# save attachments to new doc
	# 		_file = frappe.get_doc(
	# 			{
	# 				"doctype": "File",
	# 				"file_url": attach_item.file_url,
	# 				"file_name": attach_item.file_name,
	# 				"content_hash": attach_item.content_hash,
	# 				"attached_to_name": self.name,
	# 				"attached_to_doctype": self.doctype,
	# 				"folder": "Home/Attachments",
	# 				"is_private": attach_item.is_private,
	# 			}
	# 		)
	# 		_file.save()
   
	def copy_attachments_from_amended_from(self):
		"""Copy attachments from `amended_from`"""
		from frappe.desk.form.load import get_attachments
		show_pop_up = False
		# loop through attachments
		for attach_item in get_attachments(self.doctype, self.amended_from):
			# save attachments to new doc
			if not attach_item.file_url.startswith(("/api/method/")):
				_file = frappe.get_doc(
					{
						"doctype": "File",
						"file_url": attach_item.file_url,
						"file_name": attach_item.file_name,
						"attached_to_name": self.name,
						"attached_to_doctype": self.doctype,
						"folder": "Home/Attachments",
						"is_private": attach_item.is_private,
					}
				)
				_file.save()
			elif attach_item.file_url.startswith(("/api/method/")):
				show_pop_up = True

		if show_pop_up:
			frappe.msgprint("""Note: The attachments from the cancelled document aren't automatically brought forward.<br>
							If you'd like them to appear here, please link or upload them again.""")

	