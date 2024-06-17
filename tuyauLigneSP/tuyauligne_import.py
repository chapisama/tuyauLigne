import json
import os

import substance_painter.project
from PySide2 import QtWidgets

from tuyauLigneSP import project_manager as pm


def get_prp_list(combo_project_list):
    asset_folder = pm.dict_main_folders(combo_project_list).get("asset_folder")
    prop_folders = os.listdir(asset_folder)
    prop_list = []
    for folder in prop_folders:
        if "prp_" in folder:
            prop_list.append(folder)

    return prop_list


def get_set_list(combo_project_list):
    env_folder = pm.dict_main_folders(combo_project_list).get("env_folder")
    env_folders = os.listdir(env_folder)
    set_list = []
    for folder in env_folders:
        if "set_" in folder:
            set_list.append(folder)

    return set_list


def select_folder(entry_add_project):
    """
    Open a folder selection dialog and return the selected folder path.

    Parameters:
        entry_add_project (QLineEdit): The input field where the selected folder path will be set.
    """
    dialog = QtWidgets.QFileDialog()
    dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    if dialog.exec_():
        folder_path = dialog.selectedFiles()[0]
        entry_add_project.setText(folder_path)


def save_project(spp_file):
    """
    Save the current project to the specified file path.

    Parameters:
        spp_file (str): The file path where the project will be saved.
    """
    substance_painter.project.save_as(project_file_path=spp_file)


def set_settings(combo_subdiv, combo_udim):
    subdiv_level = int(combo_subdiv.currentText())
    udim = False
    if combo_udim.currentText() == "no":
        udim = False
    elif combo_udim.currentText() == "yes":
        udim = True

    if udim == True:
        project_workflow = substance_painter.project.ProjectWorkflow.UVTile
    else:
        project_workflow = substance_painter.project.ProjectWorkflow.Default

    usd_settings = substance_painter.project.UsdSettings(
        subdivision_level=subdiv_level
    )
    settings = substance_painter.project.Settings(
        usd_settings=usd_settings,
        project_workflow=project_workflow
    )
    return settings


def create_project(list_asset, combo_project_list, combo_subdiv, combo_udim):
    """
    Create or open a project based on the selected asset and project from the UI.
    If a project is already open, it will be closed before opening the new project.

    Parameters:
        list_asset (QListWidget): The widget containing the list of assets.
        combo_project_list (QComboBox): The combo box containing the list of projects.
        combo_subdiv (QComboBox) : the combo box containing the subdivision level.
        combo_udim (QComboBox) : the combo box containing the UV workflow, with or without udim.
    """

    if list_asset.currentItem() is None:
        print("No asset selected.")
        return

    asset_name = list_asset.currentItem().text()
    project_name = combo_project_list.currentText()
    spp_file_path = ""
    project_path = pm.get_project_path(project_name)

    if substance_painter.project.is_open():
        substance_painter.project.close()

    if project_path:
        if "prp_" in asset_name:
            spp_file_path = os.path.join(pm.dict_main_folders(combo_project_list).get("asset_folder"), asset_name,
                                         "wip",
                                         "substance")
        elif "set_" in asset_name:
            spp_file_path = os.path.join(pm.dict_main_folders(combo_project_list).get("env_folder"), asset_name, "wip",
                                         "substance")
        if pm.check_existing_spp(spp_file_path):
            spp_file = os.path.join(spp_file_path, f"{asset_name}_001.spp")
            substance_painter.project.open(project_file_path=spp_file)
        else:
            if "prp_" in asset_name:
                usd_file_path = os.path.join(pm.dict_main_folders(combo_project_list).get("asset_folder"), asset_name,
                                             "publish",
                                             f"{asset_name}_publish.usdc")
                spp_file = os.path.join(spp_file_path, f"{asset_name}_001.spp")
                settings = set_settings(combo_subdiv, combo_udim)
                substance_painter.project.create(mesh_file_path=usd_file_path, settings=settings)

                def save_callback():
                    save_project(spp_file)

                substance_painter.project.execute_when_not_busy(save_callback)

            elif "set_" in asset_name:
                usd_file_path = os.path.join(pm.dict_main_folders(combo_project_list).get("env_folder"), asset_name,
                                             "publish",
                                             f"{asset_name}_publish.usda")
                spp_file = os.path.join(spp_file_path, f"{asset_name}_001.spp")
                substance_painter.project.create(mesh_file_path=usd_file_path)

                def save_callback():
                    save_project(spp_file)

                substance_painter.project.execute_when_not_busy(save_callback)
    else:
        print("no project path found")


