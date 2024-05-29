try:
    from PySide6 import QtCore, QtWidgets, QtGui
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui

try:
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2.QtCore import Qt

try:
    from shiboken6 import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

import os
import string
import sys

import maya.OpenMayaUI as omui
import maya.cmds as mc
from tuyauLigne import asset_manager as am
from tuyauLigne import json_manager as jsm
from tuyauLigne import outliner_manager as outm
from tuyauLigne import project_manager as pm


class ProjectManagerLaunch:
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
            win = ProjectManagerLaunchUi(parent=self.parent)

        if win.isHidden():
            win.show()
        else:
            win.raise_()
            win.activateWindow()

        win.show()
        return win


class ProjectManagerLaunchUi(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ProjectManagerLaunchUi, self).__init__(parent)
        self.setWindowTitle("create project")
        self.setMinimumWidth(500)
        self.setMinimumHeight(260)
        self.create_widgets()
        self.create_connections()
        self.initial_state_ui()
        self.create_layout()

    def create_widgets(self):
        self.lbl_create_project = QtWidgets.QLabel(self)
        self.lbl_create_project.setText("Create project")
        self.lbl_create_project.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_create_project.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_parent_folder = QtWidgets.QLabel(self)
        self.lbl_parent_folder.setText("parent folder :")

        self.entry_parent_folder = QtWidgets.QLineEdit()
        self.entry_parent_folder.setFixedHeight(20)

        self.btn_get_folder = QtWidgets.QPushButton(self)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icons", "icon_folder.png")
        icon = QtGui.QPixmap(icon_path)
        self.btn_get_folder.setIcon(QtGui.QIcon(icon))

        self.entry_project_name = QtWidgets.QLineEdit()
        self.entry_project_name.setFixedHeight(20)
        self.entry_project_name.setMinimumWidth(316)

        self.btn_create_project = QtWidgets.QPushButton(self)
        self.btn_create_project.setText("create project")

        self.line_separator = QtWidgets.QFrame()
        self.line_separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_separator.setFrameShadow(QtWidgets.QFrame.Plain)

        self.lbl_project_name = QtWidgets.QLabel(self)
        self.lbl_project_name.setText("project name :")

        self.lbl_create_asset = QtWidgets.QLabel(self)
        self.lbl_create_asset.setText("Create asset")
        self.lbl_create_asset.setFixedHeight(20)
        self.lbl_create_asset.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_create_asset.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_current_workspace = QtWidgets.QLabel(self)

        self.lbl_asset_name = QtWidgets.QLabel(self)
        self.lbl_asset_name.setText("asset name :")

        self.combo_asset_type = QtWidgets.QComboBox(self)
        self.combo_asset_type.setMaximumWidth(60)

        self.entry_asset_name = QtWidgets.QLineEdit(self)
        self.entry_asset_name.setFixedWidth(200)

        self.combo_increment = QtWidgets.QComboBox(self)
        self.combo_increment.setFixedWidth(40)

        self.btn_create_asset = QtWidgets.QPushButton(self)
        self.btn_create_asset.setText("create asset ")

    def create_layout(self):
        # create Hbox and VBox
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.vbox_main_create = QtWidgets.QVBoxLayout()
        self.hbox_lbl_create_project = QtWidgets.QHBoxLayout()
        self.hbox_line_separator = QtWidgets.QHBoxLayout()
        self.hbox_parent_folder = QtWidgets.QHBoxLayout()
        self.hbox_project_name = QtWidgets.QHBoxLayout()
        self.hbox_btn_create_project = QtWidgets.QHBoxLayout()
        self.hbox_lbl_create_asset = QtWidgets.QHBoxLayout()
        self.hbox_current_workspace = QtWidgets.QHBoxLayout()
        self.hbox_asset_name = QtWidgets.QHBoxLayout()
        self.hbox_btn_create_asset = QtWidgets.QHBoxLayout()
        self.vbox_strech_bottom = QtWidgets.QVBoxLayout()

        # layout all the boxes
        self.grid_layout.addLayout(self.vbox_main_create, 0, 0, 1, 1)
        self.vbox_main_create.addLayout(self.hbox_lbl_create_project)
        self.vbox_main_create.addLayout(self.hbox_parent_folder)
        self.vbox_main_create.addLayout(self.hbox_project_name)
        self.vbox_main_create.addLayout(self.hbox_btn_create_project)
        self.vbox_main_create.addLayout(self.hbox_line_separator)
        self.vbox_main_create.addLayout(self.hbox_lbl_create_asset)
        self.vbox_main_create.addLayout(self.hbox_current_workspace)
        self.vbox_main_create.addLayout(self.hbox_asset_name)
        self.vbox_main_create.addLayout(self.hbox_btn_create_asset)
        self.vbox_main_create.addLayout(self.vbox_strech_bottom)

        # add widgets to the boxes
        self.hbox_lbl_create_project.addWidget(self.lbl_create_project)

        self.hbox_parent_folder.addWidget(self.lbl_parent_folder)
        self.hbox_parent_folder.addWidget(self.entry_parent_folder)
        self.hbox_parent_folder.addWidget(self.btn_get_folder)

        self.hbox_project_name.addWidget(self.lbl_project_name)
        self.hbox_project_name.addWidget(self.entry_project_name)
        self.hbox_project_name.addStretch()

        self.hbox_btn_create_project.addStretch()
        self.hbox_btn_create_project.addWidget(self.btn_create_project)
        self.hbox_btn_create_project.addStretch()

        self.hbox_line_separator.addWidget(self.line_separator)

        self.hbox_lbl_create_asset.addWidget(self.lbl_create_asset)

        self.hbox_current_workspace.addWidget(self.lbl_current_workspace)

        self.hbox_asset_name.addWidget(self.lbl_asset_name)
        self.hbox_asset_name.addWidget(self.combo_asset_type)
        self.hbox_asset_name.addWidget(self.entry_asset_name)
        self.hbox_asset_name.addWidget(self.combo_increment)
        self.hbox_asset_name.addStretch()

        self.hbox_btn_create_asset.addStretch()
        self.hbox_btn_create_asset.addWidget(self.btn_create_asset)
        self.hbox_btn_create_asset.addStretch()

        self.vbox_strech_bottom.addStretch()

    def create_connections(self):
        self.btn_create_project.clicked.connect(self.create_project)
        self.btn_create_project.clicked.connect(self.set_lbl_current_workspace)
        self.btn_get_folder.clicked.connect(self.get_parent_folder)
        self.btn_create_asset.clicked.connect(self.create_asset)

    def initial_state_ui(self):
        self.set_lbl_current_workspace()
        my_assets = ["prx", "prp"]
        self.combo_asset_type.addItems(my_assets)
        increments = list(string.ascii_uppercase)
        self.combo_increment.addItems(increments)

    def set_lbl_current_workspace(self):
        """
        Modify the label indicator of the current workspace in the UI.
        """
        root_project_folder = mc.workspace(q=True, rootDirectory=True)
        lbl = f"current workspace : {root_project_folder}"
        self.lbl_current_workspace.setText(lbl)

    def get_parent_folder(self):
        """
        Get the parent folder of the project selected by the user and copy the path in the UI.
        """
        parent_folder = mc.fileDialog2(dialogStyle=1, fileMode=3)
        self.entry_parent_folder.setText(parent_folder[0])

    def create_project(self):
        """
        Create the project main folders by getting the information specified by the user.
        """
        parent_folder = self.entry_parent_folder.text()
        project_name = self.entry_project_name.text()
        pm.create_project(parent_folder, project_name)
        jsm.create_production_tracker()

    def create_asset(self):
        """
        Create the asset main folders by getting the information specified by the user.
        """
        asset_type = self.combo_asset_type.currentText()
        short_name = self.entry_asset_name.text()
        increment = self.combo_increment.currentText()
        asset_name = asset_type + "_" + short_name + increment
        if asset_type == "prx":
            proxy_folder = pm.dict_main_folders().get("proxy_folder")
            pm.create_proxy_folder(asset_name, proxy_folder)
            am.create_proxy_maya(asset_name)
            main_grp = mc.group(name=asset_name, em=True)
            outm.lock_main_attr(main_grp)
            mc.file(save=True, type="mayaAscii")
        elif asset_type == "prp":
            asset_folder = pm.dict_main_folders().get("asset_folder")
            pm.create_asset_folder(asset_name, asset_folder)
            pm.create_sub_asset_folders(asset_name)
            am.create_prp_maya(asset_name, asset_folder)
            main_grp = mc.group(name=asset_name, em=True)
            proxy_grp = mc.group(name=asset_name.replace("prp_", "proxy_"), em=True)
            mc.parent(proxy_grp, main_grp)
            outm.lock_main_attr(main_grp)
            mc.file(save=True, type="mayaAscii")
