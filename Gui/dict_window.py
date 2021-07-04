from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidget, QTableWidgetItem, \
    QPushButton, QGroupBox, QAbstractItemView, QMessageBox
from Logic.dict_window_logic import DictionaryWindowLogic
from Gui.Components.dict_input_window import InputWindow
from Gui.Components.msg_dialogs import MsgBox


class DictionaryWindow(QDialog):
    def __init__(self, dictionary_name):
        super().__init__()
        with open('Gui/QSS/dict_form.qss', 'r') as f:
            self.setStyleSheet(f.read())
        self.add_icon = QIcon('Images/star.png')
        self.update_icon = QIcon('Images/pencil.png')
        self.delete_icon = QIcon('Images/delete.png')

        self.name = dictionary_name
        self.window_logic = DictionaryWindowLogic(self.name)

        self.groupbox = QGroupBox()
        self.add_button = QPushButton("Dodaj")
        self.del_button = QPushButton("Usuń")
        self.update_button = QPushButton("Edytuj")

        self.tableWidget = QTableWidget()

        self.resize(600, 500)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.set_window_title_and_icon()
        self.create_table()
        self.fill_table_with_data()
        self.set_buttons()
        self.exec_()

    def set_window_title_and_icon(self):
        self.setWindowTitle(self.name)
        if self.name == 'Zadania':
            self.setWindowIcon(QIcon('Images/tasks.png'))
        elif self.name == 'Ulice':
            self.setWindowIcon(QIcon('Images/road.png'))
        elif self.name == 'Miejscowości':
            self.setWindowIcon(QIcon('Images/place.png'))
        elif self.name == 'Urządzenia':
            self.setWindowIcon(QIcon('Images/electricity.png'))
        elif self.name == 'Dokumenty':
            self.setWindowIcon(QIcon('Images/attachment.png'))

    def create_table(self):
        font = QFont()
        font.setPointSize(9)

        self.tableWidget.setFont(font)
        self.vbox.addWidget(self.tableWidget)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem(self.name))

    def fill_table_with_data(self):
        for row_number, row_data in enumerate(self.window_logic.get_dictionary_items()):
            self.tableWidget.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.tableWidget.setCurrentCell(0, 0)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    def set_buttons(self):
        self.add_button.setIcon(self.add_icon)
        self.add_button.setMinimumHeight(40)
        self.add_button.clicked.connect(lambda: self.click_me(self.name, "add"))

        self.update_button.setIcon(self.update_icon)
        self.update_button.setMinimumHeight(40)
        self.update_button.clicked.connect(lambda: self.click_me(self.name, "update"))

        self.del_button.setIcon(self.delete_icon)
        self.del_button.setMinimumHeight(40)
        self.del_button.clicked.connect(lambda: self.click_me(self.name, "delete"))

        hbox = QHBoxLayout()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.update_button)
        hbox.addWidget(self.del_button)
        self.groupbox.setLayout(hbox)
        self.vbox.addWidget(self.groupbox)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(f"row :{currentQTableWidgetItem.row()}, col: {currentQTableWidgetItem.column()} "
                  f"text: {currentQTableWidgetItem.text()}")

    def click_me(self, dict_name, operation):
        current_cell_val = self.tableWidget.currentItem().text()
        if operation == 'delete':
            response = MsgBox("ok_cancel_dlg", "Usuń", f"Pytanie:\n"
                                                       f"Czy usunąć ze słownika element:\n"
                                                       f"'{current_cell_val}' ?",
                              self.delete_icon).last_user_answer

            if response:
                error = self.window_logic.delete_item(current_cell_val)
                if error is None:
                    # clear tableWidget
                    self.tableWidget.setRowCount(0)
                    # refill tableWidget with updated set of items
                    self.fill_table_with_data()
                    MsgBox('ok_dialog', "Usuń", 'Operacja zakończona sukcesem.', self.delete_icon)

        elif operation == "update":
            updated_item = InputWindow(dict_name, current_cell_val).user_answer

            if check_input_value("Edytuj", updated_item, self.update_icon):
                response = MsgBox("ok_cancel_dlg", "Edytuj",
                                  f"Pytanie:\nCzy zmienić wartość elementu:\n'{current_cell_val}'\n\n"
                                  f"na nową wartość:\n'{updated_item}'",
                                  self.update_icon).last_user_answer
                if response:
                    result = self.window_logic.update_item(current_cell_val, updated_item)
                    if result is None:
                        # clear tableWidget
                        self.tableWidget.setRowCount(0)
                        # refill tableWidget with updated set of items
                        self.fill_table_with_data()
                        MsgBox('ok_dialog', "Edytuj", 'Operacja zakończona sukcesem.', self.update_icon)
        else:
            new_item = InputWindow(dict_name, '').user_answer
            # user data validation
            if check_input_value("Dodaj", new_item, self.add_icon):
                # confirm decision
                MsgBox("ok_cancel_dlg", "Dodaj",
                       f"Pytanie:\nCzy dodać element: '{new_item}' do słownika ?",
                       self.add_icon)
                if QMessageBox.Ok == 1024:
                    result = self.window_logic.add_item(new_item)
                    if result is not None:
                        # clear tableWidget
                        self.tableWidget.setRowCount(0)
                        # refill tableWidget with updated set of items
                        self.fill_table_with_data()
                        MsgBox('ok_dialog', "Dodaj", 'Operacja zakończona sukcesem.', self.add_icon)


def check_input_value(operation_type, input_value, icon):
    if input_value is None or input_value == '':
        MsgBox('error_dialog', operation_type, 'Operacja została anulowana\n'
                                               'lub nie wprowadzono danych', icon)
        return False
    else:
        return True
