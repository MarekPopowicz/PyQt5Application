from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPlainTextEdit, QGroupBox, QVBoxLayout, QComboBox, \
    QDoubleSpinBox, QPushButton, QTableWidget
from Data.db_manager import DBManager as DbMan
from Data.db_query_commands import QUERY_SELECT_ALL_DEVICE_TYPES, QUERY_SELECT_ALL_REGULATIONS
from Gui.Components.button_panel import ButtonPanel
from Gui.Components.msg_dialogs import MsgBox
from Logic.main_window_logic import MainWindowLogic
import Gui.Components.constants as Const


def create_item_panel(widget_edit_type, label_name):
    layout = QHBoxLayout()
    label = QLabel(label_name)
    layout.addWidget(label)

    layout.addWidget(widget_edit_type)
    layout.setAlignment(Qt.AlignLeft)
    return layout


class DeviceFormConstructor:
    def __init__(self, form: QDialog, operation: str, parent):
        self.parent_logic = MainWindowLogic(parent)
        self.form = form
        self.current_task_id = self.parent_logic.parent.findChild(QTableWidget, Const.TASK_TITLE).object_id
        self.current_device_id = self.parent_logic.parent.findChild(QTableWidget, Const.DEVICE_TITLE).object_id
        with open('Gui/QSS/device_form.qss', 'r') as f:
            self.form.setStyleSheet(f.read())
        self.operation = operation
        self.create_details_panel("Szczegóły")
        self.create_regulation_panel("Docelowa regulacja prawna")
        self.create_device_notice_panel("Informacja dodatkowa")
        self.create_project_save_button()
        self.exec_project_form()

    def exec_project_form(self):
        self.form.adjustSize()
        current_width = self.form.width()
        current_height = self.form.height()
        self.form.setFixedSize(current_width, current_height)
        self.form.exec_()

    def create_details_panel(self, label):
        device_details = {}
        sql_query_devices_type_rows = QUERY_SELECT_ALL_DEVICE_TYPES
        devices_type_rows = DbMan.show_items(sql_query_devices_type_rows)

        v_layout = QVBoxLayout()

        device_type_combo = QComboBox()

        for row in devices_type_rows:
            device_type_combo.addItem(row[0])

        device_type_combo.setCurrentIndex(-1)

        device_type_item = create_item_panel(device_type_combo, "Urządzenie")
        device_details['Urządzenie'] = device_type_combo
        long_spin_box = QDoubleSpinBox()
        long_spin_box.setMaximum(100000)
        long_spin_box.setMinimumWidth(100)
        device_long_item = create_item_panel(long_spin_box, "Długość")
        device_details['Długość'] = long_spin_box
        device_long_item.addWidget(QLabel("metrów"))

        width_spin_box = QDoubleSpinBox()
        width_spin_box.setMaximum(100000)
        width_spin_box.setMinimumWidth(100)
        device_width_item = create_item_panel(width_spin_box, "Szerokość")
        device_details['Szerokość'] = width_spin_box
        device_width_item.addWidget(QLabel("metrów"))

        device_details['Device_id'] = self.current_device_id
        device_details['Task_id'] = self.current_task_id

        self.form.edit_controls.append(device_details)

        v_layout.addLayout(device_type_item)
        v_layout.addLayout(device_long_item)
        v_layout.addLayout(device_width_item)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(v_layout)
        self.form.layout().addWidget(groupbox)

    def create_regulation_panel(self, label):
        regulation_details = {}

        sql_query_regulation_type_rows = QUERY_SELECT_ALL_REGULATIONS
        rows = DbMan.show_items(sql_query_regulation_type_rows)

        regulation_type_combo = QComboBox()
        for row in rows:
            regulation_type_combo.addItem(row[0])

        regulation_type_combo.setCurrentIndex(-1)
        regulation_item = create_item_panel(regulation_type_combo, "Tytuł")
        regulation_details['Tytuł'] = regulation_type_combo

        self.form.edit_controls.append(regulation_details)

        groupbox = QGroupBox(label)

        groupbox.setStyleSheet('QGroupBox {font-weight: bold;}')
        groupbox.setLayout(regulation_item)
        self.form.layout().addWidget(groupbox)

    def create_device_notice_panel(self, label):
        notice = {}
        layout = QVBoxLayout()
        device_notice_label = QLabel("Uwagi")
        device_notice_edit = QPlainTextEdit()

        notice['Uwagi'] = device_notice_edit
        self.form.edit_controls.append(notice)

        device_notice_edit.setObjectName("Uwagi")
        device_notice_edit.lineWrapMode()
        device_notice_edit.setMaximumHeight(110)
        layout.addWidget(device_notice_label)
        layout.addWidget(device_notice_edit)

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
        result = False
        device_id = self.parent_logic.device_logic.button_clicked(form_data, self.operation)
        if device_id != 0:
            result = True

        if result:
            MsgBox('ok_dialog', 'Urządzenie', 'Operacja zakończona sukcesem.', QIcon(Const.APP_ICON))
            self.form.close()
            self.parent_logic.update_device_table_view(self.operation, device_id)
        else:
            MsgBox('error_dialog', 'Urządzenie', 'Coś poszło nie tak...', QIcon(Const.APP_ICON))
            self.form.close()
