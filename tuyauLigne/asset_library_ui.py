import os
import sys

import maya.OpenMayaUI as omui
import maya.cmds as mc

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

from tuyauLigne import project_manager as pm
from tuyauLigne import usd_editor as ue
from tuyauLigne import naming_convention as naco


class AssetLibraryLaunch:
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
            win = AssetLibraryUI(parent=self.parent)

        if win.isHidden():
            win.show()
        else:
            win.raise_()
            win.activateWindow()

        win.show()
        return win


class AssetLibraryUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(AssetLibraryUI, self).__init__(parent)
        self.setWindowTitle("Asset Library")
        self.setMinimumWidth(300)
        self.create_widgets()
        self.initial_state_ui()
        self.create_connections()
        self.create_layout()

    def create_widgets(self):

        self.lbl_search = QtWidgets.QLabel(self)
        self.lbl_search.setText("Search :")

        self.combo_asset_type = QtWidgets.QComboBox(self)
        self.combo_asset_type.setMaximumWidth(60)

        self.entry_search = QtWidgets.QLineEdit()
        self.entry_search.setMaximumHeight(26)

        self.lbl_list_asset = QtWidgets.QLabel(self)
        self.lbl_list_asset.setText("asset list")

        self.list_asset = QtWidgets.QListWidget()

        self.lbl_list_wip = QtWidgets.QLabel(self)
        self.lbl_list_wip.setText("Maya files")

        self.list_wip = QtWidgets.QListWidget()

        self.lbl_list_publish = QtWidgets.QLabel(self)
        self.lbl_list_publish.setText("USD files")

        self.list_publish = QtWidgets.QListWidget()

        self.btn_open = QtWidgets.QPushButton("Open")

        self.btn_ref = QtWidgets.QPushButton("Import as ref")
        self.btn_inc_save = QtWidgets.QPushButton("inc save")

    def create_layout(self):
        # create Hbox and VBox
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.vbox_main = QtWidgets.QVBoxLayout(self)
        self.hbox_search = QtWidgets.QHBoxLayout(self)
        self.hbox_all_lists = QtWidgets.QHBoxLayout(self)
        self.vbox_list_asset = QtWidgets.QVBoxLayout(self)
        self.vbox_list_wip = QtWidgets.QVBoxLayout(self)
        self.vbox_list_publish = QtWidgets.QVBoxLayout(self)
        self.hbox_buttons = QtWidgets.QHBoxLayout(self)

        # layout all the boxes
        self.grid_layout.addLayout(self.vbox_main, 0, 0, 1, 1)
        self.vbox_main.addLayout(self.hbox_search)
        self.vbox_main.addLayout(self.hbox_all_lists)
        self.vbox_main.addLayout(self.hbox_buttons)
        self.hbox_all_lists.addLayout(self.vbox_list_asset)
        self.hbox_all_lists.addLayout(self.vbox_list_wip)
        self.hbox_all_lists.addLayout(self.vbox_list_publish)

        # add widgets to the boxes
        self.hbox_search.addWidget(self.lbl_search)
        self.hbox_search.addWidget(self.combo_asset_type)
        self.hbox_search.addWidget(self.entry_search)
        self.hbox_search.addStretch()

        self.vbox_list_asset.addWidget(self.lbl_list_asset)
        self.vbox_list_asset.addWidget(self.list_asset)

        self.vbox_list_wip.addWidget(self.lbl_list_wip)
        self.vbox_list_wip.addWidget(self.list_wip)

        self.vbox_list_publish.addWidget(self.lbl_list_publish)
        self.vbox_list_publish.addWidget(self.list_publish)

        self.hbox_buttons.addWidget(self.btn_open)
        self.hbox_buttons.addWidget(self.btn_ref)
        self.hbox_buttons.addStretch()
        self.hbox_buttons.addWidget(self.btn_inc_save)

    def create_connections(self):
        self.combo_asset_type.currentIndexChanged.connect(self.update_asset_list)
        self.entry_search.textChanged.connect(self.update_searched_asset)
        self.list_asset.itemClicked.connect(self.display_list_wip)
        self.list_asset.itemClicked.connect(self.display_list_publish)
        self.list_wip.itemClicked.connect(self.clear_list_publish_selection)
        self.list_publish.itemClicked.connect(self.clear_list_wip_selection)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_inc_save.clicked.connect(self.inc_save)
        self.btn_ref.clicked.connect(self.import_ref)

    def initial_state_ui(self):
        my_assets = ["all", "prp", "prx", "set"]
        self.combo_asset_type.addItems(my_assets)

        for asset in self.get_asset_list():
            self.list_asset.addItem(asset)
        for proxy in self.get_proxy_list():
            self.list_asset.addItem(proxy)
        for asset in self.get_set_list():
            self.list_asset.addItem(asset)

    def update_asset_list(self):
        """
        Updates the list of assets based on the asset type selected in the combo box.
        """
        self.list_asset.clear()
        self.list_wip.clear()
        self.list_publish.clear()
        if self.combo_asset_type.currentText() == "all":
            for asset in self.get_asset_list():
                self.list_asset.addItem(asset)
            for asset in self.get_proxy_list():
                self.list_asset.addItem(asset)
            for asset in self.get_set_list():
                self.list_asset.addItem(asset)
        elif self.combo_asset_type.currentText() == "prp":
            for asset in self.get_asset_list():
                self.list_asset.addItem(asset)
        elif self.combo_asset_type.currentText() == "prx":
            for asset in self.get_proxy_list():
                self.list_asset.addItem(asset)
        elif self.combo_asset_type.currentText() == "set":
            for asset in self.get_set_list():
                self.list_asset.addItem(asset)

    def update_searched_asset(self):
        """
        Updates the list of assets based on the entry provided by the user.
        """
        str_searched = self.entry_search.text()
        self.list_asset.clear()
        if not str_searched:
            self.update_asset_list()
        elif self.combo_asset_type.currentText() == "all":
            asset_list = self.get_asset_list()
            proxy_list = self.get_proxy_list()
            set_list = self.get_set_list()
            for asset in asset_list:
                if str_searched in asset:
                    self.list_asset.addItem(asset)
            for proxy in proxy_list:
                if str_searched in proxy:
                    self.list_asset.addItem(proxy)
            for asset in set_list:
                if str_searched in asset:
                    self.list_asset.addItem(asset)

        elif self.combo_asset_type.currentText() == "prp":
            asset_list = self.get_asset_list()
            for asset in asset_list:
                if str_searched in asset:
                    self.list_asset.addItem(asset)
        elif self.combo_asset_type.currentText() == "prx":
            asset_list = self.get_proxy_list()
            for asset in asset_list:
                if str_searched in asset:
                    self.list_asset.addItem(asset)
        elif self.combo_asset_type.currentText() == "set":
            set_list = self.get_set_list()
            for asset in set_list:
                if str_searched in asset:
                    self.list_asset.addItem(asset)

    def get_proxy_list(self):
        """
        Retrieves the list of prx_assets and returns it.

        Returns:
            list: list of prx_assets
        """
        main_proxy_folder = pm.dict_main_folders().get("proxy_folder")
        if os.path.isdir(main_proxy_folder):
            proxy_folders = os.listdir(main_proxy_folder)
        else:
            mc.confirmDialog(message=f"{main_proxy_folder} does not exist", button="ok")
            proxy_folders = None
        return proxy_folders

    def get_asset_list(self):
        """
        Retrieves the list of assets and returns it.

        Returns:
            list: list of assets in the main asset folder
        """
        main_asset_folder = pm.dict_main_folders().get("asset_folder")
        if os.path.isdir(main_asset_folder):
            asset_folders = os.listdir(main_asset_folder)
        else:
            mc.confirmDialog(message=f"{main_asset_folder} does not exist", button="ok")
            asset_folders = None
        return asset_folders

    def get_set_list(self):
        """
        Retrieves the list of sets and returns it.

        Returns:
            list: list of assets in the main env folder
        """
        main_set_folder = pm.dict_main_folders().get("env_folder")
        if os.path.isdir(main_set_folder):
            set_folders = os.listdir(main_set_folder)
        else:
            mc.confirmDialog(message=f"{main_set_folder} does not exist", button="ok")
            set_folders = None
        return set_folders

    def display_list_wip(self):
        """
        Displays the list of WIP modeling files in the list_wip widget.
        """
        asset_name = self.list_asset.currentItem().text()
        asset_type = naco.dict_element_name_part(asset_name).get("element_type")
        self.list_wip.clear()
        if asset_type == "prp":
            wip_folder = pm.get_wip_modeling_folder(asset_name)
            files = os.listdir(wip_folder)
        elif asset_type == "prx":
            proxy_folder = pm.get_proxy_folder(asset_name)
            files = os.listdir(proxy_folder)
        elif asset_type == "set":
            # self.list_wip.clear()
            files = []
        for file in files:
            if file.split(".")[-1] == "ma":
                self.list_wip.addItem(file)
                self.list_wip.sortItems(Qt.DescendingOrder)

    def display_list_publish(self):
        """
        Displays the list of USD published files in the list_publish widget.
        """
        asset_name = self.list_asset.currentItem().text()
        asset_type = naco.dict_element_name_part(asset_name).get("element_type")
        self.list_publish.clear()
        if asset_type == "prp":
            publish_folder = pm.get_wip_usd_folder(asset_name)
            files = os.listdir(publish_folder)

            for file in files:
                if file.split("_")[0] == "prp" and file.split(".")[-1] == "usda":
                    self.list_publish.addItem(file)
                    self.list_publish.sortItems(Qt.DescendingOrder)
        elif asset_type == "set":
            set_wip_folder = pm.get_wip_usd_set_folder(asset_name)
            files = os.listdir(set_wip_folder)

            for file in files:
                if file.split("_")[0] == "set" and file.split(".")[-1] == "usda":
                    self.list_publish.addItem(file)
                    self.list_publish.sortItems(Qt.DescendingOrder)

    def clear_list_wip_selection(self):
        """
        Clears the list_wip widget.
        """
        self.list_wip.clear()
        self.display_list_wip()

    def clear_list_publish_selection(self):
        """
        Clears the list_publish widget.
        """
        self.list_publish.clear()
        self.display_list_publish()

    def open_file(self):
        """
        Opens the file selected by the user.
        """
        asset_name = self.list_asset.currentItem().text()
        asset_type = naco.dict_element_name_part(asset_name).get("element_type")
        if not self.list_wip.currentItem() and not self.list_publish.currentItem():
            mc.confirmDialog(message="no file selected", button="ok")
        elif self.list_wip.currentItem():
            selected_item = self.list_wip.currentItem().text()
            if asset_type == "prp":
                wip_modeling_folder = pm.get_wip_modeling_folder(asset_name)
                file_path = os.path.join(wip_modeling_folder, selected_item)
            if asset_type == "prx":
                proxy_folder = pm.get_proxy_folder(asset_name)
                file_path = os.path.join(proxy_folder, selected_item)
            if mc.file(file_path, q=True, exists=True):
                try:
                    mc.file(file_path, open=True, force=True)
                except RuntimeError as e:
                    mc.confirmDialog(message=f"{e}", button="cancel")
        elif self.list_publish.currentItem().text():
            selected_item = self.list_publish.currentItem().text()
            if asset_type == "prp":
                publish_folder = pm.get_wip_usd_folder(asset_name)
                usd_file_path = os.path.join(publish_folder, selected_item)
                mc.file(new=True, force=True)
                ue.create_prp_layer(asset_name, usd_file_path)
            elif asset_type == "set":
                set_wip_folder = pm.get_wip_usd_set_folder(asset_name)
                usd_file_path = os.path.join(set_wip_folder, selected_item)
                mc.file(new=True, force=True)
                ue.create_prp_layer(asset_name, usd_file_path)

    def inc_save(self):
        """
        inc save for prp and prx
        """
        file_name = mc.file(q=True, sceneName=True, shortName=True)
        asset_type = naco.dict_file_name_part(file_name).get("asset_type")
        asset_name = naco.dict_file_name_part(file_name).get("asset_name")
        inc_number = naco.dict_file_name_part(file_name).get("inc_number")
        inc_number = "{:03d}".format(inc_number + 1)
        if not pm.check_workspace():
            mc.confirmDialog(message="current file is not in the current workspace", button="cancel")
        elif asset_type == "prp":
            wip_folder = pm.get_wip_modeling_folder(asset_name)
            file_path = wip_folder + "/" + asset_name + "_" + inc_number
            mc.file(rename=file_path)
            mc.file(options=";v=0;", typ="mayaAscii", save=True)
            self.clear_list_wip_selection()
        elif asset_type == "prx":
            proxy_folder = pm.get_proxy_folder(asset_name)
            file_path = proxy_folder + "/" + asset_name + "_" + inc_number
            mc.file(rename=file_path)
            mc.file(options=";v=0;", typ="mayaAscii", save=True)
            self.clear_list_wip_selection()

    def import_ref(self):
        """
        Creates a reference inside the current scene of the selected file by the user.
        """
        asset_name = self.list_asset.currentItem().text()
        file_path = ""
        if not self.list_wip.currentItem() and not self.list_publish.currentItem():
            mc.confirmDialog(message="no file selected", button="ok")
        elif self.list_wip.currentItem():
            asset_type = naco.dict_element_name_part(asset_name).get("element_type")
            selected_item = self.list_wip.currentItem().text()
            if asset_type == "prp":
                wip_modeling_folder = pm.get_wip_modeling_folder(asset_name)
                file_path = os.path.join(wip_modeling_folder, selected_item)
            if asset_type == "prx":
                proxy_folder = pm.get_proxy_folder(asset_name)
                file_path = os.path.join(proxy_folder, selected_item)
            if mc.file(file_path, q=True, exists=True):
                try:
                    mc.file(file_path, namespace=asset_name, reference=True, options=";v=0;", typ="mayaAscii",
                            mergeNamespacesOnClash=True)
                except RuntimeError as e:
                    mc.confirmDialog(message=f"{e}", button="cancel")
