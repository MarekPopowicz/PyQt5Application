import re
from Logic.device_form_logic import DeviceFormLogic


def test_code_data(pattern, test_string, length):
    result = re.match(pattern, test_string)
    if result and len(test_string) == length:
        return True
    else:
        return False


def test_data(pattern, test_string):
    result = re.match(pattern, test_string)
    if result:
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
