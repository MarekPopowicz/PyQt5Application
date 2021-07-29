import os
import sys
from pathlib import Path


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)


base_dir = resource_path("")
img_dir = resource_path("Images\\")

BUTTON_HEIGHT = 35
BUTTON_WIDTH = 150

PROJECT_TITLE = "Projekt"
TASK_TITLE = "Działki"
DEVICE_TITLE = "Urządzenia"
ATTACHMENT_TITLE = "Załączniki"
USER_TITLE = "Użytkownik"
PREVIEW_TITLE = "Podgląd Wydruku"

DBNAME = str(Path(base_dir).parents[0]) + '\\register.db'

SPLASH_IMAGE = img_dir + 'car.jpg'
APP_ICON = img_dir + 'suv-car.png'
USER_ICON = img_dir + 'user.png'
DATABASE_ICON = img_dir + 'database.png'
DEVICE_ICON = img_dir + 'electricity.png'
ATTACHMENT_ICON = img_dir + 'attachment.png'
DOCUMENT_ICON = img_dir + 'attach.png'
PLACE_ICON = img_dir + 'place.png'
LOCATION_ICON = img_dir + 'location.png'
STREET_ICON = img_dir + 'road.png'
TASK_ICON = img_dir + 'tasks.png'
POWER_BUTTON_ICON = img_dir + 'power-button.png'
SEARCH_ICON = img_dir + 'binoculars.png'
PROJECT_ICON = img_dir + 'project.png'
PRINT_PDF_ICON = img_dir + 'pdf.png'
SAVE_ICON = img_dir + 'save.png'
CANCEL_ICON = img_dir + 'cancel.png'
JSON_ICON = img_dir + 'json.png'
NEW_ICON = img_dir + 'star.png'
PREVIEW_ICON = img_dir + 'preview.png'
TAURON_LOGO = img_dir + 'logo.png'
MAN_ICON = img_dir + 'man.png'
PLUS_ICON = img_dir + 'plus.png'
PENCIL_ICON = img_dir + 'pencil.png'
DELETE_ICON = img_dir + 'delete.png'

TASKS = 'Zadania'
STREETS = 'Ulice'
PLACES = 'Miejscowości'
DEVICES = 'Urządzenia'
DOCUMENTS = 'Dokumenty'
SETTINGS = 'Ustawienia'
DATABASE = 'Reset Danych'
ABOUT = 'O programie'
APPLICATIONS = 'Wnioski'
APP_NAME = "Twoja Terenówka. (ver. 1.00)"
