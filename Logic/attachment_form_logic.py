from Logic.Model.attachment_model import Attachment


class AttachmentFormLogic:
    def __init__(self):
        self.attachment = Attachment()

    def button_clicked(self, data, operation_type):
        self.set_project(data)

    def set_project(self, data):
        pass