def add_project(entry_add_project, combo_project_list, list_asset):
    """
    Add a new project to the project list by specifying its path.
    If the project is valid and not already in the list, it will be added.

    Parameters:
        entry_add_project (QLineEdit): The input field containing the path to the new project.
        combo_project_list (QComboBox): The combo box containing the list of projects.
        list_asset (QListWidget): The widget containing the list of assets.
    """
    project_already_existing = False
    project_path = entry_add_project.text().replace("/", "\\")
    if not project_path:
        print("no path specified")
    elif "\\" not in project_path:
        print("entry is not a valid path")
    elif not pm.check_folder_content(project_path):
        print("the folder has not a correct project")
    else:
        project_name = project_path.split("\\")[-1]
        file_path = pm.get_json_path()
        with open(file_path, 'r') as f:
            datas = json.load(f)
            for data in datas["projects"]:
                if project_name == data["name"]:
                    project_already_existing = True
                    break
            if not project_already_existing:
                datas["last_project"] = project_name
            if datas['projects'][0]['name'] == "no_projects":
                combo_project_list.addItem(project_name)
                combo_project_list.setCurrentText(project_name)

                datas['projects'][0] = {
                    "name": project_name,
                    "project_path": project_path,
                }
                load_asset_list(project_path, list_asset)
            elif not project_already_existing:
                combo_project_list.addItem(project_name)
                combo_project_list.setCurrentText(project_name)

                new_project = {
                    "name": project_name,
                    "project_path": project_path,
                }
                load_asset_list(project_path, list_asset)
                datas['projects'].append(new_project)
                datas['projects'] = sorted(datas['projects'], key=lambda x: x['name'])
        with open(file_path, 'w') as f:
            json.dump(datas, f, indent=2)


def remove_project(combo_project_list, list_asset):
    """
    Remove the selected project from the project list.

    Parameters:
        combo_project_list (QComboBox): The combo box containing the list of projects.
        list_asset (QListWidget): The widget containing the list of assets.
    """
    project_name = combo_project_list.currentText()
    if project_name == "":
        print("No project selected.")
        return

    file_path = pm.get_json_path()
    project_found = False
    with open(file_path, 'r') as f:
        datas = json.load(f)
    for data in datas["projects"]:
        if project_name == data["name"]:
            datas["projects"].remove(data)
            project_found = True
            break

    if project_found:
        # Write the updated project list back to the JSON file
        with open(file_path, 'w') as f:
            json.dump(datas, f, indent=2)

        # Remove the project from the combo box and reset the asset list
        combo_project_list.removeItem(combo_project_list.currentIndex())
        project_name = combo_project_list.currentText()
        for data in datas["projects"]:
            if project_name == data["name"]:
                project_path = data["project_path"]
                load_asset_list(project_path, list_asset)
                break

        # If no projects are left, add a placeholder
        if combo_project_list.count() == 0:
            list_asset.clear()
            no_project = {
                "name": "no_projects",
                "project path": "no_path"
            }
            datas['projects'].append(no_project)
            datas['last_project'] = "no_project"
            with open(file_path, 'w') as f:
                json.dump(datas, f, indent=2)
    else:
        print("Project not found in the list.")


def load_asset_list(project_path, list_asset):
    """
    Populate the asset list widget with assets found in the specified project path.

    Parameters:
        project_path (str): The path to the project folder.
        list_asset (QListWidget): The widget where the assets will be listed.
    """
    list_asset.clear()
    asset_main_folder = os.path.join(project_path, pm.dict_folders_alone().get("asset_folder"))
    if os.path.isdir(asset_main_folder):
        asset_folders = os.listdir(asset_main_folder)
        for asset in asset_folders:
            list_asset.addItem(asset)
    else:
        print(f"The folder {asset_main_folder} does not exist.")

    set_main_folder = os.path.join(project_path, pm.dict_folders_alone().get("env_folder"))
    if os.path.isdir(set_main_folder):
        set_folders = os.listdir(set_main_folder)
        for set in set_folders:
            list_asset.addItem(set)
    else:
        print(f"The folder {set_main_folder} does not exist.")


