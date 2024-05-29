import json
import os

from tuyauLigne import project_manager as pm


def create_production_tracker():
    """
    Creates the production_tracker.json inside the data folder.
    """
    data = {'assets': [{
        "name": "no_assets",
        "Modeling": "TODO",
        "UV unfold": "TODO",
        "Surfacing": "TODO"
    }]}
    file_path = os.path.join(pm.dict_main_folders().get("data_folder"), 'production_tracker.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def add_value(asset_name):
    """
    Adds a dictionary of values of the asset inside the production_tracker.json file.

    Parameters:
        asset_name (str): Name of the asset.
    """
    file_path = os.path.join(pm.dict_main_folders().get("data_folder"), 'production_tracker.json')
    with open(file_path, 'r') as f:
        datas = json.load(f)
        if datas['assets'][0]['name'] == "no_assets":
            datas['assets'][0] = {
                "name": asset_name,
                "Modeling": "TODO",
                "UV unfold": "TODO",
                "Surfacing": "TODO"
            }
        else:
            new_asset = {
                "name": asset_name,
                "Modeling": "TODO",
                "UV unfold": "TODO",
                "Surfacing": "TODO"
            }
            datas['assets'].append(new_asset)
            datas['assets'] = sorted(datas['assets'], key=lambda x: x['name'])
    with open(file_path, 'w') as f:
        json.dump(datas, f, indent=2)


def check_existing_value(asset_name):
    """
    Checks if an asset is already inside the production tracker file.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
        bool: True if the asset is already in the production tracker file.
    """
    existing_value = False
    file_path = os.path.join(pm.dict_main_folders().get("data_folder"), 'production_tracker.json')
    with open(file_path, 'r') as f:
        datas = json.load(f)
    for data in datas['assets']:
        if asset_name == data['name']:
            existing_value = True
    return existing_value
