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

import os
import sys
from functools import partial

import maya.OpenMayaUI as omui
import maya.cmds as mc
from tuyauLigne import asset_manager as am
from tuyauLigne import naming_convention as naco
from tuyauLigne import outliner_manager as outm
from tuyauLigne import project_manager as pm
from tuyauLigne import sanity_check_list as scl


class SanityCheckLaunch:
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
            win = SanityCheckUi(parent=self.parent)

        if win.isHidden():
            win.show()
        else:
            win.raise_()
            win.activateWindow()

        win.show()
        return win


class SanityCheckUi(QtWidgets.QDialog):
    hbox_ = {}
    btn_ = {}
    btn_report_ = {}
    vbox_ = {}
    header_ = {}
    btn_header_ = {}
    btn_collapse_ = {}
    lbl_ = {}
    hbox_lbl_ = {}

    def __init__(self, parent=None):
        super(SanityCheckUi, self).__init__(parent)
        self.setWindowTitle("sanity check")
        self.setMinimumWidth(700)
        self.setMinimumHeight(260)
        self.create_widgets()
        self.create_connections()
        self.initial_state_ui()
        self.create_layout()

    def create_widgets(self):
        self.lbl_sanity = QtWidgets.QLabel("Sanity Check :")
        self.lbl_report = QtWidgets.QLabel("Report :")

        # widgets for report column
        self.list_report = QtWidgets.QListWidget()
        self.list_report.setMinimumWidth(300)

        # widget for main button
        self.btn_sanity = QtWidgets.QPushButton("Sanity")
        self.btn_publish = QtWidgets.QPushButton("Publish")

    def create_layout(self):

        # main boxes
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.vbox_main = QtWidgets.QVBoxLayout(self)
        self.hbox_main = QtWidgets.QHBoxLayout(self)

        # column boxes
        self.vbox_sanity = QtWidgets.QVBoxLayout(self)
        self.hbox_lbl_sanity = QtWidgets.QHBoxLayout(self)
        self.vbox_report = QtWidgets.QVBoxLayout(self)
        self.hbox_lbl_report = QtWidgets.QHBoxLayout(self)
        # main button box
        self.hbox_main_button = QtWidgets.QHBoxLayout(self)

        # main layout
        self.grid_layout.addLayout(self.vbox_main, 0, 0, 1, 1)
        self.vbox_main.addLayout(self.hbox_main)
        self.vbox_main.addLayout(self.hbox_main_button)
        self.hbox_main.addLayout(self.vbox_sanity)
        self.hbox_main.addLayout(self.vbox_report)
        self.vbox_sanity.addLayout(self.hbox_lbl_sanity)
        self.vbox_report.addLayout(self.hbox_lbl_report)

        # adding widgets
        self.hbox_lbl_sanity.addWidget(self.lbl_sanity)
        self.hbox_lbl_report.addWidget(self.lbl_report)

        # adding buttons to main buttons
        self.hbox_main_button.addStretch()
        self.hbox_main_button.addWidget(self.btn_sanity)
        self.hbox_main_button.addWidget(self.btn_publish)

        # create headers
        for header in scl.sanity_cat_list:
            category = header['category']
            label = header['label']
            self.vbox_[category] = QtWidgets.QVBoxLayout(self)
            self.vbox_sanity.addLayout(self.vbox_[category])
            self.header_[category] = QtWidgets.QHBoxLayout(self)
            self.btn_header_[category] = QtWidgets.QPushButton(label)
            self.btn_header_[category].setFixedWidth(200)
            self.btn_collapse_[category] = QtWidgets.QPushButton(">")
            self.btn_collapse_[category].setFixedWidth(30)
            self.btn_collapse_[category].clicked.connect(partial(self.toggle_category, category))
            self.vbox_[category].addLayout(self.header_[category])
            self.header_[category].addWidget(self.btn_header_[category])
            self.header_[category].addWidget(self.btn_collapse_[category])

        # create check buttons, and connect them to their respective functionns
        functions = self.dict_functions()
        self.descriptions = []
        for dict_check in scl.sanity_check_list:
            function = dict_check['function_name']
            label = dict_check['label']
            category = dict_check['category']
            description = dict_check['description']
            check_function, report_function = functions[function]

            self.lbl_[description] = QtWidgets.QLabel(description)
            self.lbl_[description].setWordWrap(True)
            self.lbl_[description].setFixedWidth(350)
            self.hbox_lbl_[description] = QtWidgets.QHBoxLayout()
            self.hbox_lbl_[description].addWidget(self.lbl_[description])
            self.hbox_lbl_[description].addStretch()
            self.vbox_report.addLayout(self.hbox_lbl_[description])
            self.lbl_[description].hide()
            self.descriptions.append(self.lbl_[description])

            self.hbox_[function] = QtWidgets.QHBoxLayout(self)
            self.vbox_[category].addLayout(self.hbox_[function])
            self.btn_[function] = QtWidgets.QPushButton(label)
            self.btn_[function].setFixedWidth(160)
            self.btn_[function].setFixedHeight(18)
            self.btn_report_[function] = QtWidgets.QPushButton("!!!")
            self.btn_report_[function].setFixedWidth(30)
            self.btn_report_[function].setFixedHeight(18)
            self.hbox_[function].addWidget(self.btn_[function])
            self.hbox_[function].addWidget(self.btn_report_[function])

            self.btn_[function].clicked.connect(partial(check_function, function))
            self.btn_report_[function].clicked.connect(partial(report_function, description))

        self.vbox_report.addWidget(self.list_report)
        self.vbox_report.addStretch()
        self.vbox_sanity.addStretch()

    def create_connections(self):
        self.list_report.itemClicked.connect(self.select_item)
        self.btn_sanity.clicked.connect(self.sanity_check)
        self.btn_publish.clicked.connect(self.publish_assets)

    def initial_state_ui(self):
        self.list_report.hide()

    def dict_functions(self):
        """
        Creates a dictionary mapping function names to function and report objects.

        This function iterates over a list of dictionaries representing sanity checks.
        Each dictionary contains a function name and a report name. For each entry,
        the function retrieves the function object and the report object from the class
        instance (self) using the provided names. These are then stored in a dictionary
        where the keys are function names and the values are tuples of the function
        and report objects.

        Returns:
            dict: A dictionary mapping function names to tuples (function, report).
        """
        functions = {}
        for dict_check in scl.sanity_check_list:
            function_name = dict_check['function_name']
            report_name = dict_check['report_called']
            function = getattr(self, function_name)
            report = getattr(self, report_name)
            functions[function_name] = (function, report)
        return functions

    def hide_descriptions(self):
        """
        Hides the description in the UI.
        """

        for description in self.descriptions:
            description.hide()

    def select_item(self):
        """
        Select in the outliner the object clicked on the report list by the user if it exists.
        """

        mc.select(d=True)
        item_selected = self.list_report.currentItem().text()
        if mc.objExists(item_selected):
            mc.select(mc.ls(item_selected))

    def toggle_category(self, category):
        """
        Hide or show the categories associated with the header
        """

        for check in scl.sanity_check_list:
            function = check['function_name']
            visible_state = self.btn_[function].isVisible()
            if category == check['category']:
                self.btn_[function].setVisible(not visible_state)
                self.btn_report_[function].setVisible(not visible_state)

    def return_summary_bool(self, function, report):
        """
        Parameters:
            function (str) : name of the function called
            report : report resulting from the execution of the function.
        Returns:
            bool : True if there is no report
        """
        if report:
            self.btn_[function].setStyleSheet("QPushButton {background-color :#b41637}")
            return False
        else:
            self.btn_[function].setStyleSheet("QPushButton {background-color :#2a8225}")
            return True

    # TODO : reflexion on the reports
    def report_summary(self, summary, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_group_id') and summary:
            for e in summary:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

        # self.list_report.clear()
        # self.hide_descriptions()
        # if hasattr(self, 'summary_transforms') and self.summary_transforms:
        #     for e in self.summary_transforms:
        #         self.list_report.addItem(e)
        #     self.list_report.show()
        #     self.lbl_[description].show()

    def check_workspace(self, function):
        """
        Create and set the workspace for the specified project.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if the workspace is created, False if it isn't.
        """
        report = pm.check_workspace()
        if report:
            self.btn_[function].setStyleSheet("QPushButton {background-color :#2a8225}")
            self.bilan_workspace = "ok"
        else:
            self.btn_[function].setStyleSheet("QPushButton {background-color :#b41637}")
            self.bilan_workspace = "current scene is not in the good workspace"

        return report

    def report_workspace(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'bilan_workspace') and self.bilan_workspace:
            self.list_report.addItem(self.bilan_workspace)
            self.list_report.show()
            self.lbl_[description].show()

    def check_master_grp(self, function):
        """
        check if there is a master group in the maya scene, and if it is at the root.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_master_grp = ""
        master_grp = outm.get_master_grp_name()
        master_grp = mc.ls(master_grp, type="transform", shortNames=True)
        if not master_grp:
            self.btn_[function].setStyleSheet("QPushButton {background-color :#b41637}")
            self.summary_master_grp = f"no group named '{master_grp}'"
            return False
        elif len(master_grp) > 1:
            self.btn_[function].setStyleSheet("QPushButton {background-color :#b41637}")
            self.summary_master_grp = f"only one group shall be named '{master_grp}'"
            return False
        elif mc.listRelatives(master_grp[0], parent=True):
            self.btn_[function].setStyleSheet("QPushButton {background-color :#b41637}")
            self.summary_master_grp = f"'{master_grp}' group must be at the top root "
            return False
        else:
            self.btn_[function].setStyleSheet("QPushButton {background-color :#2a8225}")
            return True

    def report_master_grp(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_master_grp') and self.summary_master_grp:
            self.list_report.addItem(self.summary_master_grp)
            self.list_report.show()
            self.lbl_[description].show()

    def check_prefix_prp(self, function):
        """
        check if groups children of master_grp are named "prp_"

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        group_to_check = []
        self.summary_prefix_prp = []
        groups = mc.ls(type="transform")
        master_grp = outm.get_master_grp_name()
        for group in groups:
            if mc.listRelatives(group, parent=True) == [master_grp]:
                group_to_check.append(group)
        for group in group_to_check:
            if group.split("_")[0] != "prp":
                self.summary_prefix_prp.append(group)
        check_ok = self.return_summary_bool(function, self.summary_prefix_prp)

        return check_ok

    def report_prefix_prp(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_prefix_prp') and self.summary_prefix_prp:
            for e in self.summary_prefix_prp:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_prp_hierarchy_naming(self, function):
        """
        Check if children groups of "prp_nameX" are named "proxy_nameX" or "render_nameX"

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_prp_hierarchy_naming = []
        prp_groups = []
        master_grp = outm.get_master_grp_name()
        groups_in_master = mc.listRelatives(master_grp, allDescendents=True, type="transform")
        if "prp_" in master_grp:
            prp_groups.append(master_grp)

        for group in groups_in_master:
            if "prp_" in group:
                prp_groups.append(group)
        for prp_group in prp_groups:
            prp_name = prp_group.split("_")[1]
            prp_children = mc.listRelatives(prp_group, children=True)
            for prp_child in prp_children:
                if "_" not in prp_child:
                    self.summary_prp_hierarchy_naming.append(prp_child)
                else:
                    child_name = prp_child.split("_")[1]
                    child_prefix = prp_child.split("_")[0]
                    if child_name != prp_name or child_prefix != "proxy" and child_prefix != "render":
                        self.summary_prp_hierarchy_naming.append(prp_child)

        check_ok = self.return_summary_bool(function, self.summary_prp_hierarchy_naming)

        return check_ok

    def report_prp_hierarchy_naming(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_prp_hierarchy_naming') and self.summary_prp_hierarchy_naming:
            for e in self.summary_prp_hierarchy_naming:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_purpose_grp_hierarchy(self, function):
        """
        check if "prp_" are parents of "proxy_" or "render_"

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        groups_in_master = mc.listRelatives("prp_*", allDescendents=True, type="transform")
        self.summary_purpose_grp_hierarchy = []
        for group in groups_in_master:
            if "proxy_" in group or "render_" in group:
                parent = mc.listRelatives(group, parent=True)
                if "prp_" not in parent[0]:
                    self.summary_purpose_grp_hierarchy.append(group)

        check_ok = self.return_summary_bool(function, self.summary_purpose_grp_hierarchy)

        return check_ok

    def report_purpose_grp_hierarchy(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_purpose_grp_hierarchy') and self.summary_purpose_grp_hierarchy:
            for e in self.summary_purpose_grp_hierarchy:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_mesh_in_grp(self, function):
        """
        Check if there is no meshes are child of master group

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_mesh_in_grp = []
        master_grp = outm.get_master_grp_name()
        all_meshes = mc.listRelatives(master_grp, allDescendents=True, type="mesh", fullPath=True)
        for mesh in all_meshes:
            parent = mc.listRelatives(mesh, parent=True)
            grand_parent = mc.listRelatives(parent, parent=True)
            if grand_parent[0] == master_grp:
                short_name = mc.ls(parent, shortNames=True)
                self.summary_mesh_in_grp.append(short_name[0])

        check_ok = self.return_summary_bool(function, self.summary_mesh_in_grp)

        return check_ok

    def report_mesh_in_grp(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_mesh_in_grp') and self.summary_mesh_in_grp:
            for e in self.summary_mesh_in_grp:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_empty_group(self, function):
        """
        Check if there is empty groups.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_empty_group = []
        master_grp = outm.get_master_grp_name()
        all_groups = mc.listRelatives(master_grp, allDescendents=True, type="transform", fullPath=True)
        for group in all_groups:
            if not mc.listRelatives(group, children=True):
                self.summary_empty_group.append(group)

        check_ok = self.return_summary_bool(function, self.summary_empty_group)

        return check_ok

    def report_empty_group(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_empty_group') and self.summary_empty_group:
            for e in self.summary_empty_group:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_prp_in_master(self, function):
        """
        Check if "prp_" groups are children of master group

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        master_grp = outm.get_master_grp_name()
        groups_in_master = mc.listRelatives(master_grp, allDescendents=True, type="transform")
        self.summary_prp_in_master = []
        for group in groups_in_master:
            if "prp_" in group and mc.listRelatives(group, parent=True)[0] != master_grp:
                self.summary_prp_in_master.append(group)

        check_ok = self.return_summary_bool(function, self.summary_prp_in_master)

        return check_ok

    def report_prp_in_master(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_prp_in_master') and self.summary_prp_in_master:
            for e in self.summary_prp_in_master:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_grp_name(self, function):
        """
        Check if other groups are named "grp_"

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_grp_name = []
        transforms_in_purpose = mc.listRelatives("proxy_*", allDescendents=True, type="transform")
        for transform in transforms_in_purpose:
            if not mc.listRelatives(transform, children=True, type="mesh") and "grp_" not in transform:
                self.summary_grp_name.append(transform)

        check_ok = self.return_summary_bool(function, self.summary_grp_name)

        return check_ok

    def report_grp_name(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_grp_name') and self.summary_grp_name:
            for e in self.summary_grp_name:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_unique_name(self, function):
        """
        Check if different elements have the same name

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_unique_name = []
        master_grp = outm.get_master_grp_name()
        elements_in_master = mc.listRelatives(master_grp, allDescendents=True)
        for element in elements_in_master:
            check_unique_name = mc.ls(element, shortNames=True)
            if len(check_unique_name) > 1:
                self.summary_unique_name.append(element)

        check_ok = self.return_summary_bool(function, self.summary_unique_name)

        return check_ok

    def report_unique_name(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_unique_name') and self.summary_unique_name:
            for e in self.summary_unique_name:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_existing_prp(self, function):
        """
        Check if a version of the prop is already published

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_existing_prp = []
        asset_folder = pm.dict_main_folders().get("asset_folder")
        asset_folders = os.listdir(asset_folder)
        master_grp = outm.get_master_grp_name()
        prp_grp = mc.listRelatives(master_grp, children=True, type="transform")
        if "prp_" in master_grp:
            if os.path.isdir(asset_folder):
                for asset in asset_folders:
                    if master_grp in asset:
                        self.summary_existing_prp.append(asset)
        if os.path.isdir(asset_folder):
            for asset in asset_folders:
                if "prp_" in asset and asset in prp_grp:
                    self.summary_existing_prp.append(asset)

        check_ok = self.return_summary_bool(function, self.summary_existing_prp)

        return check_ok

    def report_existing_prp(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_existing_prp') and self.summary_existing_prp:
            for e in self.summary_existing_prp:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_existing_set(self, function):
        """
        Check if a version of the set is already published

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_existing_set = []
        set_folder = pm.dict_main_folders().get("env_folder")
        set_folders = os.listdir(set_folder)
        master_grp = outm.get_master_grp_name()
        if "prx_" in master_grp:
            for set_folder in set_folders:
                if master_grp == set_folder.replace("set_", "prx_"):
                    self.summary_existing_set.append(set_folder)

        check_ok = self.return_summary_bool(function, self.summary_existing_set)

        return check_ok

    def report_existing_set(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_existing_set') and self.summary_existing_set:
            for e in self.summary_existing_set:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_history(self, function):
        """
        Check if meshes have history.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_history = []
        master_grp = outm.get_master_grp_name()
        all_shapes = mc.listRelatives(master_grp, allDescendents=True, type="mesh")
        for shape in all_shapes:
            if len(mc.listHistory(shape)) > 1:
                self.summary_history.append(shape)

        check_ok = self.return_summary_bool(function, self.summary_history)

        return check_ok

    def report_history(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_history') and self.summary_history:
            for e in self.summary_history:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_group_id(self, function):
        """
        Check if the scene has group ID.

        Parameters:
            function (str) : name of the function called when the button is clicked.

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_group_id = mc.ls(type="groupId")

        check_ok = self.return_summary_bool(function, self.summary_group_id)

        return check_ok

    def report_group_id(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_group_id') and self.summary_group_id:
            for e in self.summary_group_id:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_ghost_mesh(self, function):
        """
        Check if meshes nodes has no connexions.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.summary_ghost_mesh = []
        master_grp = outm.get_master_grp_name()
        all_shapes = mc.listRelatives(master_grp, allDescendents=True, type="mesh")
        for shape in all_shapes:
            if not mc.listConnections(shape) or mc.listConnections(shape)[0] == "MayaNodeEditorSavedTabsInfo" and len(
                    mc.listConnections(shape)) == 1:
                self.summary_ghost_mesh.append(shape)

        check_ok = self.return_summary_bool(function, self.summary_ghost_mesh)

        return check_ok

    def report_ghost_mesh(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_ghost_mesh') and self.summary_ghost_mesh:
            for e in self.summary_ghost_mesh:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_transforms(self, function):
        """
        Check the transforms of all element in the master group. For master, "proxy_", "render_", and "mesh_transform",
         verify if the transforms are in the default value. For the "prp_", check if the pivot group sets with the
         translate default value is at the world center.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.hide_descriptions()
        self.summary_transforms = []
        ok_all_pivot = True
        prp_groups = []
        groups_to_default = []
        grp_groups = []
        master_grp = outm.get_master_grp_name()
        master_transform = outm.store_element_transforms(master_grp)
        all_groups = mc.listRelatives(master_grp, allDescendents=True, type="transform")
        expected_transforms = {
            "tx": 0,
            "ty": 0,
            "tz": 0,
            "rx": 0,
            "ry": 0,
            "rz": 0,
            "sx": 1,
            "sy": 1,
            "sz": 1,
        }
        for group in all_groups:
            if "prp_" in group:
                prp_groups.append(group)
            elif "proxy_" in group or "render_" in group or mc.listRelatives(group, children=True, type="mesh"):
                groups_to_default.append(group)
            # elif "grp_" in group:

        for transform, expected_value in expected_transforms.items():
            if master_transform[transform] != expected_value and master_grp not in self.summary_transforms:
                self.summary_transforms.append(master_grp)
                ok_all_pivot = False

        if groups_to_default and ok_all_pivot:
            for group in groups_to_default:
                group_transforms = outm.store_element_transforms(group)

                for transform, expected_value in expected_transforms.items():
                    if group_transforms[transform] != expected_value and group not in self.summary_transforms:
                        self.summary_transforms.append(group)

        if prp_groups and ok_all_pivot:
            for group in prp_groups:
                group_transforms = outm.store_element_transforms(group)
                outm.center_element_world(group)
                pivot = mc.xform(group, query=True, worldSpace=True, rotatePivot=True)
                if pivot != [0, 0, 0] and group not in self.summary_transforms:
                    self.summary_transforms.append(group)
                outm.restore_element_transforms(group, group_transforms)

        check_ok = self.return_summary_bool(function, self.summary_transforms)

        return check_ok

    def report_transforms(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_transforms') and self.summary_transforms:
            for e in self.summary_transforms:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_usd_preview(self, function):
        """
        Check if the meshes inside the proxy groups have an usd preview shader assign to them.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.hide_descriptions()
        self.summary_usd_preview = []
        master_grp = outm.get_master_grp_name()
        all_groups = mc.listRelatives(master_grp, allDescendents=True, type="transform")
        for group in all_groups:
            if "proxy_" in group:
                meshes_in_proxy = mc.listRelatives(group, allDescendents=True, type="mesh")
                for mesh in meshes_in_proxy:
                    sg_connections = mc.listConnections(mesh + ".instObjGroups", destination=True, source=False)
                    for sg_connection in sg_connections:
                        shader_connexions = mc.listConnections(sg_connection + ".surfaceShader", destination=False,
                                                               source=True)
                        for shader_connexion in shader_connexions:
                            if mc.nodeType(shader_connexion) != "usdPreviewSurface":
                                self.summary_usd_preview.append(mesh)

        check_ok = self.return_summary_bool(function, self.summary_usd_preview)

        return check_ok

    def report_usd_preview(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_usd_preview') and self.summary_usd_preview:
            for e in self.summary_usd_preview:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_tmp_mat(self, function):
        """
        Check if the meshes inside the render groups have an usd preview shader assign to them.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.hide_descriptions()
        self.summary_tmp_mat = []
        master_grp = outm.get_master_grp_name()
        all_groups = mc.listRelatives(master_grp, allDescendents=True, type="transform")
        for group in all_groups:
            if "render_" in group:
                meshes_in_proxy = mc.listRelatives(group, allDescendents=True, type="mesh")
                for mesh in meshes_in_proxy:
                    sg_connections = mc.listConnections(mesh + ".instObjGroups", destination=True, source=False)
                    for sg_connection in sg_connections:
                        shader_connexions = mc.listConnections(sg_connection + ".surfaceShader", destination=False,
                                                               source=True)
                        for shader_connexion in shader_connexions:
                            if mc.nodeType(shader_connexion) != "usdPreviewSurface":
                                self.summary_tmp_mat.append(mesh)

        check_ok = self.return_summary_bool(function, self.summary_tmp_mat)

        return check_ok

    def report_tmp_mat(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_tmp_mat') and self.summary_tmp_mat:
            for e in self.summary_tmp_mat:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def check_shader_naming(self, function):
        """
        Check if the shaders are correctly named.

        Parameters:
            function (str) : name of the function called when the button is clicked

        Returns :
            bool : True if all conditions are ok
        """
        self.list_report.clear()
        self.hide_descriptions()
        self.summary_shader_naming = []

        master_grp = outm.get_master_grp_name()
        all_groups = mc.listRelatives(master_grp, allDescendents=True, type="transform")
        for group in all_groups:
            if "proxy_" in group:
                short_name = group.split("_")[1]
                standard_sg_name = "usdPrev_" + short_name + "SG"
                standard_shader_name = "usdPrev_" + short_name
                meshes_in_proxy = mc.listRelatives(group, allDescendents=True, type="mesh")
                for mesh in meshes_in_proxy:
                    sg_connections = mc.listConnections(mesh + ".instObjGroups", destination=True, source=False)
                    for sg_connection in sg_connections:
                        if sg_connection != standard_sg_name:
                            self.summary_shader_naming.append(sg_connection)
                        shader_connexions = mc.listConnections(sg_connection + ".surfaceShader", destination=False,
                                                               source=True)
                        for shader_connexion in shader_connexions:
                            if shader_connexion != standard_shader_name:
                                self.summary_shader_naming.append(shader_connexion)
            elif "render_" in group:
                short_name = group.split("_")[1]
                standard_sg_name = "mat_" + short_name + "SG"
                standard_shader_name = "mat_" + short_name
                meshes_in_render = mc.listRelatives(group, allDescendents=True, type="mesh")
                for mesh in meshes_in_render:
                    sg_connections = mc.listConnections(mesh + ".instObjGroups", destination=True, source=False)
                    for sg_connection in sg_connections:
                        if sg_connection != standard_sg_name:
                            self.summary_shader_naming.append(sg_connection)
                        shader_connexions = mc.listConnections(sg_connection + ".surfaceShader", destination=False,
                                                               source=True)
                        for shader_connexion in shader_connexions:
                            if shader_connexion != standard_shader_name:
                                self.summary_shader_naming.append(shader_connexion)

        check_ok = self.return_summary_bool(function, self.summary_shader_naming)

        return check_ok

    def report_shader_naming(self, description):
        self.list_report.clear()
        self.hide_descriptions()
        if hasattr(self, 'summary_shader_naming') and self.summary_shader_naming:
            for e in self.summary_shader_naming:
                self.list_report.addItem(e)
            self.list_report.show()
            self.lbl_[description].show()

    def proxy_sanity_check(self):
        """
        Verifies whether the proxy scene meets cleanliness standards.

        Returns:
            bool: True if all checks pass successfully, indicating the scene is clean.
        """

        checks = [
            self.check_workspace,
            self.check_master_grp,
            self.check_unique_name,
            self.check_empty_group,
            self.check_prp_in_master,
            self.check_purpose_grp_hierarchy,
            self.check_mesh_in_grp,
            self.check_prefix_prp,
            self.check_existing_prp,
            self.check_existing_set,
            self.check_prp_hierarchy_naming,
            self.check_grp_name,
            self.check_history,
            self.check_group_id,
            self.check_ghost_mesh,
            self.check_transforms,
            self.check_usd_preview,
            self.check_shader_naming
        ]

        self.list_report.clear()
        self.hide_descriptions()

        for check in checks:
            if not check(check.__name__):
                return False

        return True

    def prp_sanity_check(self):
        """
        Verifies whether the prop scene meets cleanliness standards.

        Returns:
            bool: True if all checks pass successfully, indicating the scene is clean.
        """
        checks = [
            self.check_workspace,
            self.check_master_grp,
            self.check_unique_name,
            self.check_empty_group,
            self.check_purpose_grp_hierarchy,
            self.check_mesh_in_grp,
            self.check_prp_hierarchy_naming,
            self.check_grp_name,
            self.check_history,
            self.check_group_id,
            self.check_ghost_mesh,
            self.check_transforms,
            self.check_usd_preview,
            self.check_tmp_mat,
            self.check_shader_naming
        ]

        self.list_report.clear()
        self.hide_descriptions()

        for check in checks:
            if not check(check.__name__):
                return False

        return True

    def sanity_check(self):
        """
        Executes the appropriate sanity check based on the context of the file.

        Returns:
            bool: True if the sanity check passes, indicating the context is clean.
        """
        sanity = False
        maya_file_name = mc.file(q=True, sceneName=True, shortName=True)
        asset_type = naco.dict_file_name_part(maya_file_name).get("asset_type")
        if asset_type == "prx":
            sanity = self.proxy_sanity_check()
        elif asset_type == "prp":
            sanity = self.prp_sanity_check()
        return sanity

    def publish_assets(self):
        """
        Publishes the asset if the sanity check passes.

        This function first performs the sanity check and, if successful, publishes the asset
        depending on the asset type (proxy or prop).
        """

        sanity = self.sanity_check()
        maya_file_name = mc.file(q=True, sceneName=True, shortName=True)
        asset_type = naco.dict_file_name_part(maya_file_name).get("asset_type")
        if sanity:
            if asset_type == "prx":
                am.create_asset_from_proxy()
            elif asset_type == "prp":
                am.create_asset_from_prp()
