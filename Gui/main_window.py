import sys

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QAction, QDesktopWidget, QHBoxLayout, QVBoxLayout, QListWidget, \
    QGroupBox, QWidget, QPushButton, QTextBrowser, QLineEdit, QMessageBox, QTableWidget

import Gui.Components.table_view_panel as tblViewPnl
from Data.db_manager import DBManager
from Gui.Components.msg_dialogs import MsgBox
from Gui.Components.table_view_buttons_panel import ButtonPanel
from Gui.Constructors.user_form_constructor import UserFormConstructor
from Gui.dict_window import DictionaryWindow
from Gui.form_window import WindowManager
import Gui.Components.constants as Const
from Logic.main_window_logic import MainWindowLogic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        with open('Gui/QSS/main_window.qss', 'r') as f:
            self.setStyleSheet(f.read())
        self.logic = MainWindowLogic(self)
        self.current_project_id = -1
        self.setWindowTitle(Const.APP_NAME)
        self.setMinimumWidth(1200)
        self.setWindowIcon(QIcon(Const.APP_ICON))
        self.main_widget = QWidget(self)
        self.search_line_edit = QLineEdit()
        self.center()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignBottom)
        self.create_menu()
        self.create_listview_panel()
        self.create_details_panel()
        self.create_buttons_panel()
        self.main_layout.addLayout(self.right_layout)
        self.set_data()
        self.creator_init_flag = False
        if not DBManager.if_user_exists():
            MsgBox('ok_dialog', 'Użytkownik',
                   'Wykryto brak użytkownika\nDalsze korzystanie z aplikacji wymaga rejestracji użytkownika.',
                   QIcon(Const.APP_ICON))
            if user_window() > 0:
                self.show()
            else:
                sys.exit()
        else:
            self.show()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft().x(), 20)

    def create_menu(self):
        main_menu = self.menuBar()

        exit_action = QAction(QIcon(Const.POWER_BUTTON_ICON), 'Wyjdź', self)
        exit_action.triggered.connect(self.on_exit)
        exit_action.setShortcut("Ctrl+Q")
        main_menu.addAction(exit_action)

        dict_menu = main_menu.addMenu('Słowniki')
        dict_task_action = QAction(QIcon(Const.TASK_ICON), Const.TASKS, self)
        dict_menu.addAction(dict_task_action)
        dict_task_action.triggered.connect(lambda: show_dictionary_window(Const.TASKS))

        dict_street_action = QAction(QIcon(Const.STREET_ICON), Const.STREETS, self)
        dict_menu.addAction(dict_street_action)
        dict_street_action.triggered.connect(lambda: show_dictionary_window(Const.STREETS))

        dict_place_action = QAction(QIcon(Const.PLACE_ICON), Const.PLACES, self)
        dict_menu.addAction(dict_place_action)
        dict_place_action.triggered.connect(lambda: show_dictionary_window(Const.PLACES))

        dict_device_action = QAction(QIcon(Const.DEVICE_ICON), Const.DEVICES, self)
        dict_menu.addAction(dict_device_action)
        dict_device_action.triggered.connect(lambda: show_dictionary_window(Const.DEVICE_TITLE))

        dict_document_action = QAction(QIcon(Const.ATTACHMENT_ICON), Const.DOCUMENTS, self)
        dict_menu.addAction(dict_document_action)
        dict_document_action.triggered.connect(lambda: show_dictionary_window(Const.DOCUMENTS))

        settings_menu = main_menu.addMenu(Const.SETTINGS)

        data_action = QAction(QIcon(Const.DATABASE_ICON), Const.DATABASE, self)
        settings_menu.addAction(data_action)
        data_action.triggered.connect(lambda: data_base_manager_window())

        user_action = QAction(QIcon(Const.USER_ICON), Const.USER_TITLE, self)
        settings_menu.addAction(user_action)
        user_action.triggered.connect(lambda: user_window())

        info_action = QAction(Const.ABOUT, self)
        main_menu.addAction(info_action)
        info_action.triggered.connect(self.about)

    def create_listview_panel(self):
        list_widget = QListWidget()
        list_widget.setObjectName('list_widget')
        list_widget.setFont(QFont("Sanserif", 9))
        list_widget.clicked.connect(lambda: self.list_item_clicked(list_widget))

        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(5, 5, 5, 5)
        list_layout.addWidget(list_widget)

        self.search_line_edit.setPlaceholderText("Wpisz poszukiwaną frazę")
        list_layout.addWidget(self.search_line_edit)

        search_button = QPushButton("Szukaj")
        search_button.setToolTip("Szukaj wybranej frazy w numerze wniosku")
        list_layout.addWidget(search_button)
        search_button.setMinimumSize(Const.BUTTON_WIDTH, Const.BUTTON_HEIGHT)
        search_icon = QIcon(Const.SEARCH_ICON)
        search_button.setIcon(search_icon)
        search_button.clicked.connect(self.button_search_clicked)

        groupbox_list = QGroupBox(Const.APPLICATIONS)
        groupbox_list.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox_list.setMaximumWidth(240)
        groupbox_list.setLayout(list_layout)
        self.main_layout.addWidget(groupbox_list)

    def create_details_panel(self):
        task_table_columns_names = ['Id', ' Księga Wieczysta ', ' Nr dz.', ' AM ', ' Obręb ',
                                    ' Kontakt z właścicielem ', ' Uwagi ']
        device_table_columns_names = ['Id', ' Urządzenie ', ' Dł. ', ' Szer. ', ' Regulacja ', ' Uwagi ']
        document_table_columns_names = ['Id', ' Dokument ', ' Oryg. ', ' Szt. ', ' Uwagi ']

        # TextBrowser Widget Creation

        # Create layout
        txt_bsr_layout = QHBoxLayout()
        txt_bsr_layout.setContentsMargins(5, 5, 5, 5)

        # Create text_browser widget
        txt_bsr_project = QTextBrowser()
        txt_bsr_project.setObjectName('txt_bsr_project')

        project_icon = QIcon(Const.PROJECT_ICON)
        button_panel = ButtonPanel()
        button_panel.add_button.clicked.connect(lambda: self.button_clicked("add", Const.PROJECT_TITLE, project_icon))
        button_panel.edit_button.clicked.connect(lambda: self.button_clicked("edit", Const.PROJECT_TITLE, project_icon))
        button_panel.del_button.clicked.connect(
            lambda: self.button_clicked("delete", Const.PROJECT_TITLE, project_icon))

        # Add text_browser widget to layout
        txt_bsr_layout.addWidget(txt_bsr_project)
        txt_bsr_layout.addWidget(button_panel)

        # Create group_box
        groupbox_txt_bsr_project = QGroupBox(Const.PROJECT_TITLE)
        groupbox_txt_bsr_project.setStyleSheet('QGroupBox {font-weight: bold}')

        # Add layout to group_box
        groupbox_txt_bsr_project.setLayout(txt_bsr_layout)

        # Add group_box to higher level layout
        self.right_layout.addWidget(groupbox_txt_bsr_project)

        # Tasks TableView Widget Creation
        task_panel = tblViewPnl.TablePanel(Const.TASK_TITLE, task_table_columns_names)
        task_panel.table_view.itemClicked.connect(self.task_table_onclick)
        task_panel.table_view.setColumnWidth(1, 140)
        task_panel.table_view.setColumnWidth(4, 100)
        location_icon = QIcon(Const.LOCATION_ICON)
        task_panel.button_panel.add_button.clicked.connect(
            lambda: self.button_clicked("add", Const.TASK_TITLE, location_icon))
        task_panel.button_panel.edit_button.clicked.connect(
            lambda: self.button_clicked("edit", Const.TASK_TITLE, location_icon))
        task_panel.button_panel.del_button.clicked.connect(
            lambda: self.button_clicked("delete", Const.TASK_TITLE, location_icon))

        # Add group_box to higher level layout
        self.right_layout.addWidget(task_panel.groupbox_table_view)

        # Devices TableView Widget Creation
        device_panel = tblViewPnl.TablePanel(Const.DEVICE_TITLE, device_table_columns_names)
        device_panel.table_view.itemClicked.connect(self.device_table_onclick)
        device_panel.table_view.setColumnWidth(1, 250)
        device_panel.table_view.setColumnWidth(2, 50)
        device_panel.table_view.setColumnWidth(3, 50)
        device_panel.table_view.setColumnWidth(4, 200)
        device_icon = QIcon(Const.DEVICE_ICON)
        device_panel.button_panel.add_button.clicked.connect(
            lambda: self.button_clicked("add", Const.DEVICE_TITLE, device_icon))
        device_panel.button_panel.edit_button.clicked.connect(
            lambda: self.button_clicked("edit", Const.DEVICE_TITLE, device_icon))
        device_panel.button_panel.del_button.clicked.connect(
            lambda: self.button_clicked("delete", Const.DEVICE_TITLE, device_icon))

        # Add group_box to higher level layout
        self.right_layout.addWidget(device_panel.groupbox_table_view)

        # Documents TableView Widget Creation
        document_panel = tblViewPnl.TablePanel(Const.ATTACHMENT_TITLE, document_table_columns_names)
        document_panel.table_view.itemClicked.connect(self.attachment_table_onclick)
        document_panel.table_view.setColumnWidth(1, 250)
        document_icon = QIcon(Const.DOCUMENT_ICON)
        document_panel.button_panel.add_button.clicked.connect(
            lambda: self.button_clicked("add", Const.ATTACHMENT_TITLE, document_icon))
        document_panel.button_panel.edit_button.clicked.connect(
            lambda: self.button_clicked("edit", Const.ATTACHMENT_TITLE, document_icon))
        document_panel.button_panel.del_button.clicked.connect(
            lambda: self.button_clicked("delete", Const.ATTACHMENT_TITLE, document_icon))
        # Add group_box to higher level layout
        self.right_layout.addWidget(document_panel.groupbox_table_view)

    def task_table_onclick(self):
        task_table_widget = self.findChild(QTableWidget, Const.TASK_TITLE)
        row = task_table_widget.currentRow()
        task_table_widget.object_id = int(task_table_widget.item(row, 0).text())
        self.logic.update_device_table_view('set', -1)

    def device_table_onclick(self):
        device_table_widget = self.findChild(QTableWidget, Const.DEVICE_TITLE)
        row = device_table_widget.currentRow()
        device_table_widget.object_id = int(device_table_widget.item(row, 0).text())

    def attachment_table_onclick(self):
        attachment_table_widget = self.findChild(QTableWidget, Const.ATTACHMENT_TITLE)
        row = attachment_table_widget.currentRow()
        attachment_table_widget.object_id = int(attachment_table_widget.item(row, 0).text())

    def create_buttons_panel(self):
        pdf_icon = QIcon(Const.PRINT_PDF_ICON)
        new_icon = QIcon(Const.NEW_ICON)

        button_print = QPushButton("Drukuj")
        button_print.setToolTip("Drukuj wybrany wniosek do pliku PDF")
        button_print.setMinimumSize(Const.BUTTON_WIDTH, Const.BUTTON_HEIGHT)
        button_print.setIcon(pdf_icon)
        button_print.clicked.connect(lambda: print_button_clicked())

        button_new = QPushButton("Nowy")
        button_new.setToolTip("Kreator nowego wniosku")
        button_new.setMinimumSize(Const.BUTTON_WIDTH, Const.BUTTON_HEIGHT)
        button_new.setIcon(new_icon)
        button_new.clicked.connect(self.new_button_clicked)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        buttons_layout.addWidget(button_new)
        buttons_layout.addWidget(button_print)

        groupbox_buttons = QGroupBox()
        groupbox_buttons.setMaximumHeight(75)
        groupbox_buttons.setLayout(buttons_layout)
        self.right_layout.addWidget(groupbox_buttons)

    @pyqtSlot()
    def on_exit(self):
        self.close()

    def button_search_clicked(self):
        if self.search_line_edit.text() == '':
            MsgBox('error_dialog', 'Szukaj', 'Nie wprowadzono frazy do znalezienia.', QIcon(Const.SEARCH_ICON))
        else:
            pass
        self.search_line_edit.setText('')

    def about(self):
        QMessageBox.about(self, "O programie",
                          "Aplikacja <b>'Twoja Terenówka'</b> to narzędzie "
                          "do tworzenia cyfrowego <b>wniosku o regulację terenowo-prawną.</b> "
                          "<br/>"
                          "Zapewnia kontrolę kompletności przekazywanych informacji, oraz "
                          "zapisaniu całości w bazie danych na stacji roboczej użytkownika.")

    def new_button_clicked(self):
        self.creator_init_flag = True
        WindowManager(Const.PROJECT_TITLE, QIcon(Const.PROJECT_ICON), "add", self)

    def button_clicked(self, operation_type, panel_name, icon: QIcon):
        task_id = self.findChild(QTableWidget, Const.TASK_TITLE).object_id
        device_id = self.findChild(QTableWidget, Const.DEVICE_TITLE).object_id
        attachment_id = self.findChild(QTableWidget, Const.ATTACHMENT_TITLE).object_id

        # region Add and Edit operation
        if operation_type == 'add' or operation_type == 'edit':

            # Do not take any action if there is no project.
            if (
                    panel_name == Const.TASK_TITLE or panel_name == Const.DEVICE_TITLE or panel_name == Const.ATTACHMENT_TITLE) \
                    and (self.current_project_id == -1):
                MsgBox('error_dialog', panel_name, 'Brak projektu uniemożliwia wykonanie dalszych operacji.\n'
                                                   'Należy najpierw zarejestrować projekt.', QIcon(Const.APP_ICON))
                return

            if panel_name == Const.PROJECT_TITLE and operation_type == 'edit' and self.current_project_id == -1:
                MsgBox('error_dialog', panel_name, 'Należy najpierw zarejestrować projekt.', QIcon(Const.APP_ICON))
                return

            message = 'Brak danych do edycji.'
            if panel_name == Const.TASK_TITLE and operation_type == 'edit' and task_id <= 0:
                MsgBox('error_dialog', panel_name, message, QIcon(Const.APP_ICON))
                return

            if panel_name == Const.DEVICE_TITLE and operation_type == 'add' and task_id <= 0:
                MsgBox('error_dialog', panel_name, 'Urządzenie jest zlokalizowane na działce.\nNależy najpierw '
                                                   'zarejestrować działkę.', QIcon(Const.APP_ICON))
                return

            if panel_name == Const.DEVICE_TITLE and operation_type == 'edit' and device_id <= 0:
                MsgBox('error_dialog', panel_name, message, QIcon(Const.APP_ICON))
                return

            if panel_name == Const.ATTACHMENT_TITLE and operation_type == 'edit' and attachment_id <= 0:
                MsgBox('error_dialog', panel_name, message, QIcon(Const.APP_ICON))
                return

            WindowManager(panel_name, icon, operation_type, self)
        # endregion

        # region Delete operation
        if operation_type == 'delete':
            # Do not take any actions if there is no project
            if self.current_project_id == -1:
                MsgBox('error_dialog', panel_name, 'Brak projektu uniemożliwia wykonanie tej operacji.\n'
                                                   'Należy najpierw zarejestrować projekt.', QIcon(Const.APP_ICON))
                return

            if panel_name == Const.PROJECT_TITLE:
                msg_warning = 'projekt ?\nUsunięcie spowoduje także utratę danych o działkach, urządzeniach i ' \
                              'załącznikach związanych z tym projektem.'

            elif panel_name == Const.TASK_TITLE:
                if task_id <= 0:
                    MsgBox('error_dialog', panel_name, 'Brak danych do usunięcia.', QIcon(Const.APP_ICON))
                    return
                msg_warning = 'działkę ?\nUsunięcie spowoduje także utratę danych o urządzeniach ' \
                              'związanych z działkami. '

            elif panel_name == Const.DEVICE_TITLE:
                if device_id <= 0:
                    MsgBox('error_dialog', panel_name, 'Brak danych do usunięcia.', QIcon(Const.APP_ICON))
                    return
                msg_warning = 'urządzenie ?'
            else:
                if attachment_id <= 0:
                    MsgBox('error_dialog', panel_name, 'Brak danych do usunięcia.', QIcon(Const.APP_ICON))
                    return
                msg_warning = 'załącznik ?'

            response = MsgBox("ok_cancel_dlg", f"{panel_name} :: Usunięcie", f"Pytanie:\n"
                                                                             f"Czy trwale usunąć {msg_warning}",
                              icon).last_user_answer

            if response:
                result = False
                if panel_name == Const.PROJECT_TITLE:
                    # Check if any tasks are out there
                    tasks_list = self.logic.task_logic.get_tasks_list(str(self.current_project_id))
                    # if so, delete every single task with its devices
                    if len(tasks_list) > 0:
                        for task in tasks_list:
                            self.delete_tasks(task[0])
                    # Delete all attachments
                    self.logic.attachment_logic.delete_attachments(str(self.current_project_id))
                    # Delete project
                    result = self.logic.project_logic.delete_project(str(self.current_project_id))

                if panel_name == Const.TASK_TITLE:
                    # Read id's no from first column in current table row

                    # task_table_widget = self.findChild(QTableWidget, Const.TASK_TITLE)
                    # new_index = task_table_widget.model().index(task_table_widget.currentRow(), 0)
                    # Id = task_table_widget.model().data(new_index)

                    result = self.delete_tasks(task_id)

                if panel_name == Const.DEVICE_TITLE:
                    result = self.logic.device_logic.delete_device(str(device_id))

                if panel_name == Const.ATTACHMENT_TITLE:
                    result = self.logic.attachment_logic.delete_attachment(str(attachment_id))

                if result:
                    MsgBox('ok_dialog', panel_name, 'Operacja zakończona sukcesem.', QIcon(Const.APP_ICON))

                    if panel_name == Const.PROJECT_TITLE:
                        self.set_data()

                    if panel_name == Const.TASK_TITLE:
                        self.logic.update_task_table_view('set', -1)
                        self.logic.update_device_table_view('set', -1)

                    if panel_name == Const.DEVICE_TITLE:
                        self.logic.update_device_table_view('set', -1)

                    if panel_name == Const.ATTACHMENT_TITLE:
                        self.logic.update_attachment_table_view('set', -1)
                else:
                    MsgBox('error_dialog', panel_name, 'Coś poszło nie tak...', QIcon(Const.APP_ICON))
        # endregion

    def delete_tasks(self, task_id):
        result = False
        device_list = self.logic.device_logic.get_device_list(str(task_id))
        if len(device_list) > 0:
            # Remove all devices na and then current task
            if self.logic.device_logic.delete_devices(str(task_id)):
                result = self.logic.task_logic.delete_task(str(task_id))
        else:
            result = self.logic.task_logic.delete_task(str(task_id))
        return result

    def set_data(self):
        project_list = self.logic.project_logic.get_projects_list()
        if len(project_list) > 0:
            first_item = project_list[0]
            end_index = first_item.find('.')
            self.current_project_id = first_item[0:end_index]

        else:
            self.current_project_id = -1

        self.logic.update_project_view_list('set')
        self.logic.update_project_txt_browser()
        self.logic.update_task_table_view('set', -1)
        self.logic.update_device_table_view('set', -1)
        self.logic.update_attachment_table_view('set', -1)

    def list_item_clicked(self, list_view: QListWidget):
        item = list_view.currentItem().text()
        end_index = item.find('.')
        project_id = item[0:end_index]
        self.current_project_id = project_id
        self.logic.update_project_txt_browser()
        self.logic.update_task_table_view('set', -1)
        self.logic.update_device_table_view('set', -1)
        self.logic.update_attachment_table_view('set', -1)


def user_window():
    return len(UserFormConstructor().logic.user.name)


def show_dictionary_window(dictionary_name):
    DictionaryWindow(dictionary_name)


def data_base_manager_window():
    pass


def print_button_clicked(self):
    pass
