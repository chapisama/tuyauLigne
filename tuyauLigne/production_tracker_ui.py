import json
import os
import sys

import maya.OpenMayaUI as omui

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtWidgets

try:
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2.QtCore import Qt

try:
    from shiboken6 import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

from functools import partial

from tuyauLigne import project_manager as pm


class ProductionTrackerLaunch:
    def __init__(self):
        self.parent = self.maya_main_window()

    def maya_main_window(self):
        main_window_ptr = omui.MQtUtil.mainWindow()

        if sys.version_info.major >= 3:
            try:
                return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
            except:
                return None
        else:
            return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def run(self):
        """  builds our UI
        """
        win = None

        if not win:
            win = ProductionTrackerUI(parent=self.parent)

        if win.isHidden():
            win.show()
        else:
            win.raise_()
            win.activateWindow()

        win.show()
        return win


class ProductionTrackerUI(QtWidgets.QDialog):
    lbl_name_ = {}
    combo_modeling_ = {}
    combo_uv_ = {}
    combo_surfacing_ = {}

    def __init__(self, parent=None):
        super(ProductionTrackerUI, self).__init__(parent)
        self.setWindowTitle("Production Tracker")
        self.setFixedWidth(500)
        self.setMaximumHeight(500)
        self.create_widgets()
        self.initial_state_ui()
        self.create_connections()
        self.create_layout()

    def create_widgets(self):
        self.combo_asset_type = QtWidgets.QComboBox(self)
        self.combo_asset_type.setMaximumWidth(60)

        self.entry_search = QtWidgets.QLineEdit()
        self.entry_search.setMaximumHeight(26)

        self.lbl_asset_name = QtWidgets.QLabel("Asset name")
        self.lbl_modeling = QtWidgets.QLabel("Modeling")
        self.lbl_uv_unfold = QtWidgets.QLabel("UV unfold")
        self.lbl_surfacing = QtWidgets.QLabel("Surfacing")

    def create_layout(self):
        working_steps = ["TODO", "WIP", "DONE", "RETAKE"]

        file_path = os.path.join(pm.dict_main_folders().get("data_folder"), 'production_tracker.json')
        with open(file_path) as f:
            asset_list = json.load(f)
        assets = asset_list['assets']

        # creates the boxes
        main_layout = QtWidgets.QVBoxLayout()
        hbox_search = QtWidgets.QHBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout(self)
        vbox_asset_list = QtWidgets.QVBoxLayout()

        # add grid_layout to a widget
        layout_widget = QtWidgets.QWidget()
        layout_widget.setLayout(self.grid_layout)

        # create scroll_area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(layout_widget)

        # add boxes to the main layout
        main_layout.addLayout(hbox_search)
        main_layout.addLayout(vbox_asset_list)
        main_layout.addStretch()
        self.setLayout(main_layout)

        # add widgets to boxes
        hbox_search.addWidget(self.combo_asset_type)
        hbox_search.addWidget(self.entry_search)

        self.grid_layout.addWidget(self.lbl_asset_name, 0, 0)
        self.grid_layout.addWidget(self.lbl_modeling, 0, 1)
        self.grid_layout.addWidget(self.lbl_uv_unfold, 0, 2)
        self.grid_layout.addWidget(self.lbl_surfacing, 0, 3)

        vbox_asset_list.addWidget(scroll_area)

        # create and set all rows of assets status / widgets per cell in the grid
        for asset in assets:
            asset_name = asset.get('name')
            modeling_status = asset.get('Modeling')
            uv_status = asset.get("UV unfold")
            surfacing_status = asset.get("Surfacing")
            row = self.grid_layout.rowCount() + 1
            column_modeling = 1
            column_uv = 2
            column_surfacing = 3

            # create widgets
            self.lbl_name_[asset_name] = QtWidgets.QLabel(asset_name)
            self.combo_modeling_[asset_name] = QtWidgets.QComboBox()
            self.combo_uv_[asset_name] = QtWidgets.QComboBox()
            self.combo_surfacing_[asset_name] = QtWidgets.QComboBox()
            for step in working_steps:
                self.combo_modeling_[asset_name].addItem(step)
                self.combo_uv_[asset_name].addItem(step)
                self.combo_surfacing_[asset_name].addItem(step)

            # set current status by looking at the json file        
            self.set_combo_text(self.combo_modeling_[asset_name], modeling_status)
            self.set_combo_text(self.combo_uv_[asset_name], uv_status)
            self.set_combo_text(self.combo_surfacing_[asset_name], surfacing_status)

            # set the color of combobox box by looking at their status
            index = self.combo_modeling_[asset_name].currentIndex()
            status = self.combo_modeling_[asset_name].itemText(index)
            self.set_combobox_background_color(self.combo_modeling_[asset_name], status)
            index = self.combo_uv_[asset_name].currentIndex()
            status = self.combo_uv_[asset_name].itemText(index)
            self.set_combobox_background_color(self.combo_uv_[asset_name], status)
            index = self.combo_surfacing_[asset_name].currentIndex()
            status = self.combo_surfacing_[asset_name].itemText(index)
            self.set_combobox_background_color(self.combo_surfacing_[asset_name], status)

            # add the widgets in their row                                                                                                    
            self.grid_layout.addWidget(self.lbl_name_[asset_name], row, 0)
            self.grid_layout.addWidget(self.combo_modeling_[asset_name], row, column_modeling)
            self.grid_layout.addWidget(self.combo_uv_[asset_name], row, column_uv)
            self.grid_layout.addWidget(self.combo_surfacing_[asset_name], row, column_surfacing)

            # connect each combobox to their function called when changed
            self.combo_modeling_[asset_name].currentIndexChanged.connect(
                partial(self.edit_json_status, column_modeling, asset_name, self.combo_modeling_[asset_name]))
            self.combo_uv_[asset_name].currentIndexChanged.connect(
                partial(self.edit_json_status, column_uv, asset_name, self.combo_uv_[asset_name]))
            self.combo_surfacing_[asset_name].currentIndexChanged.connect(
                partial(self.edit_json_status, column_surfacing, asset_name, self.combo_surfacing_[asset_name]))

    def create_connections(self):
        self.combo_asset_type.currentIndexChanged.connect(self.update_searched_asset)
        self.entry_search.textChanged.connect(self.update_searched_asset)

    def initial_state_ui(self):
        asset_types = ["all", "prx", "prp"]
        self.combo_asset_type.addItems(asset_types)

    def edit_json_status(self, column, asset_name, combobox, combo_index):
        """
        Edits the status of the asset inside the production_tracker.json file.

        Parameters:
            column (int): Index of the column task.
            asset_name (str): Name of the asset.
            combobox (QComboBox): ComboBox associated with the asset and its production step.
            combo_index (int): Index of the text selected inside the ComboBox.
        """
        status = combobox.itemText(combo_index)
        task_item = self.grid_layout.itemAtPosition(0, column)
        task_widget = task_item.widget()
        task_str = task_widget.text()
        file_path = os.path.join(pm.dict_main_folders().get("data_folder"), 'production_tracker.json')

        with open(file_path, 'r') as f:
            asset_data = json.load(f)
        for asset in asset_data['assets']:
            if asset['name'] == asset_name:
                asset[task_str] = status
                break
        with open(file_path, 'w') as f:
            json.dump(asset_data, f, indent=2)

        if column == 1:
            self.set_combobox_background_color(self.combo_modeling_[asset_name], status)
        elif column == 2:
            self.set_combobox_background_color(self.combo_uv_[asset_name], status)
        elif column == 3:
            self.set_combobox_background_color(self.combo_surfacing_[asset_name], status)

    def set_combobox_background_color(self, combobox, status):
        """
        Sets the background color of the ComboBox based on the current text.

        Parameters:
            combobox (QComboBox): ComboBox associated with the asset and its production step.
            status (str): Text selected inside the ComboBox.
        """
        if status == "TODO":
            combobox.setStyleSheet("background-color: #670101;")
        elif status == "WIP":
            combobox.setStyleSheet("background-color: #7f7a14;")
        elif status == "RETAKE":
            combobox.setStyleSheet("background-color: #714a08;")
        elif status == "DONE":
            combobox.setStyleSheet("background-color: #365f29;")

    def set_combo_text(self, combobox, status):
        """
        Sets the status of the ComboBox based on the production_tracker.json.

        Parameters:
            combobox (QComboBox): ComboBox associated with the asset and its production step.
            status (str): Status inside the production_tracker.json.
        """
        if status == "TODO":
            combobox.setCurrentText("TODO")
        elif status == "WIP":
            combobox.setCurrentText("WIP")
        elif status == "DONE":
            combobox.setCurrentText("DONE")
        elif status == "RETAKE":
            combobox.setCurrentText("RETAKE")

    def update_searched_asset(self):
        """
        Displays the assets inside the UI by looking at the search entry of the user.
        """
        asset_to_hide = []
        self.show_all_asset_line()
        if self.combo_asset_type.currentText() == "all":
            str_searched = self.entry_search.text()
        else:
            str_searched = self.combo_asset_type.currentText() + "_" + self.entry_search.text()
        if str_searched:
            file_path = os.path.join(pm.dict_main_folders().get("data_folder"), 'production_tracker.json')
            with open(file_path) as f:
                asset_list = json.load(f)
            assets = asset_list['assets']
            for asset in assets:
                if str_searched not in asset['name']:
                    asset_to_hide.append(asset['name'])
            for asset in asset_to_hide:
                self.hide_asset_line(asset)

    def hide_asset_line(self, asset_name):
        """
        Hides the asset line inside the UI.

        Parameters:
            asset_name (str): Name of the asset to hide.
        """
        self.lbl_name_[asset_name].hide()
        self.combo_modeling_[asset_name].hide()
        self.combo_uv_[asset_name].hide()
        self.combo_surfacing_[asset_name].hide()

    def show_all_asset_line(self):
        """
        Shows all asset lines.
        """
        file_path = os.path.join(pm.dict_main_folders().get("data_folder"), 'production_tracker.json')
        with open(file_path) as f:
            asset_list = json.load(f)
        assets = asset_list['assets']
        for asset in assets:
            asset_name = asset['name']
            self.lbl_name_[asset_name].show()
            self.combo_modeling_[asset_name].show()
            self.combo_uv_[asset_name].show()
            self.combo_surfacing_[asset_name].show()
