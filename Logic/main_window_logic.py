from PyQt5.QtWidgets import QTextBrowser, QListWidget, QTableWidgetItem, QTableWidget
import Gui.Components.constants as Const
from Logic.attachment_form_logic import AttachmentFormLogic
from Logic.device_form_logic import DeviceFormLogic
from Logic.project_form_logic import ProjectFormLogic
from Logic.task_form_logic import TaskFormLogic
from Logic.application_form_logic import ApplicationFormLogic
from Logic.user_form_logic import UserFormLogic

FONT_SIZE = '15px'
LABEL_COLOR = 'black'
VALUE_COLOR = 'darkblue'
FONT_WEIGHT_LABEL = 'bold'
FONT_WEIGHT_VALUE = 'normal'


class MainWindowLogic:
    def __init__(self, main_window):
        self.parent = main_window
        self.project_logic = ProjectFormLogic()
        self.task_logic = TaskFormLogic()
        self.device_logic = DeviceFormLogic()
        self.attachment_logic = AttachmentFormLogic()
        self.application_logic = ApplicationFormLogic()
        self.user_logic = UserFormLogic()

    def update_project_view_list(self, operation_type):
        project_list = self.project_logic.get_projects_list()
        list_widget = self.parent.findChild(QListWidget, 'list_widget')
        row = list_widget.currentRow()
        if len(project_list) > 0:
            list_widget.clear()
            list_widget.addItems(project_list)
            if operation_type == 'set':
                list_widget.setCurrentRow(0)
            elif operation_type == 'add':
                list_widget.setCurrentRow(list_widget.count() - 1)
            else:
                list_widget.setCurrentRow(row)
        else:
            list_widget.clear()

    def search_project_view_list(self, search_string: str):
        project_list = self.project_logic.search_projects_list(search_string)
        list_widget = self.parent.findChild(QListWidget, 'list_widget')
        if len(project_list) > 0:
            list_widget.clear()
            list_widget.addItems(project_list)
            list_widget.setCurrentRow(0)
            return project_list[0]
        else:
            return ''

    def update_task_table_view(self, operation_type, task_id):
        task_table_widget = self.parent.findChild(QTableWidget, Const.TASK_TITLE)

        if operation_type == 'set':
            tasks_list = self.task_logic.get_tasks_list(str(self.parent.current_project_id))
            task_table_widget.setRowCount(0)
            if len(tasks_list) > 0:
                task_table_widget.object_id = int(tasks_list[0][0])
                for task in tasks_list:
                    table_item_appender(task_table_widget, task)
                task_table_widget.selectRow(0)
            else:
                task_table_widget.object_id = int(task_id)

        if operation_type == 'edit':
            row = task_table_widget.currentRow()
            tasks_list = self.task_logic.get_tasks_list(str(self.parent.current_project_id))
            task_table_widget.setRowCount(0)
            if len(tasks_list) > 0:
                task_table_widget.object_id = int(task_id)
                for task in tasks_list:
                    table_item_appender(task_table_widget, task)
                task_table_widget.selectRow(row)

        if operation_type == 'add':
            task = self.task_logic.get_task(str(task_id))
            if task is not None:
                task_data = (
                    task.id,
                    task.register_no,
                    task.parcel_no,
                    task.sheet_no,
                    task.area_name,
                    task.owner_data,
                    task.notice
                )
                table_item_appender(task_table_widget, task_data)
                task_table_widget.object_id = int(task_id)
                task_table_widget.selectRow(task_table_widget.rowCount() - 1)

    def update_device_table_view(self, operation_type, device_id):
        current_task_id = self.parent.findChild(QTableWidget, Const.TASK_TITLE).object_id
        device_table_widget = self.parent.findChild(QTableWidget, Const.DEVICE_TITLE)

        if operation_type == 'set':
            if current_task_id != 0:
                device_list = self.device_logic.get_device_list(str(current_task_id))
                device_table_widget.setRowCount(0)
                if len(device_list) > 0:
                    device_table_widget.object_id = int(device_list[0][0])
                    for device in device_list:
                        table_item_appender(device_table_widget, device)
                    device_table_widget.selectRow(0)
                else:
                    device_table_widget.object_id = int(device_id)

        if operation_type == 'add':
            device = self.device_logic.get_device(str(device_id))
            if device is not None:
                device_data = (
                    device.id,
                    device.device_type,
                    device.device_long,
                    device.device_width,
                    device.regulation_type,
                    device.notice
                )
                table_item_appender(device_table_widget, device_data)
                device_table_widget.object_id = int(device_id)
                device_table_widget.selectRow(device_table_widget.rowCount() - 1)

        if operation_type == 'edit':
            row = device_table_widget.currentRow()
            device_list = self.device_logic.get_device_list(str(current_task_id))
            device_table_widget.setRowCount(0)
            if len(device_list) > 0:
                device_table_widget.object_id = int(device_id)
                for device in device_list:
                    table_item_appender(device_table_widget, device)
                device_table_widget.selectRow(row)

    def update_attachment_table_view(self, operation_type, attachment_id):
        attachment_table_widget = self.parent.findChild(QTableWidget, Const.ATTACHMENT_TITLE)

        if operation_type == 'set':
            if self.parent.current_project_id != 0:
                attachment_list = self.attachment_logic.get_attachment_list(str(self.parent.current_project_id))
                attachment_table_widget.setRowCount(0)
                if len(attachment_list) > 0:
                    set_attachment_table_widget(attachment_list, attachment_table_widget)
                    attachment_table_widget.selectRow(0)
                else:
                    attachment_table_widget.object_id = int(attachment_id)

        if operation_type == 'add':
            attachment = self.attachment_logic.get_attachment(str(attachment_id))
            if attachment is not None:
                if attachment.document_original == 1:
                    attachment.document_original = 'Tak'
                else:
                    attachment.document_original = 'Nie'

                attachment_data = (
                    attachment.id,
                    attachment.document_name,
                    attachment.document_original,
                    attachment.document_count,
                    attachment.notice
                )
                table_item_appender(attachment_table_widget, attachment_data)
                attachment_table_widget.object_id = int(attachment_id)
                attachment_table_widget.selectRow(attachment_table_widget.rowCount() - 1)

        if operation_type == 'edit':
            row = attachment_table_widget.currentRow()
            attachment_list = self.attachment_logic.get_attachment_list(str(self.parent.current_project_id))
            attachment_table_widget.setRowCount(0)
            if len(attachment_list) > 0:
                set_attachment_table_widget(attachment_list, attachment_table_widget)
                attachment_table_widget.object_id = int(attachment_id)
                attachment_table_widget.selectRow(row)

    def update_project_txt_browser(self):
        txt_bsr_project = self.parent.findChild(QTextBrowser, 'txt_bsr_project')
        if self.parent.current_project_id == -1:
            txt_bsr_project.clear()
        else:
            project = self.project_logic.get_project(str(self.parent.current_project_id))
            if project is not None:
                set_project_txt_browser_data(project, txt_bsr_project)
            else:
                return


