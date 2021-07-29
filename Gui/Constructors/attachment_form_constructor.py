from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QGroupBox, QHBoxLayout, QComboBox, \
    QCheckBox, QSpinBox, QPushButton, QTableWidget

from Data.db_manager import DBManager as DbMan
from Data.db_query_commands import QUERY_SELECT_ALL_DOCUMENTS
from Gui.Components.button_panel import ButtonPanel
from Gui.Components.msg_dialogs import MsgBox
from Logic.main_window_logic import MainWindowLogic
import Gui.Components.constants as Const
from Logic.tools import test_data, resource_path


def create_item_panel(widget_edit_type, label_name):
    layout = QHBoxLayout()
    label = QLabel(label_name)
    label.setStyleSheet("color: red")
    layout.addWidget(label)
    widget_edit_type.setObjectName(label_name)
    layout.addWidget(widget_edit_type)
    layout.setAlignment(Qt.AlignLeft)
    return layout


class AttachmentFormConstructor:
    def __init__(self, form: QDialog, operation: str, parent):
        self.parent_logic = MainWindowLogic(parent)
        self.form = form
        self.current_attachment_id = self.parent_logic.parent.findChild(QTableWidget, Const.ATTACHMENT_TITLE).object_id
        qss_dir = resource_path("Gui\\QSS\\")
        with open(qss_dir + 'attachment_form.qss', 'r') as f:
            self.form.setStyleSheet(f.read())
        self.operation = operation
        self.create_details_panel("Szczegóły")
        self.create_attachment_notice_panel("Informacja dodatkowa")
        self.create_project_save_button()
        self.exec_project_form()

    def exec_project_form(self):
        self.form.adjustSize()
        current_width = self.form.width()
        current_height = self.form.height()
        self.form.setFixedSize(current_width, current_height)
        if self.operation == 'edit':
            if int(self.parent_logic.parent.current_project_id) <= 0:
                return
            else:
                self.set_attachment_data()
        self.form.exec_()

    def create_details_panel(self, label):
        attachment_details = {}
        sql_query_document_type_rows = QUERY_SELECT_ALL_DOCUMENTS
        rows = DbMan.show_items(sql_query_document_type_rows)

        v_layout = QVBoxLayout()

        document_type_combo = QComboBox()
        for row in rows:
            document_type_combo.addItem(row[0])

        document_type_combo.setCurrentIndex(-1)
        doc_type_item = create_item_panel(document_type_combo, "Załącznik")
        attachment_details['Załącznik'] = document_type_combo

        original_checkbox = QCheckBox()
        attachment_details['Oryginał'] = original_checkbox
        original = create_item_panel(original_checkbox, "Oryginał")

        szt = QSpinBox()
        attachment_details['Sztuk'] = szt
        szt.setMinimum(1)
        quantity = create_item_panel(szt, "Sztuk")
        attachment_details['project_id'] = self.parent_logic.parent.current_project_id
        attachment_details['attachment_id'] = self.current_attachment_id
        self.form.edit_controls.append(attachment_details)

        v_layout.addLayout(doc_type_item)
        v_layout.addLayout(original)
        v_layout.addLayout(quantity)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(v_layout)
        self.form.layout().addWidget(groupbox)

    def create_attachment_notice_panel(self, label):
        attachment_notice = {}
        layout = QVBoxLayout()
        attachment_notice_label = QLabel("Uwagi")
        attachment_notice_edit = QPlainTextEdit()

        attachment_notice['Uwagi'] = attachment_notice_edit
        self.form.edit_controls.append(attachment_notice)

        attachment_notice_edit.setObjectName("Uwagi")
        attachment_notice_edit.lineWrapMode()
        attachment_notice_edit.setMaximumHeight(110)
        layout.addWidget(attachment_notice_label)
        layout.addWidget(attachment_notice_edit)

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
        if not self.validate():
            return
        form_data = self.form.edit_controls
        result = False

        attachment_id = self.parent_logic.attachment_logic.button_clicked(form_data, self.operation)
        if attachment_id != 0:
            result = True

        if result:
            MsgBox('ok_dialog', 'Załącznik', 'Operacja zakończona sukcesem.', QIcon(Const.APP_ICON))
            self.form.close()
            if self.operation == 'add':
                self.parent_logic.update_attachment_table_view(self.operation, attachment_id)
            else:
                self.parent_logic.update_attachment_table_view(self.operation, self.current_attachment_id)
        else:
            MsgBox('error_dialog', 'Załącznik', 'Coś poszło nie tak...', QIcon(Const.APP_ICON))
            self.form.close()

        self.parent_logic.parent.exit = False

    def set_attachment_data(self):
        attachment = self.parent_logic.attachment_logic.get_attachment(str(self.current_attachment_id))
        if attachment is not None:
            attachment_form_data = self.form.edit_controls
            attachment_form_data[0]['Załącznik'].setCurrentText(attachment.document_name)
            if attachment.document_original == 1:
                attachment_form_data[0]['Oryginał'].setChecked(True)
            attachment_form_data[0]['Sztuk'].setValue(attachment.document_count)
            attachment_form_data[1]['Uwagi'].setPlainText(attachment.notice)

    def validate(self):
        results = []
        result = False
        form_data = self.form.edit_controls
        zalacznik = form_data[0]['Załącznik'].currentText()

        results.append(test_data(r".+", zalacznik))

        for item in results:
            if not item:
                MsgBox('error_dialog', 'Załącznik',
                       'Co najmniej jedno z pól formularza nie zawiera wymaganych informacji '
                       'lub wprowadzone dane są niewłaściwego formatu.', QIcon(Const.APP_ICON))
                result = False
                break
            else:
                result = True
        return result

