from Logic.Model.attachment_model import Attachment
import Data.db_query_commands as dbQry
from Data.db_manager import DBManager as DbMan


class AttachmentFormLogic:
    def __init__(self):
        self.attachment = Attachment()

    def button_clicked(self, data, operation_type):
        if len(data) > 0:
            self.set_attachment(data)
            if operation_type == 'add':
                return self.add_attachment()
            else:
                return self.update_attachment()

    def set_attachment(self, data):
        self.attachment.id = data[0]['attachment_id']
        self.attachment.project_id = data[0]['project_id']
        self.attachment.document_name = data[0]['Załącznik'].currentText()
        self.attachment.document_count = data[0]['Sztuk'].value()
        if data[0]['Oryginał'].isChecked():
            self.attachment.document_original = 1
        else:
            self.attachment.document_original = 0
        self.attachment.notice = data[1]['Uwagi'].toPlainText()

    def add_attachment(self):
        query = dbQry.QUERY_INSERT_ATTACHMENT
        result = DbMan.add_new_items(query, (
            self.attachment.project_id,
            self.attachment.document_name,
            self.attachment.document_original,
            self.attachment.document_count,
            self.attachment.notice
        ))
        if result is not None:
            self.attachment.id = result
            return result
        else:
            return 0

    def update_attachment(self):
        query = dbQry.QUERY_UPDATE_ATTACHMENT
        qry = query.replace('id_value', str(self.attachment.id))
        qry = qry.replace('document_name_value', self.attachment.document_name)
        qry = qry.replace('document_count_value', str(self.attachment.document_count))
        qry = qry.replace('document_original_value', str(self.attachment.document_original))
        qry = qry.replace('notice_value', self.attachment.notice)
        result = DbMan.update_item(qry)
        return result

    def get_attachment(self, attachment_id):
        query = dbQry.QUERY_SELECT_ATTACHMENT
        qry = query.replace('?', attachment_id)
        result = DbMan.show_items(qry)
        if len(result) > 0:
            self.attachment.id = result[0][0]
            self.attachment.project_id = result[0][1]
            self.attachment.document_name = result[0][2]
            self.attachment.document_original = result[0][3]
            self.attachment.document_count = result[0][4]
            self.attachment.notice = result[0][5]
            return self.attachment
        else:
            return None

    @staticmethod
    def delete_attachment(attachment_id: str):
        query = dbQry.QUERY_DELETE_ATTACHMENT
        qry = query.replace('?', attachment_id)
        result = DbMan.delete_item(qry)
        return result

    @staticmethod
    def delete_attachments(project_id: str):
        query = dbQry.QUERY_DELETE_ATTACHMENTS
        qry = query.replace('?', project_id)
        result = DbMan.delete_item(qry)
        return result

    @staticmethod
    def get_attachment_list(project_id):
        query = dbQry.QUERY_SELECT_ATTACHMENTS
        qry = query.replace('?', project_id)
        attachments = DbMan.show_items(qry)
        if len(attachments) > 0:
            return attachments
        else:
            return []

    @staticmethod
    def get_attachment_data(project_id):
        query = dbQry.QUERY_SELECT_ATTACHMENTS_DATA
        qry = query.replace('?', project_id)
        attachments = DbMan.show_items(qry)
        if len(attachments) > 0:
            return attachments
        else:
            return []
