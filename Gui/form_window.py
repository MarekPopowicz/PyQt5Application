from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QDialog

import Gui.Components.constants as Const
import Gui.Constructors.project_form_constructor as ProjFmConst
import Gui.Constructors.task_form_constructor as TaskFmConst
import Gui.Constructors.device_form_constructor as DevFmConst
import Gui.Constructors.attachment_form_constructor as AttachFmConst


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
        form.__setattr__('edit_controls', [])
        form.setWindowTitle(self.type)
        form.setWindowIcon(self.icon)
        form.setWindowTitle(self.set_window_title())
        vbox = QVBoxLayout()
        form.setLayout(vbox)
        return form

    def set_window_title(self):
        if self.operation == 'add':
            if self.parent.creator_init_flag:
                return f"{self.type} :: Kreator nowego projektu"
            else:
                return f"{self.type} :: Nowy"
        else:
            return f'{self.type} :: Edycja'

    def set_form_controls(self):
        if self.type == Const.PROJECT_TITLE:
            ProjFmConst.ProjectFormConstructor(self.form, self.operation, self.parent)

        if self.type == Const.TASK_TITLE:
            TaskFmConst.TaskFormConstructor(self.form, self.operation, self.parent)

        if self.type == Const.DEVICE_TITLE:
            DevFmConst.DeviceFormConstructor(self.form, self.operation, self.parent)

        if self.type == Const.ATTACHMENT_TITLE:
            AttachFmConst.AttachmentFormConstructor(self.form, self.operation, self.parent)