def update_asset_list(combo_project_list, list_asset):
    """
    Update the asset list based on the currently selected project.

    Parameters:
        combo_project_list (QComboBox): The combo box containing the list of projects.
        list_asset (QListWidget): The widget where the assets will be listed.
    """
    project_name = combo_project_list.currentText()
    project_path = pm.get_project_path(project_name)
    file_path = pm.get_json_path()

    if project_path:
        load_asset_list(project_path, list_asset)
    with open(file_path, 'r') as f:
        datas = json.load(f)
    datas["last_project"] = project_name
    with open(file_path, 'w') as f:
        json.dump(datas, f, indent=2)


def update_searched_asset(combo_project_list, combo_asset_type, entry_search, list_asset):
    """
    Updates the list of assets based on the entry provided by the user.
    """

    prp_list = get_prp_list(combo_project_list)
    set_list = get_set_list(combo_project_list)
    str_searched = entry_search.text()
    asset_type = combo_asset_type.currentText()

    list_asset.clear()
    if not str_searched:
        if asset_type == "all":
            update_asset_list(combo_project_list, list_asset)
        elif asset_type == "prp":
            for prp in prp_list:
                list_asset.addItem(prp)
        elif asset_type == "set":
            for set in set_list:
                list_asset.addItem(set)

    elif asset_type == "all":
        for prp in prp_list:
            if str_searched in prp:
                list_asset.addItem(prp)
        for set in set_list:
            if str_searched in set:
                list_asset.addItem(set)

    elif asset_type == "prp":
        for prp in prp_list:
            if str_searched in prp and "prp_" in prp:
                list_asset.addItem(prp)

    elif asset_type == "set":
        for set in set_list:
            if str_searched in set and "set_" in set:
                list_asset.addItem(set)


