from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QGroupBox, QHBoxLayout, QComboBox, \
    QCheckBox, QSpinBox, QPushButton

from Data.db_manager import DBManager as DbMan
from Data.db_query_commands import QUERY_SELECT_ALL_DOCUMENTS
from Gui.Components.button_panel import ButtonPanel
from Logic.main_window_logic import MainWindowLogic


def create_item_panel(widget_edit_type, label_name):
    layout = QHBoxLayout()
    label = QLabel(label_name)
    layout.addWidget(label)
    widget_edit_type.setObjectName(label_name)
    layout.addWidget(widget_edit_type)
    layout.setAlignment(Qt.AlignLeft)
    return layout


class AttachmentFormConstructor:
    def __init__(self, form: QDialog, operation: str, parent):
        self.parent_logic = MainWindowLogic(parent)
        self.form = form
        with open('Gui/QSS/attachment_form.qss', 'r') as f:
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
        self.form.exec_()

    def create_details_panel(self, label):
        sql_query_document_type_rows = QUERY_SELECT_ALL_DOCUMENTS
        rows = DbMan.show_items(sql_query_document_type_rows)

        v_layout = QVBoxLayout()

        document_type_combo = QComboBox()
        for row in rows:
            document_type_combo.addItem(row[0])

        document_type_combo.setCurrentIndex(-1)
        doc_type_item = create_item_panel(document_type_combo, "Załącznik")
        original = create_item_panel(QCheckBox(), "Oryginał")
        szt = QSpinBox()
        szt.setMinimum(1)
        quantity = create_item_panel(szt, "Sztuk")

        v_layout.addLayout(doc_type_item)
        v_layout.addLayout(original)
        v_layout.addLayout(quantity)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(v_layout)
        self.form.layout().addWidget(groupbox)

    def create_attachment_notice_panel(self, label):
        layout = QVBoxLayout()
        attachment_notice_label = QLabel("Uwagi")
        attachment_notice_edit = QPlainTextEdit()
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
        form_data = self.form.edit_controls
        self.parent_logic.attachment_logic.button_clicked(form_data, self.operation)
