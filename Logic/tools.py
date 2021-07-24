import re
from Logic.device_form_logic import DeviceFormLogic


def test_data(pattern, test_string, length=0):
    result = re.match(pattern, test_string)
    if result:
        if length == len(test_string) or length == 0:
            return True
    else:
        return False


def data_export_prepare(project, tasks, attachments):
    application = {
        "projekt": project,
        "dzialki": tasks,
        "urzadzenia": [DeviceFormLogic.get_devices_data(task[0]) for task in tasks],
        "zalaczniki": attachments
    }

    return application
