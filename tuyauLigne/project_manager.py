import os

import maya.cmds as mc
from tuyauLigne import naming_convention as naco


def create_workspace(parent_folder, project_name):
    """
    Create and set the workspace for the specified project.

    Parameters:
        parent_folder (str): Path of the parent folder of the project.
        project_name (str): Name of the project specified by the user.

    Returns:
        bool: True if the workspace is created, False if it isn't.
    """
    root_project_folder = os.path.join(parent_folder, project_name)
    if not os.path.exists(parent_folder):
        mc.confirmDialog(message=f"parent folder {parent_folder} does not exists or field is empty", button="ok")
        return False
    elif not project_name:
        mc.confirmDialog(message=f"project name field is empty", button="ok")
        return False
    elif not os.path.exists(root_project_folder):
        os.makedirs(root_project_folder)
        mc.workspace(root_project_folder, o=True)
        set_data_workspace()
        mc.workspace(saveWorkspace=True)
        mc.confirmDialog(message="project folder is created", button="ok")
        return True
    else:
        mc.confirmDialog(message="project folder already exist or field is empty", button="ok")
        return False


def set_data_workspace():
    """
    Configure the data folder inside the workspace file according to various data types.

    Sets different file rules in the workspace configuration for various data types such as 'ASS', 'Alembic', 'FBX',
     'OBJ', and others.
    """
    data_folder = dict_main_folders().get("data_folder")
    data_type = ['ASS', 'ASS Export', 'Alembic', 'Arnold-USD', 'BIF', 'CATIAV4_ATF', 'CATIAV5_ATF',
                 'CATIAV5_ATF Export', 'DAE_FBX', 'DAE_FBX export', 'DWG_ATF', 'DWG_ATF Export', 'DXF_ATF',
                 'DXF_ATF Export', 'FBX', 'FBX export', 'IGES_ATF', 'IGES_ATF Export', 'JT_ATF', 'JT_ATF Export',
                 'NX_ATF', 'NX_ATF Export', 'OBJ', 'OBJexport', 'PARASOLID_ATF', 'PARASOLID_ATF Export', 'PROE_ATF',
                 'SAT_ATF', 'SAT_ATF Export', 'STEP_ATF', 'STEP_ATF Export', 'SVG', 'USD Export', 'USD Import',
                 'WIRE_ATF', 'WIRE_ATF Export', 'eps', 'illustrator', 'move', 'translatorData']
    for data in data_type:
        mc.workspace(fileRule=[data, data_folder])


def check_workspace():
    """
    Check if the current scene opened in Maya is in the correct workspace.

    Returns:
        bool: True if the current scene is in the correct workspace, False otherwise.
    """
    project_folder = mc.workspace(q=True, rootDirectory=True)
    file_path = mc.file(q=True, sceneName=True)
    if project_folder in file_path:
        good_workspace = True
    else:
        good_workspace = False
    return good_workspace


def dict_main_folders():
    """
    Store all the main folder paths of the current project.

    Returns:
        dict: All main folders for each key step of the project.
    """
    root_project_folder = mc.workspace(q=True, rootDirectory=True)
    main_folders = {
        "preprod_folder": os.path.join(root_project_folder, "000_preprod"),
        "proxy_folder": os.path.join(root_project_folder, "010_proxy"),
        "asset_folder": os.path.join(root_project_folder, "020_mod_surf"),
        "env_folder": os.path.join(root_project_folder, "030_sets_envs"),
        "shot_folder": os.path.join(root_project_folder, "040_shot_renders"),
        "data_folder": os.path.join(root_project_folder, "999_datas")
    }
    return main_folders


def get_publish_folder(asset_name):
    """
    Get the publish folder within the asset folder.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
        publish_folder (str): Path of the publish folder.
    """
    main_asset_folder = dict_main_folders().get("asset_folder")
    publish_folder = main_asset_folder + "/" + asset_name + "/publish"

    return publish_folder


def get_publish_set_folder(set_name):
    """
    Get the publish folder for a specified set within the environment folder.

    Parameters:
        set_name (str): Name of the set.

    Returns:
        publish_set_folder (str): Path of the publish set folder.
    """
    main_env_folder = dict_main_folders().get("env_folder")
    publish_set_folder = os.path.join(main_env_folder, set_name, "publish")

    return publish_set_folder


def get_wip_modeling_folder(asset_name):
    """
    Get the WIP maya folder within the asset folder.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
        wip_folder (str): Path of the WIP folder.
    """
    main_asset_folder = dict_main_folders().get("asset_folder")
    wip_folder = main_asset_folder + "/" + asset_name + "/wip/maya"

    return wip_folder


