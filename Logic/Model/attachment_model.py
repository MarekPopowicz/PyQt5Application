class Attachment:
    def __init__(self,
                 a_id=0,
                 a_project_id=0,
                 a_document_name='',
                 a_document_original=0,
                 a_document_count=0,
                 a_notice=''):
        self.id = a_id
        self.project_id = a_project_id
        self.document_name = a_document_name
        self.document_original = a_document_original
        self.document_count = a_document_count
        self.notice = a_notice
