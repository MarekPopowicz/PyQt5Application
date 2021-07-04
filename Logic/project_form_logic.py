from Logic.Model.project_model import Project
import Data.db_query_commands as dbQry
from Data.db_manager import DBManager as DbMan


class ProjectFormLogic:
    def __init__(self):
        self.project = Project()
        user_data = self.get_user()
        if user_data is not None:
            self.user = list(self.get_user()[0])
        else:
            self.user = None

    def button_clicked(self, data, operation_type):
        self.set_project(data)

        if operation_type == 'add':
            if self.add_project():
                return self.project.id
            else:
                return 0
        else:
            if self.update_project(data[0]['Project_id']):
                return True
            else:
                return False

    def set_project(self, data):
        sap_info = data[0]
        self.project.nr_sap = sap_info['Nr_projektu'].text()
        self.project.nr_psp = sap_info['Regulacja'].text()
        self.project.nr_sap_work_hours = sap_info['Roboczogodziny'].text()

        if self.user is not None:
            self.project.engineer_name = self.user[0]

        project_title = data[1]
        if project_title['Priorytet'].isChecked():
            self.project.project_priority = 1
        else:
            self.project.project_priority = 0
        self.project.up_type = project_title['Dokument'].currentText()
        self.project.up_no = project_title['Nr'].text()
        self.project.up_date = project_title['z_dnia'].text()

        radio_buttons = data[2]
        for radio_button in radio_buttons:
            if radio_buttons[radio_button].isChecked():
                self.project.task_type = radio_button
                break

        main_device = data[3]
        self.project.main_device = main_device['Urządzenie_wiodące'].currentText()

        location = data[4]
        self.project.place = location['Miejscowość'].currentText()
        self.project.street = location['Ulica'].currentText()

        notice = data[5]
        self.project.notice = notice['Uwagi'].toPlainText()

    def update_project(self, project_id: str):
        query = dbQry.QUERY_UPDATE_PROJECT
        qry = query.replace('id_value', str(project_id))
        qry = qry.replace('nr_sap_value', self.project.nr_sap)
        qry = qry.replace('nr_psp_value', self.project.nr_psp)
        qry = qry.replace('nr_sap_work_hours_value', self.project.nr_sap_work_hours)
        qry = qry.replace('project_priority_value', str(self.project.project_priority))
        qry = qry.replace('task_type_value', self.project.task_type)
        qry = qry.replace('task_name_value', self.project.main_device)
        qry = qry.replace('place_value', self.project.place)
        qry = qry.replace('street_value', self.project.street)
        qry = qry.replace('up_type_value', self.project.up_type)
        qry = qry.replace('up_no_value', self.project.up_no)
        qry = qry.replace('notice_value', self.project.notice)
        result = DbMan.update_item(qry)
        return result

    def add_project(self):
        query = dbQry.QUERY_INSERT_PROJECT
        result = DbMan.add_new_items(query, (self.project.nr_sap,
                                             self.project.nr_psp,
                                             self.project.nr_sap_work_hours,
                                             self.project.project_priority,
                                             self.project.task_type,
                                             self.project.main_device,
                                             self.project.place,
                                             self.project.street,
                                             self.project.engineer_name,
                                             self.project.up_type,
                                             self.project.up_no,
                                             self.project.notice,
                                             ))
        if result > 0:
            self.project.id = result
            return True
        else:
            return False

    @staticmethod
    def delete_project(project_id: str):
        query = dbQry.QUERY_DELETE_PROJECT
        qry = query.replace('?', project_id)
        result = DbMan.delete_item(qry)
        return result

    @staticmethod
    def get_user():
        query = dbQry.QUERY_SELECT_USER
        result = DbMan.show_items(query)
        if len(result) > 0:
            return result
        else:
            return None

    def get_project(self, project_id: str):
        query = dbQry.QUERY_SELECT_PROJECT
        qry = query.replace('?', project_id)
        result = DbMan.show_items(qry)
        if result is not None:
            project_data = list(result[0])
            self.project.id = int(project_id)
            self.project.nr_sap = project_data[0]
            self.project.nr_psp = project_data[1]
            self.project.nr_sap_work_hours = project_data[2]
            self.project.project_priority = project_data[3]
            self.project.main_device = project_data[4]
            self.project.task_type = project_data[5]
            self.project.place = project_data[6]
            self.project.street = project_data[7]
            self.project.engineer_name = project_data[8]
            self.project.registration_date = project_data[9]
            self.project.up_type = project_data[10]
            self.project.up_no = project_data[11]
            self.project.notice = project_data[12]

            return self.project
        else:
            return None

    @staticmethod
    def get_projects_list():
        projects_list = []
        query = dbQry.QUERY_SELECT_ALL_PROJECTS
        projects = DbMan.show_items(query)
        if len(projects) > 0:
            for project in projects:
                projects_list.append(f'{project[0]}.{project[1]}')
        return projects_list
