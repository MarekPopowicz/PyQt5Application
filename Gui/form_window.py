from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QDialog

import Gui.Components.constants as Const
import Gui.Constructors.project_form_constructor as ProjFmConst
import Gui.Constructors.task_form_constructor as TaskFmConst
import Gui.Constructors.device_form_constructor as DevFmConst
import Gui.Constructors.attachment_form_constructor as AttachFmConst
import Gui.Constructors.application_form_constructor as AppFmConst


class WindowManager:
    def __init__(self, panel_name, icon: QIcon, operation_type, parent):
        self.parent = parent
        self.type = panel_name
        self.icon = icon
        self.operation = operation_type
        self.form = self.create_form()
        self.set_form_controls()

    def create_form(self):
        form = QDialog()
        form.closeEvent = self.close_event
        form.__setattr__('edit_controls', [])
        form.setWindowTitle(self.type)
        form.setWindowIcon(self.icon)
        form.setWindowTitle(self.set_window_title())
        vbox = QVBoxLayout()
        form.setLayout(vbox)
        return form

    def close_event(self, e):
        self.parent.exit = True
        e.accept()

    def set_window_title(self):
        if self.operation == 'add':
            return f"{self.type} :: Nowy"
        elif self.operation == 'edit':
            return f'{self.type} :: Edycja'
        else:
            return self.type

    def set_form_controls(self):
        if self.type == Const.PROJECT_TITLE:
            ProjFmConst.ProjectFormConstructor(self.form, self.operation, self.parent)

        if self.type == Const.TASK_TITLE:
            TaskFmConst.TaskFormConstructor(self.form, self.operation, self.parent)

        if self.type == Const.DEVICE_TITLE:
            DevFmConst.DeviceFormConstructor(self.form, self.operation, self.parent)

        if self.type == Const.ATTACHMENT_TITLE:
            AttachFmConst.AttachmentFormConstructor(self.form, self.operation, self.parent)

        if self.type == Const.PREVIEW_TITLE:
            AppFmConst.ApplicationFormConstructor(self.form, self.operation, self.parent)