def get_wip_usd_folder(asset_name):
    """
    Get the WIP (Work in Progress) USD folder within the asset folder.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
        str: Path of the WIP USD folder.
    """
    main_asset_folder = dict_main_folders().get("asset_folder")
    wip_folder = main_asset_folder + "/" + asset_name + "/wip/usd"

    return wip_folder


def get_proxy_folder(asset_name):
    """
    Get the proxy asset folder within the main proxy folder.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
        str: Path of the proxy folder.
    """
    main_proxy_folder = dict_main_folders().get("proxy_folder")
    proxy_folder = main_proxy_folder + "/" + asset_name

    return proxy_folder


def get_wip_set_folder(set_name):
    """
    Get the WIP folder for a specified set within the environment folder.

    Parameters:
        set_name (str): Name of the asset.

    Returns:
        wip_set_folder (str): Path of the WIP set folder.
    """
    main_env_folder = dict_main_folders().get("env_folder")
    wip_set_folder = os.path.join(main_env_folder, set_name, "wip")

    return wip_set_folder


def get_wip_usd_set_folder(set_name):
    """
    Get the WIP usd folder for a specified set within the environment folder.

    Parameters:
        set_name (str): Name of the asset.

    Returns:
        wip_usd_set_folder (str): Path of the WIP usd set folder.
    """
    main_env_folder = dict_main_folders().get("env_folder")
    wip_usd_set_folder = os.path.join(main_env_folder, set_name, "wip/usd")

    return wip_usd_set_folder


def create_main_folders(main_folders):
    """
    Create the main folders specified in a dictionary inside the project folder.

    Parameters:
        dict: Use the values of main_folders to get the main folders' names.
    """
    root_project_folder = mc.workspace(q=True, rootDirectory=True)
    for main_folder in main_folders.values():
        os.makedirs(os.path.join(root_project_folder, main_folder))


def create_sub_asset_folders(asset_name):
    """
    Create an asset folder inside the main asset folder and add all the sub-folders.

    Parameters:
        asset_name (str): Name of the asset.
    """
    main_asset_folder = dict_main_folders().get("asset_folder")
    asset_sub_folders = {
        "publish_folder": "publish",
        "texture_map_folder": "publish/texture_maps",
        "wip_folder": "wip",
        "wip_maya_folder": "wip/maya",
        "wip_substance_folder": "wip/substance",
        "wip_usd_folder": "wip/usd"
    }

    asset_folder = main_asset_folder + "/" + asset_name
    if not os.path.exists(asset_folder):
        os.makedirs(asset_folder)

    for sub_folder in asset_sub_folders.values():
        os.makedirs(os.path.join(asset_folder, sub_folder))


def create_sub_set_folders(set_name):
    """
    Create a set folder inside the main env folder and add all the sub-folders.

    Parameters:
        set_name (str): Name of the set.
    """
    main_set_folder = dict_main_folders().get("env_folder")
    set_sub_folders = {
        "publish_folder": "publish",
        "wip_folder": "wip",
        "wip_substance_folder": "wip/substance",
        "wip_usd_folder": "wip/usd"
    }
    set_folder = main_set_folder + "/" + set_name
    if not os.path.exists(set_folder):
        os.makedirs(set_folder)

    for sub_folder in set_sub_folders.values():
        os.makedirs(os.path.join(set_folder, sub_folder))


def create_proxy_folder(proxy_name, proxy_folder):
    """
    Create the proxy folder

    Parameters:
        proxy_name (str): Name of the proxy.
        proxy_folder (str): path of the main proxy folder.
    """
    os.makedirs(os.path.join(proxy_folder, proxy_name))


def create_asset_folder(asset_name, asset_folder):
    """
    Create the asset folder

    Parameters:
        asset_name (str): Name of the asset.
        asset_folder (str): path of the main asset folder.
    """
    os.makedirs(os.path.join(asset_folder, asset_name))


def create_env_folder():
    """
    Create an environment folder for a new environment within the environment folder.

    The function also creates a layout folder within the new environment folder.
    """
    env_folder = dict_main_folders().get("env_folder")
    file_name = naco.get_file_name()
    env_name = "env_" + naco.dict_file_name_part(file_name).get("asset_short_name")
    os.makedirs(os.path.join(env_folder, env_name))
    env_path = os.path.join(env_folder, env_name)
    lay_name = "lay_" + naco.dict_file_name_part(file_name).get("asset_short_name")
    os.makedirs(os.path.join(env_path, lay_name))


def create_project(parent_folder, project_name):
    """
    Create the project folder, its workspace, and the main folders within it.

    Parameters:
        parent_folder (str) : path of the parent folder of the project.
        project_name (str): Name of the project.
    """
    workspace = create_workspace(parent_folder, project_name)
    if workspace:
        main_folders = dict_main_folders()
        create_main_folders(main_folders)
