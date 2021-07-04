from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class MsgBox(QMessageBox):
    def __init__(self, dlg_type, title, prompt_text, icon: QIcon):
        super().__init__()
        self.title = title
        self.prompt_txt = prompt_text
        self.icon = icon
        self.last_user_answer = False
        if dlg_type == 'ok_cancel_dlg':
            self.ok_cancel_dialog()
        elif dlg_type == 'error_dialog':
            self.error_dialog()
        else:
            self.ok_dialog()

    def ok_cancel_dialog(self):
        self.setIcon(self.Question)
        self.setText(self.prompt_txt)
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setStandardButtons(self.Ok | self.Cancel)
        return_value = self.exec()
        if return_value == self.Ok:
            self.last_user_answer = True

    def ok_dialog(self):
        self.setIcon(self.Information)
        self.setText(self.prompt_txt)
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setStandardButtons(self.Ok)
        self.exec()

    def error_dialog(self):
        self.setIcon(self.Critical)
        self.setText(self.prompt_txt)
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setStandardButtons(self.Ok)
        self.exec()
