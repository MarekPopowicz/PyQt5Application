from Logic.Model.device_model import Device
import Data.db_query_commands as dbQry
from Data.db_manager import DBManager as DbMan


class DeviceFormLogic:
    def __init__(self):
        self.device = Device()

    def button_clicked(self, data, operation_type):
        if len(data) > 0:
            self.set_project(data)
            if operation_type == 'add':
                return self.add_device()
            else:
                return self.update_device()

    def set_project(self, data):
        self.device.id = data[0]['Device_id']
        self.device.task_id = data[0]['Task_id']
        self.device.device_type = data[0]['Urządzenie'].currentText()
        self.device.device_long = data[0]['Długość'].text()
        self.device.device_width = data[0]['Szerokość'].text()
        self.device.regulation_type = data[1]['Tytuł'].currentText()
        self.device.notice = data[2]['Uwagi'].toPlainText()

    def add_device(self):
        query = dbQry.QUERY_INSERT_DEVICE
        result = DbMan.add_new_items(query, (
            self.device.task_id,
            self.device.device_type,
            self.device.device_long,
            self.device.device_width,
            self.device.regulation_type,
            self.device.notice
        ))
        if result is not None:
            self.device.id = result
            return result
        else:
            return 0

    def update_device(self):
        query = dbQry.QUERY_UPDATE_DEVICE
        qry = query.replace('id_value', str(self.device.id))
        qry = qry.replace('device_type_value', self.device.device_type)
        qry = qry.replace('device_width_value', self.device.device_width)
        qry = qry.replace('device_long_value', self.device.device_long)
        qry = qry.replace('regulation_type_value', self.device.regulation_type)
        qry = qry.replace('notice_value', self.device.notice)
        result = DbMan.update_item(qry)
        return result

    def get_device(self, device_id):
        query = dbQry.QUERY_SELECT_DEVICE
        qry = query.replace('?', device_id)
        result = DbMan.show_items(qry)
        if len(result) > 0:
            self.device.id = result[0][0]
            self.device.task_id = result[0][1]
            self.device.device_type = result[0][2]
            self.device.device_width = result[0][3]
            self.device.device_long = result[0][4]
            self.device.regulation_type = result[0][5]
            self.device.notice = result[0][6]
            return self.device
        else:
            return None

    @staticmethod
    def delete_device(device_id: str):
        query = dbQry.QUERY_DELETE_DEVICE
        qry = query.replace('?', device_id)
        result = DbMan.delete_item(qry)
        return result

    @staticmethod
    def delete_device(device_id: str):
        query = dbQry.QUERY_DELETE_DEVICE
        qry = query.replace('?', device_id)
        result = DbMan.delete_item(qry)
        return result

    @staticmethod
    def delete_devices(task_id: str):
        query = dbQry.QUERY_DELETE_DEVICES
        qry = query.replace('?', task_id)
        result = DbMan.delete_item(qry)
        return result

    @staticmethod
    def get_device_list(task_id):
        query = dbQry.QUERY_SELECT_DEVICES
        qry = query.replace('?', task_id)
        devices = DbMan.show_items(qry)
        if len(devices) > 0:
            return devices
        else:
            return []
