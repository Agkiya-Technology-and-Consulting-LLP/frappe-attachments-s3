# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'


from frappe.model.document import Document
from frappe_s3_attachment.frappe_s3_attachment.custom.document import custom_copy_attachments_from_amended_from
Document.copy_attachments_from_amended_from = custom_copy_attachments_from_amended_from