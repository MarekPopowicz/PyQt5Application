import os
import re
import sys

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


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)


def read_doc_lines(path_file_name):
    """ Return list of file document's paragraphs """
    doc_line_list = []
    try:
        with open(path_file_name) as file:
            doc = file.readlines()
            for line in doc:
                doc_line_list.append(line.rstrip('\n'))
    except OSError:
        pass

    return doc_line_list


def write_to_file(path_file_name, data_to_write, mode):
    """ write document to file """
    try:
        with open(path_file_name, mode=mode, encoding='utf8') as file:
            file.write(data_to_write)
    except OSError:
        return False

    return True