def create_ui():
    """
    Create the user interface for the plugin, including widgets and layout.
    Initialize the UI with project and asset data.

    Returns:
        QWidget: The main widget containing the plugin's UI.
    """
    asset_type = ["all", "prp", "set"]
    subdiv = ["0", "1", "2"]
    with_udim = ["no", "yes"]
    project_list = []

    # Create the main widgets
    import_widget = QtWidgets.QWidget()
    import_layout = QtWidgets.QVBoxLayout(import_widget)
    import_widget.setWindowTitle("Tuyau Ligne Open ")

    # Creates the boxes
    hbox_add_project = QtWidgets.QHBoxLayout()
    hbox_project_list = QtWidgets.QHBoxLayout()
    hbox_search = QtWidgets.QHBoxLayout()
    hbox_asset_list = QtWidgets.QHBoxLayout()
    hbox_import = QtWidgets.QHBoxLayout()

    # Creates the widgets
    lbl_add_project = QtWidgets.QLabel()
    lbl_add_project.setText("Add a project :")
    entry_add_project = QtWidgets.QLineEdit()
    btn_search_project = QtWidgets.QPushButton("...")
    btn_search_project.setMaximumWidth(26)
    btn_add_project = QtWidgets.QPushButton("+")
    btn_add_project.setMaximumWidth(26)

    lbl_project_list = QtWidgets.QLabel()
    lbl_project_list.setText("Project list :")
    combo_project_list = QtWidgets.QComboBox()
    combo_project_list.setMinimumWidth(200)
    btn_remove_project = QtWidgets.QPushButton("-")

    lbl_search = QtWidgets.QLabel()
    lbl_search.setText("Search :")
    combo_asset_type = QtWidgets.QComboBox()
    entry_search = QtWidgets.QLineEdit()

    list_asset = QtWidgets.QListWidget()

    lbl_udim = QtWidgets.QLabel()
    lbl_udim.setText("UDIM :")
    combo_udim = QtWidgets.QComboBox()
    lbl_subdiv = QtWidgets.QLabel()
    lbl_subdiv.setText("Subdiv :")
    combo_subdiv = QtWidgets.QComboBox()
    btn_open = QtWidgets.QPushButton("open")
    btn_open.setMaximumWidth(26)

    # add the widgets to the boxes
    hbox_add_project.addWidget(lbl_add_project)
    hbox_add_project.addWidget(entry_add_project)
    hbox_add_project.addWidget(btn_search_project)
    hbox_add_project.addWidget(btn_add_project)

    hbox_project_list.addWidget(lbl_project_list)
    hbox_project_list.addWidget(combo_project_list)
    hbox_project_list.addWidget(btn_remove_project)
    hbox_project_list.addStretch()

    hbox_search.addWidget(lbl_search)
    hbox_search.addWidget(combo_asset_type)
    hbox_search.addWidget(entry_search)

    hbox_asset_list.addWidget(list_asset)

    hbox_import.addStretch()
    hbox_import.addWidget(lbl_udim)
    hbox_import.addWidget(combo_udim)
    hbox_import.addWidget(lbl_subdiv)
    hbox_import.addWidget(combo_subdiv)
    hbox_import.addWidget(btn_open)

    # add the boxes to the main box
    import_layout.addLayout(hbox_add_project)
    import_layout.addLayout(hbox_project_list)
    import_layout.addLayout(hbox_search)
    import_layout.addLayout(hbox_asset_list)
    import_layout.addLayout(hbox_import)

    # sets initial states
    lbl_udim.hide()
    lbl_subdiv.hide()
    # gets the project list in the json file
    file_path = pm.get_json_path()
    with open(file_path, 'r') as f:
        datas = json.load(f)
    for data in datas['projects']:
        if data["name"] != "no_projects":
            project_list.append(data["name"])
    combo_project_list.addItems(project_list)
    # looks at the last selected project
    last_project = datas['last_project']
    if last_project != "no_project":
        combo_project_list.setCurrentText(last_project)
    # creates the asset list of the project
    project_name = combo_project_list.currentText()
    for data in datas['projects']:
        if data["name"] == project_name:
            project_path = data["project_path"]
            load_asset_list(project_path, list_asset)
    # sets the remaining combo boxes
    combo_asset_type.addItems(asset_type)
    combo_udim.addItems(with_udim)
    combo_udim.hide()
    combo_subdiv.addItems(subdiv)
    combo_subdiv.hide()

    # creates connexions
    btn_search_project.clicked.connect(lambda: select_folder(entry_add_project))
    btn_open.clicked.connect(lambda: create_project(list_asset, combo_project_list, combo_subdiv, combo_udim))
    btn_add_project.clicked.connect(lambda: add_project(entry_add_project, combo_project_list, list_asset))
    btn_remove_project.clicked.connect(lambda: remove_project(combo_project_list, list_asset))
    combo_asset_type.currentIndexChanged.connect(
        lambda: update_searched_asset(combo_project_list, combo_asset_type, entry_search, list_asset))
    entry_search.textChanged.connect(
        lambda: update_searched_asset(combo_project_list, combo_asset_type, entry_search, list_asset))
    combo_project_list.currentIndexChanged.connect(lambda: update_asset_list(combo_project_list, list_asset))
    combo_subdiv.currentIndexChanged.connect(lambda: set_settings(combo_subdiv, combo_udim))
    combo_udim.currentIndexChanged.connect(lambda: set_settings(combo_subdiv, combo_udim))
    list_asset.itemClicked.connect(
        lambda: toggle_visibility_parameters(combo_project_list, list_asset, combo_subdiv, combo_udim, lbl_subdiv,
                                             lbl_udim, btn_open))
    return import_widget


def toggle_visibility_parameters(combo_project_list, list_asset, combo_subdiv, combo_udim, lbl_subdiv, lbl_udim,
                                 btn_open):
    asset_name = list_asset.currentItem().text()
    widgets = [combo_subdiv, combo_udim, lbl_subdiv, lbl_udim]
    if "prp_" in asset_name:
        spp_file_path = os.path.join(pm.dict_main_folders(combo_project_list).get("asset_folder"), asset_name, "wip",
                                     "substance")
    elif "set_" in asset_name:
        spp_file_path = os.path.join(pm.dict_main_folders(combo_project_list).get("env_folder"), asset_name, "wip",
                                     "substance")

    if pm.check_existing_spp(spp_file_path):
        for widget in widgets:
            if widget.isVisible():
                widget.hide()
        btn_open.setText("open")

    else:
        for widget in widgets:
            if widget.isHidden():
                widget.show()
        btn_open.setText("import")
