from Logic.Model.device_model import Device


class DeviceFormLogic:
    def __init__(self):
        self.device = Device()

    def button_clicked(self, data, operation_type):
        self.set_project(data)

    def set_project(self, data):
        pass
