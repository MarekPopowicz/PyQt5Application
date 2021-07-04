import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QGroupBox, QHBoxLayout

import Gui.Components.constants as Const
from Gui.Components.msg_dialogs import MsgBox
from Logic.user_form_logic import UserFormLogic


class UserFormConstructor(QDialog):
    def __init__(self):
        super().__init__()
        with open('Gui/QSS/user_form.qss', 'r') as f:
            self.setStyleSheet(f.read())
        self.edit_controls = []
        self.logic = UserFormLogic()
        self.initUI()
        self.get_user_data()
        self.exec_()

    def initUI(self):
        self.setWindowIcon(QIcon('Images/man.png'))
        self.setWindowTitle(Const.USER_TITLE)
        self.setFixedSize(500, 275)
        self.setLayout(QVBoxLayout())

        nameLabel = QLabel('Imię i Nazwisko')
        nameLineEdit = QLineEdit()
        self.edit_controls.append(nameLineEdit)

        emailLabel = QLabel('Email')
        emailLineEdit = QLineEdit()
        self.edit_controls.append(emailLineEdit)

        passwordLabel = QLabel('Hasło')
        passwordLineEdit = QLineEdit()
        passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.edit_controls.append(passwordLineEdit)

        phoneLabel = QLabel('Telefon')
        phoneLineEdit = QLineEdit()
        self.edit_controls.append(phoneLineEdit)

        btnOK = QPushButton('Zapisz')
        btnOK_icon = QIcon(Const.SAVE_ICON)
        btnOK.setToolTip("Zapisz")
        btnOK.setMinimumSize(Const.BUTTON_WIDTH, Const.BUTTON_HEIGHT)
        btnOK.setIcon(btnOK_icon)
        btnOK.clicked.connect(self.save_button_clicked)

        btnCancel = QPushButton('Anuluj')
        btnCancel_icon = QIcon(Const.CANCEL_ICON)
        btnCancel.setToolTip("Anuluj")
        btnCancel.setMinimumSize(Const.BUTTON_WIDTH, Const.BUTTON_HEIGHT)
        btnCancel.setIcon(btnCancel_icon)
        btnCancel.clicked.connect(self.cancel_button_clicked)

        groupbox_layout = QGridLayout()
        groupbox = QGroupBox()
        groupbox.setStyleSheet('QGroupBox {font-weight: bold}')
        groupbox.setLayout(groupbox_layout)

        groupbox_layout.addWidget(nameLabel, 0, 0)
        groupbox_layout.addWidget(nameLineEdit, 0, 1, 1, 2)

        groupbox_layout.addWidget(emailLabel, 1, 0)
        groupbox_layout.addWidget(emailLineEdit, 1, 1, 1, 2)

        groupbox_layout.addWidget(passwordLabel, 2, 0)
        groupbox_layout.addWidget(passwordLineEdit, 2, 1, 1, 2)

        groupbox_layout.addWidget(phoneLabel, 3, 0)
        groupbox_layout.addWidget(phoneLineEdit, 3, 1, 1, 2)

        self.layout().addWidget(groupbox)

        buttons_layout = QHBoxLayout(self)
        buttons_groupbox = QGroupBox(self)
        buttons_groupbox.setLayout(buttons_layout)
        buttons_layout.addWidget(btnCancel)
        buttons_layout.addWidget(btnOK)

        self.layout().addWidget(buttons_groupbox)

    def get_user_data(self):
        self.edit_controls[0].setText(self.logic.user.name)
        self.edit_controls[1].setText(self.logic.user.email)
        self.edit_controls[2].setText(self.logic.user.password)
        self.edit_controls[3].setText(self.logic.user.phone)

    def save_button_clicked(self):

        user_data = []
        for edit in self.edit_controls:
            if len(edit.text()) > 0:
                user_data.append(edit.text())
            else:
                MsgBox('error_dialog', 'Błąd',
                       'Informacje o użytkowniku nie zostały uzupełnione.\n'
                       'Uzupełnij wszystkie wymagane dane.',
                       QIcon(Const.USER_ICON))
                self.edit_controls[0].setFocus()
                return
        if self.logic.change_current_user(user_data):
            MsgBox('ok_dialog', 'Informacja', 'Dane użytkownika zostały zaktualizowane.', QIcon(Const.USER_ICON))
            self.close()
        else:
            sys.exit()

    def cancel_button_clicked(self):
        self.close()
