from Logic.Model.task_model import Task
import Data.db_query_commands as dbQry
from Data.db_manager import DBManager as DbMan


class TaskFormLogic:
    def __init__(self):
        self.task = Task()

    def button_clicked(self, data, operation_type):
        self.set_task(data)
        if operation_type == 'add':
            if self.add_task():
                return self.task.id
            else:
                return 0
        else:
            self.task.id = data[0]['task_id']
            if self.update_task():
                return self.task.id
            else:
                return 0

    def set_task(self, data):
        task_info = data[0]
        self.task.register_no = task_info['KW'].text()
        self.task.parcel_no = task_info['Dz.'].text()
        self.task.sheet_no = task_info['AM'].text()
        self.task.area_name = task_info['Obręb'].text()

        owner = data[1]
        self.task.owner_data = owner['Właściciel'].toPlainText()
        self.task.project_id = int(owner['Project_id'])

        notice = data[2]
        self.task.notice = notice['Uwagi'].toPlainText()

    def add_task(self):
        query = dbQry.QUERY_INSERT_TASK
        result = DbMan.add_new_items(query, (
            self.task.project_id,
            self.task.register_no,
            self.task.parcel_no,
            self.task.sheet_no,
            self.task.area_name,
            self.task.owner_data,
            self.task.notice,
        ))
        if result > 0:
            self.task.id = result
            return True
        else:
            return False

    def update_task(self):
        query = dbQry.QUERY_UPDATE_TASK
        qry = query.replace('id_value', str(self.task.id))
        qry = qry.replace('register_no_value', self.task.register_no)
        qry = qry.replace('parcel_no_value', self.task.parcel_no)
        qry = qry.replace('map_sheet_no_value', self.task.sheet_no)
        qry = qry.replace('area_name_value', self.task.area_name)
        qry = qry.replace('owner_data_value', self.task.owner_data)
        qry = qry.replace('notice_value', self.task.notice)
        result = DbMan.update_item(qry)
        return result

    def get_task(self, task_id):
        query = dbQry.QUERY_SELECT_TASK
        qry = query.replace('?', task_id)
        result = DbMan.show_items(qry)
        if len(result) > 0:
            self.task.id = result[0][0]
            self.task.register_no = result[0][1]
            self.task.parcel_no = result[0][2]
            self.task.sheet_no = result[0][3]
            self.task.area_name = result[0][4]
            self.task.owner_data = result[0][5]
            self.task.notice = result[0][6]
            return self.task
        else:
            return None

    @staticmethod
    def delete_task(task_id: str):
        query = dbQry.QUERY_DELETE_TASK
        qry = query.replace('?', task_id)
        result = DbMan.delete_item(qry)
        return result

    @staticmethod
    def get_tasks_list(project_id):
        query = dbQry.QUERY_SELECT_TASKS
        qry = query.replace('?', project_id)
        tasks = DbMan.show_items(qry)
        if len(tasks) > 0:
            return tasks
        else:
            return []
