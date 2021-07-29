from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon
import Gui.Components.constants as Const


class Button(QPushButton):
    def __init__(self, icon: QIcon):
        super().__init__()
        self.setIcon(icon)
        self.setMinimumSize(40, 40)


class ButtonPanel(QWidget):
    def __init__(self):
        super().__init__()
        # Task TableView Widget Creation

        add_icon = QIcon(Const.PLUS_ICON)
        edit_icon = QIcon(Const.PENCIL_ICON)
        delete_icon = QIcon(Const.DELETE_ICON)

        # Create layout
        layout = QVBoxLayout()

        # Create table_view widget
        self.add_button = Button(add_icon)
        self.add_button.setToolTip("Dodaj")
        self.edit_button = Button(edit_icon)
        self.edit_button.setToolTip("Zmień")
        self.del_button = Button(delete_icon)
        self.del_button.setToolTip("Usuń")

        # Add tasks_table_view widget to layout
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.del_button)
        self.setLayout(layout)
        self.return_widget()

    def return_widget(self):
        return self
