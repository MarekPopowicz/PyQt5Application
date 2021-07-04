from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QHBoxLayout, QGroupBox, QAbstractScrollArea
from Gui.Components.table_view_buttons_panel import ButtonPanel


class TableView(QTableWidget):
    def __init__(self, table_columns_list):
        super().__init__()
        self.columns = table_columns_list
        self.object_id = 0
        self.set_table()

    def set_table(self):

        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        # Set cells non-editable
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
        # Set first column hidden
        self.setColumnHidden(0, True)
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Disable header text bold style on row selected
        self.horizontalHeader().setHighlightSections(False)
        # Set the entire row selected
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.setHorizontalHeaderLabels(self.columns)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.resizeColumnsToContents()
        # Set last column stretched
        self.horizontalHeader().setStretchLastSection(True)


class TablePanel:
    def __init__(self, panel_name, table_columns_list):
        # Task TableView Widget Creation
        # Create layout
        self.view_layout = QHBoxLayout()
        self.view_layout.setContentsMargins(5, 5, 5, 5)
        # Create table_view widget
        self.table_view = TableView(table_columns_list)
        self.table_view.setObjectName(panel_name)
        self.button_panel = ButtonPanel()
        # Add tasks_table_view widget to layout
        self.view_layout.addWidget(self.table_view)
        self.view_layout.addWidget(self.button_panel)
        # Create tasks_table_view group_box
        self.groupbox_table_view = QGroupBox(panel_name)
        self.groupbox_table_view.setStyleSheet('QGroupBox {font-weight: bold}')
        # Add layout to group_box
        self.groupbox_table_view.setLayout(self.view_layout)
        self.return_widget()

    def return_widget(self):
        return self
