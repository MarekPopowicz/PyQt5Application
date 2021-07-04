from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QInputDialog, QDesktopWidget


class InputWindow(QWidget):

    def __init__(self, dict_name, text):
        super().__init__()
        self.name = dict_name
        self.center()
        self.selected_item_value = text
        self.user_answer = self.get_text()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def get_text(self):
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.resize(500, 100)

        if self.selected_item_value == '':
            dlg.setWindowTitle("Dodaj")
            self.setWindowIcon(QIcon('Images/star.png'))
        else:
            dlg.setWindowTitle("Edytuj")
            self.setWindowIcon(QIcon('Images/pencil.png'))
            dlg.setTextValue(self.selected_item_value)
        if self.name == 'Zadania':
            dlg.setLabelText('Zadanie:')
        elif self.name == 'Ulice':
            dlg.setLabelText('Ulica:')
        elif self.name == 'Miejscowości':
            dlg.setLabelText('Miejscowość:')
        elif self.name == 'Urządzenia':
            dlg.setLabelText('Urządzenie:')
        elif self.name == 'Dokumenty':
            dlg.setLabelText('Dokument:')

        ok = dlg.exec_()
        value = dlg.textValue()
        if ok == dlg.Accepted and value != '':
            # print(value)
            return value
        self.close()
