import json
import os

import substance_painter.project


def get_json_path():
    """
    Get the path to the JSON file that contains the project list.

    Returns:
        str: The file path to the project_list.json file.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(script_dir, "project_list.json")
    return json_file_path


def get_project_path(project_name):
    """
    Get the project path for the specified project name from the JSON file.

    Parameters:
        project_name (str): The name of the project.

    Returns:
        str: The path to the project directory if found, otherwise an empty string.
    """
    project_path = ""
    json_file_path = get_json_path()
    with open(json_file_path, 'r') as f:
        datas = json.load(f)
        for data in datas['projects']:
            if project_name == data['name']:
                project_path = data["project_path"]
                break
    return project_path


def get_current_project_path():
    current_file_path = substance_painter.project.file_path()
    return current_file_path


def dict_split_folders():
    file_path = get_current_project_path()
    split_path = file_path.replace('\\', '/').split('/')
    dict_folders = {
        "file_name": split_path[-1],
        "wip_spp_folder": os.path.join(split_path[-3], split_path[-2]),
        "asset_folder": split_path[-4],
        "dpt_folder": split_path[-5],
        "project_folder": file_path.replace('\\', '/').replace('/'.join(split_path[-5:]), '').rstrip('/')
    }
    return dict_folders


def get_textures_folder():
    project_folder = dict_split_folders().get("project_folder")
    dpt_folder = dict_split_folders().get("dpt_folder")
    asset_folder = dict_split_folders().get("asset_folder")
    textures_folder = os.path.join(project_folder, dpt_folder, asset_folder, "publish", "texture_maps").replace(
        '\\', '/')
    return textures_folder


def dict_folders_alone():
    """
    Get a dictionary of standalone folder names for assets and environments.

    Returns:
        dict: A dictionary with keys 'asset_folder' and 'env_folder' pointing to their respective folder names.
    """
    dict_folder_alone = {
        "asset_folder": "020_mod_surf",
        "env_folder": "030_sets_envs",
        "data_folder": "999_datas"
    }
    return dict_folder_alone


def dict_main_folders(combo_project_list):
    """
    Get the main folders for assets and environments based on the selected project.

    Parameters:
        combo_project_list (QComboBox): The combo box containing the list of projects.

    Returns:
        dict: A dictionary containing paths to the asset and environment folders.
    """
    project_name = combo_project_list.currentText()
    project_path = get_project_path(project_name)
    dict_main_folder = {
        "asset_folder": os.path.join(project_path, dict_folders_alone().get("asset_folder")),
        "env_folder": os.path.join(project_path, dict_folders_alone().get("env_folder")),
    }
    return dict_main_folder


def check_folder_content(project_path):
    """
    Check if the specified folder contains the expected subdirectory structure for a project.

    Parameters:
        project_path (str): The path to the project folder.

    Returns:
        bool: True if the folder contains the expected subdirectory, False otherwise.
    """
    target_folder = os.path.join(project_path, dict_folders_alone().get("data_folder"))

    # Check if the folder exists
    return os.path.isdir(target_folder)


def check_existing_spp(spp_file_path):
    """
    Check if there are any existing .spp files in the specified path.

    Parameters:
        spp_file_path (str): The path to check for existing .spp files.

    Returns:
        bool: True if there are existing .spp files, False otherwise.
    """
    files = os.listdir(spp_file_path)
    existing_spp = False
    for file in files:
        if ".spp" in file:
            existing_spp = True
            break
    return existing_spp


def rename_textures():
    textures_folder = get_textures_folder()
    files = os.listdir(textures_folder)
    for file in files:
        if os.path.isfile(os.path.join(textures_folder, file)):
            if "SG_" in file:
                new_name = file.replace("SG_", "_")
                old_path = os.path.join(textures_folder, file)
                new_path = os.path.join(textures_folder, new_name)
                os.replace(old_path, new_path)
