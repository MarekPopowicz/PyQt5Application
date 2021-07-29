from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QDialog
import Gui.Components.constants as Const


class ButtonPanel:
    def __init__(self, form: QDialog):
        self.form = form
        self.create_button_panel()

    def create_button_panel(self):
        save_icon = QIcon(Const.SAVE_ICON)
        button_save = QPushButton("Zapisz")
        button_save.setObjectName("Zapisz")
        button_save.setToolTip("Zapisz")
        button_save.setMinimumSize(Const.BUTTON_WIDTH, Const.BUTTON_HEIGHT)
        button_save.setIcon(save_icon)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        buttons_layout.addWidget(button_save)
        layout = self.form.layout()
        layout.addLayout(buttons_layout)