def set_project_txt_browser_data(project, txt_bsr: QTextBrowser):
    nr_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Nr wniosku: </font>'
    nr_value = f'<font style = "color:red; font-weight: {FONT_WEIGHT_VALUE}">{project.id}/{project.registration_date[:4]}</font> '
    nr_sap_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Projekt: </font>'
    nr_sap = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.nr_sap}</font>'
    regulacja_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Regulacja: </font>'
    regulacja_value = f'<font style =  "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.nr_psp}</font>'
    roboczogodziny_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Roboczogodziny: </font>'
    roboczogodziny_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.nr_sap_work_hours}</font> '

    wnioskodawca_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Wnioskodawca: </font>'
    wnioskodawca_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.engineer_name}</font> '

    rejestracja_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Data: </font>'
    rejestracja_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.registration_date}</font> '

    priorytet_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Priorytet: </font>'
    if project.project_priority == 1:
        value = 'TAK'
        color = 'red'
    else:
        value = 'NIE'
        color = VALUE_COLOR

    priorytet_value = f'<font style = "color:{color}; font-weight: {FONT_WEIGHT_VALUE}">{value}</font>'

    task_type_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Zakres: </font>'
    task_type_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.task_type}</font>'

    main_device_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Urządzenie: </font>'
    main_device_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.main_device}</font>'

    up_type_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Podstawa: </font>'
    up_type_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.up_type}</font>'

    up_no_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Nr: </font>'
    up_no_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.up_no}</font>'

    up_date_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}"> z dn.: </font>'
    up_date_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.up_date}</font>'

    place_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Lokalizacja: </font>'
    place_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.place}</font>'

    street_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Ulica: </font>'
    street_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.street}</font>'

    notice_label = f'<font style = "color:{LABEL_COLOR}; font-weight: {FONT_WEIGHT_LABEL}">Informacje dodatkowe: </font>'
    notice_value = f'<font style = "color:{VALUE_COLOR}; font-weight: {FONT_WEIGHT_VALUE}">{project.notice}</font>'

    line_1 = f'<div>{nr_sap_label} {nr_sap} {nr_label} {nr_value} {wnioskodawca_label} {wnioskodawca_value} ' \
             f'{rejestracja_label} {rejestracja_value}</div> '

    line_2 = f'<div>{regulacja_label} {regulacja_value} {roboczogodziny_label} {roboczogodziny_value}</div>'

    line_3 = f'<div>{task_type_label} {task_type_value} {main_device_label} {main_device_value}</div>'

    line_4 = f'<div>{up_type_label} {up_type_value} {up_no_label} {up_no_value} {up_date_label} {up_date_value} ' \
             f'{priorytet_label} {priorytet_value}</div>'

    line_5 = f'<div>{place_label} {place_value} {street_label} {street_value}</div>'

    line_6 = f'<p>{notice_label} {notice_value}</p>'

    text = f'<div style = "font-size: {FONT_SIZE}">{line_1}{line_2}{line_3}{line_4}{line_5}{line_6}</div>'

    txt_bsr.clear()
    txt_bsr.setText(text)


def set_attachment_table_widget(attachment_list, attachment_table_widget):
    attachment_table_widget.object_id = int(attachment_list[0][0])
    for attachment in attachment_list:
        a = list(attachment)
        if a[2] == 1:
            a[2] = 'Tak'
        else:
            a[2] = 'Nie'
        table_item_appender(attachment_table_widget, a)


def table_item_appender(table, *args):
    def set_columns(length, pos):
        if pos == length - 1:
            table.setItem(table.rowCount() - 1, pos, QTableWidgetItem(str(args[0][pos])))

            table.setRowHeight(table.rowCount() - 1, 25)
        else:
            table.setItem(table.rowCount() - 1, pos, QTableWidgetItem(str(args[0][pos])))
            set_columns(length, pos + 1)

    table.insertRow(table.rowCount())
    set_columns(table.columnCount(), 0)
    table.horizontalHeader().setStretchLastSection(True)


