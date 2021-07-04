import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QCheckBox, QGroupBox, QLabel, QLineEdit, QComboBox, QVBoxLayout, \
    QRadioButton, QPlainTextEdit, QDateEdit, QPushButton
from Data.db_data import PROJECT_DOC_BASIS
from Data.db_manager import DBManager as DbMan
from Data.db_query_commands import QUERY_SELECT_ALL_TASK_TYPES, QUERY_SELECT_ALL_DEVICE_TYPES, \
    QUERY_SELECT_ALL_PLACES, QUERY_SELECT_ALL_STREETS
from Gui.Components.button_panel import ButtonPanel
from Gui.Components.msg_dialogs import MsgBox
from Gui.Components.searchable_combo import ExtendedComboBox
from Logic.main_window_logic import MainWindowLogic
import Gui.Components.constants as Const


class ProjectFormConstructor:
    def __init__(self, form: QDialog, operation: str, parent):
        self.parent_logic = MainWindowLogic(parent)
        self.form = form
        with open('Gui/QSS/project_form.qss', 'r') as f:
            self.form.setStyleSheet(f.read())
        self.operation = operation
        self.create_sap_info_panel('Identyfikacja SAP')
        self.create_project_title_panel('Podstawa')
        self.create_radio_box_panel('Przedmiot i zakres prac')
        self.create_project_location_panel('Lokalizacja')
        self.create_project_notice_panel('Informacje uzupełniajace')
        self.create_project_save_button()
        self.exec_project_form()

    def exec_project_form(self):
        self.form.adjustSize()
        current_width = self.form.width()
        current_height = self.form.height()
        self.form.setFixedSize(current_width, current_height)
        if self.operation == 'edit' and self.parent_logic.parent.current_project_id == -1:
            return
        elif self.operation == 'edit' and self.parent_logic.parent.current_project_id != -1:
            self.set_project_data()

        self.form.exec_()

    def create_radio_box_panel(self, label):
        radio_box = {}
        sql_query_tasks_type_rows = QUERY_SELECT_ALL_TASK_TYPES
        tasks_type_rows = DbMan.show_items(sql_query_tasks_type_rows)

        sql_query_devices_type_rows = QUERY_SELECT_ALL_DEVICE_TYPES
        devices_type_rows = DbMan.show_items(sql_query_devices_type_rows)

        # Create layout
        groupbox_layout = QVBoxLayout()
        check_box_layout = QHBoxLayout()
        combo_box_layout = QHBoxLayout()

        for row in tasks_type_rows:
            new_radio_button = QRadioButton(row[0])
            radio_box[row[0]] = new_radio_button

            # Add radiobutton widget to layout
            check_box_layout.addWidget(new_radio_button)

        radio_box[(tasks_type_rows[0])[0]].setChecked(True)

        self.form.edit_controls.append(radio_box)

        main_device = {}
        main_device_label = QLabel("Urządzenie wiodące")
        main_device_combo = QComboBox()
        main_device["Urządzenie_wiodące"] = main_device_combo

        self.form.edit_controls.append(main_device)

        for row in devices_type_rows:
            main_device_combo.addItem(row[0])

        main_device_combo.setCurrentIndex(1)
        combo_box_layout.addWidget(main_device_label)
        combo_box_layout.addWidget(main_device_combo)
        combo_box_layout.setAlignment(Qt.AlignLeft)
        groupbox_layout.addLayout(check_box_layout)
        groupbox_layout.addLayout(combo_box_layout)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')

        # Add layout to group_box
        groupbox.setLayout(groupbox_layout)

        # Add checkbox to form layout
        self.form.layout().addWidget(groupbox)

    def create_sap_info_panel(self, label):
        sap_info_panel_widgets = {}
        layout = QHBoxLayout()

        proj_no_label = QLabel("Nr projektu")
        proj_no_edit = QLineEdit()
        proj_no_edit.setPlaceholderText('np. I-WR-AO-2001234')
        proj_no_edit.setText('I-WR-')
        sap_info_panel_widgets['Nr_projektu'] = proj_no_edit

        proj_psp_label = QLabel("Regulacja")
        proj_psp_edit = QLineEdit()
        proj_psp_edit.setPlaceholderText('np. SPAK001')
        sap_info_panel_widgets['Regulacja'] = proj_psp_edit

        proj_rbg_label = QLabel("Roboczogodziny")
        proj_rbg_edit = QLineEdit()
        proj_rbg_edit.setPlaceholderText('np. PKNN001')
        sap_info_panel_widgets['Roboczogodziny'] = proj_rbg_edit

        self.form.edit_controls.append(sap_info_panel_widgets)

        layout.addWidget(proj_no_label)
        layout.addWidget(proj_no_edit)
        layout.addWidget(proj_psp_label)
        layout.addWidget(proj_psp_edit)
        layout.addWidget(proj_rbg_label)
        layout.addWidget(proj_rbg_edit)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(layout)
        self.form.layout().addWidget(groupbox)

    def create_project_title_panel(self, label):
        title_panel_widgets = {}

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        priority_checkbox = QCheckBox("Priorytet")
        title_panel_widgets['Priorytet'] = priority_checkbox
        proj_title_label = QLabel("Dokument")
        proj_title_combo = QComboBox()
        title_panel_widgets['Dokument'] = proj_title_combo
        proj_title_combo.addItems(PROJECT_DOC_BASIS)
        proj_title_combo.setCurrentIndex(0)

        doc_no_label = QLabel("Nr")
        doc_no_edit = QLineEdit()
        title_panel_widgets['Nr'] = doc_no_edit

        doc_date_label = QLabel("z dnia")
        doc_date_edit = QDateEdit()
        title_panel_widgets['z_dnia'] = doc_date_edit
        current_date = datetime.date.today()
        doc_date_edit.setDate(current_date)
        doc_date_edit.setMaximumWidth(120)

        self.form.edit_controls.append(title_panel_widgets)

        layout.addWidget(proj_title_label)
        layout.addWidget(proj_title_combo)
        layout.addWidget(doc_no_label)
        layout.addWidget(doc_no_edit)
        layout.addWidget(doc_date_label)
        layout.addWidget(doc_date_edit)

        layout.addWidget(priority_checkbox)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(layout)
        self.form.layout().addWidget(groupbox)

    def create_project_notice_panel(self, label):
        notice_panel_widgets = {}

        layout = QHBoxLayout()
        proj_notice_label = QLabel("Uwagi")
        proj_notice_edit = QPlainTextEdit()

        notice_panel_widgets['Uwagi'] = proj_notice_edit
        proj_notice_edit.lineWrapMode()
        proj_notice_edit.setMaximumHeight(110)

        self.form.edit_controls.append(notice_panel_widgets)

        layout.addWidget(proj_notice_label)
        layout.addWidget(proj_notice_edit)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(layout)
        self.form.layout().addWidget(groupbox)

    def create_project_location_panel(self, label):
        location_panel_widgets = {}

        sql_query_places_rows = QUERY_SELECT_ALL_PLACES
        places_rows = DbMan.show_items(sql_query_places_rows)

        sql_query_streets_rows = QUERY_SELECT_ALL_STREETS
        streets_rows = DbMan.show_items(sql_query_streets_rows)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        proj_location_label = QLabel("Miejscowość")
        proj_location_combo = ExtendedComboBox()
        location_panel_widgets["Miejscowość"] = proj_location_combo
        for row in places_rows:
            proj_location_combo.addItem(row[0])

        proj_location_combo.setCurrentIndex(-1)
        proj_street_label = QLabel("Ulica")
        proj_street_combo = ExtendedComboBox()
        location_panel_widgets["Ulica"] = proj_street_combo
        for row in streets_rows:
            proj_street_combo.addItem(row[0])

        proj_street_combo.setCurrentIndex(-1)
        proj_street_combo.setMinimumWidth(250)

        self.form.edit_controls.append(location_panel_widgets)

        layout.addWidget(proj_location_label)
        layout.addWidget(proj_location_combo)
        layout.addWidget(proj_street_label)
        layout.addWidget(proj_street_combo)

        groupbox = QGroupBox(label)
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(layout)
        self.form.layout().addWidget(groupbox)

    def create_project_save_button(self):
        button_panel = ButtonPanel(self.form)
        self.form = button_panel.form
        save_button = self.form.findChild(QPushButton, "Zapisz")
        save_button.clicked.connect(self.save_button_clicked)

    def save_button_clicked(self):
        project_id = 0
        form_data = self.form.edit_controls
        result = False
        if self.operation == 'edit':
            form_data[0]['Project_id'] = self.parent_logic.parent.current_project_id
            result = self.parent_logic.project_logic.button_clicked(form_data, self.operation)
        else:
            project_id = self.parent_logic.project_logic.button_clicked(form_data, self.operation)
            if project_id != 0:
                result = True

        if result:
            MsgBox('ok_dialog', 'Projekt', 'Operacja zakończona sukcesem.', QIcon(Const.APP_ICON))
            self.form.close()
            if self.operation == 'add':
                self.parent_logic.parent.current_project_id = project_id

            self.parent_logic.update_project_view_list(self.operation)
            self.parent_logic.update_project_txt_browser()
            self.parent_logic.update_task_table_view('set', -1)
        else:
            MsgBox('error_dialog', 'Projekt', 'Coś poszło nie tak...', QIcon(Const.APP_ICON))
            self.form.close()

    def set_project_data(self):
        project_id = self.parent_logic.parent.current_project_id
        project = self.parent_logic.project_logic.get_project(str(project_id))

        sap_info = self.form.edit_controls[0]
        sap_info['Nr_projektu'].setText(project.nr_sap)
        sap_info['Regulacja'].setText(project.nr_psp)
        sap_info['Roboczogodziny'].setText(project.nr_sap_work_hours)

        project_title = self.form.edit_controls[1]
        if project.project_priority == 1:
            project_title['Priorytet'].setChecked(True)
        project_title['Dokument'].setCurrentText(project.up_type)
        project_title['Nr'].setText(project.up_no)

        radio_boxes = self.form.edit_controls[2]
        for radio_box in radio_boxes:
            if radio_box == project.task_type:
                radio_boxes[radio_box].setChecked(True)
                break

        main_device = self.form.edit_controls[3]
        main_device['Urządzenie_wiodące'].setCurrentText(project.main_device)

        location = self.form.edit_controls[4]
        location['Miejscowość'].setCurrentText(project.place)
        location['Ulica'].setCurrentText(project.street)

        notice = self.form.edit_controls[5]
        notice['Uwagi'].setPlainText(project.notice)
