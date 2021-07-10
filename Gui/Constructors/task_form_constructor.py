from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPlainTextEdit, QGroupBox, QLineEdit, QVBoxLayout, \
    QPushButton, QTableWidget
from Gui.Components.button_panel import ButtonPanel
from Gui.Components.msg_dialogs import MsgBox
from Logic.main_window_logic import MainWindowLogic
import Gui.Components.constants as Const

items_edit = {}


def create_item_edit_panel(item_label, max_width: int):
    layout = QHBoxLayout()
    new_label = QLabel(item_label)
    new_edit = QLineEdit()
    new_edit.setMaximumWidth(max_width)
    items_edit[item_label] = new_edit
    layout.addWidget(new_label)
    layout.addWidget(new_edit)
    return layout


class TaskFormConstructor:
    def __init__(self, form: QDialog, operation: str, parent):
        self.parent_logic = MainWindowLogic(parent)
        self.form = form
        self.current_task_id = self.parent_logic.parent.findChild(QTableWidget, Const.TASK_TITLE).object_id
        with open('Gui/QSS/task_form.qss', 'r') as f:
            self.form.setStyleSheet(f.read())
        self.operation = operation
        self.create_details_panel("Szczegóły")
        self.create_project_notice_panel("Informacja dodatkowa")
        self.create_project_save_button()
        self.exec_project_form()

    def exec_project_form(self):
        self.form.adjustSize()
        current_width = self.form.width()
        current_height = self.form.height()
        self.form.setFixedSize(current_width, current_height)
        if self.operation == 'edit':
            if self.current_task_id <= 0:
                MsgBox('error_dialog', 'Działka', 'Brak danych do edycji.', QIcon(Const.APP_ICON))
                return
            else:
                self.set_task_data()
        self.form.exec_()

    def create_details_panel(self, label):
        owner_data = {}
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        register_panel = create_item_edit_panel('KW', 400)
        parcel_panel = create_item_edit_panel('Dz.', 50)
        map_sheet_panel = create_item_edit_panel('AM', 50)
        area_panel = create_item_edit_panel('Obręb', 400)
        owner_label = QLabel('Dane kontaktowe właściciela')
        owner_label.setStyleSheet('QLabel {margin-top: 10px}')
        owner_edit = QPlainTextEdit()
        owner_data['Właściciel'] = owner_edit
        owner_data['Project_id'] = self.parent_logic.parent.current_project_id
        owner_edit.lineWrapMode()
        owner_edit.setMaximumHeight(110)

        self.form.edit_controls.append(items_edit)
        self.form.edit_controls.append(owner_data)

        v_layout.addLayout(register_panel)
        h_layout.addLayout(parcel_panel)
        h_layout.addLayout(map_sheet_panel)
        h_layout.addLayout(area_panel)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(owner_label)
        v_layout.addWidget(owner_edit)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(v_layout)
        self.form.layout().addWidget(groupbox)

    def create_project_notice_panel(self, label):
        notice = {}
        layout = QVBoxLayout()
        task_notice_label = QLabel("Uwagi")
        task_notice_edit = QPlainTextEdit()
        notice["Uwagi"] = task_notice_edit

        self.form.edit_controls.append(notice)

        task_notice_edit.lineWrapMode()
        task_notice_edit.setMaximumHeight(110)
        layout.addWidget(task_notice_label)
        layout.addWidget(task_notice_edit)

        groupbox = QGroupBox(label)

        groupbox.setStyleSheet('QGroupBox {font-weight: bold;}')
        groupbox.setLayout(layout)
        self.form.layout().addWidget(groupbox)

    def create_project_save_button(self):
        button_panel = ButtonPanel(self.form)
        self.form = button_panel.form
        save_button = self.form.findChild(QPushButton, "Zapisz")
        save_button.clicked.connect(self.save_button_clicked)

    def save_button_clicked(self):
        form_data = self.form.edit_controls
        form_data[0]['task_id'] = self.current_task_id
        result = False
        task_id = self.parent_logic.task_logic.button_clicked(form_data, self.operation)
        if task_id != 0:
            result = True

        if result:
            MsgBox('ok_dialog', 'Działka', 'Operacja zakończona sukcesem.', QIcon(Const.APP_ICON))
            self.form.close()
            self.parent_logic.update_task_table_view(self.operation, task_id)
            self.parent_logic.update_device_table_view('set', -1)
        else:
            MsgBox('error_dialog', 'Działka', 'Coś poszło nie tak...', QIcon(Const.APP_ICON))
            self.form.close()
            self.parent_logic.parent.creator_init_flag = False

    def set_task_data(self):
        task = self.parent_logic.task_logic.get_task(str(self.current_task_id))
        if task is not None:
            task_form_data = self.form.edit_controls
            task_form_data[0]['KW'].setText(task.register_no)
            task_form_data[0]['Dz.'].setText(task.parcel_no)
            task_form_data[0]['AM'].setText(task.sheet_no)
            task_form_data[0]['Obręb'].setText(task.area_name)
            task_form_data[1]['Właściciel'].setPlainText(task.owner_data)
            task_form_data[2]['Uwagi'].setPlainText(task.notice)
