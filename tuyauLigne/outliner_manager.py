import maya.cmds as mc

from tuyauLigne import naming_convention as naco


def get_master_grp_name():
    """
    Gets the master group name by looking at the file name.

    Returns:
        str: Name of the master group.
    """
    file_name = mc.file(q=True, sceneName=True, shortName=True)
    master_grp = naco.dict_file_name_part(file_name).get("asset_name")
    return master_grp


def lock_main_attr(element):
    """
    Locks the translate, rotate, and scale attributes of the element.

    Parameters:
        element (str): Name of the element. Can be a group, a mesh, etc.
    """
    attributs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]

    for attribut in attributs:
        mc.setAttr(f"{element}.{attribut}", lock=True)


def unlock_main_attr(element):
    """
    Unlocks the translate, rotate, and scale attributes of the element.

    Parameters:
        element (str): Name of the element. Can be a group, a mesh, etc.
    """
    attributs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]

    for attribut in attributs:
        mc.setAttr(f"{element}.{attribut}", lock=False)


def unparent(asset_name):
    """
    Unparents the given asset group.

    Parameters:
        asset_name (str): Name of the asset.
    """
    mc.parent(asset_name, world=True)


def parent(asset_name, main_grp):
    """
    Parents the given asset group to the main group.

    Parameters:
        asset_name (str): Name of the asset.
        main_grp (str): Name of the main group, same as the file name.
    """
    mc.parent(asset_name, main_grp)


def toggle_visibility_on(element_list):
    """
    Turns on the visibility for a list of elements.

    Parameters:
        element_list (list): List of elements to change visibility.
    """
    for element in element_list:
        mc.setAttr(f'{element}.visibility', 1)


def store_element_transforms(asset_name):
    """
    Stores the translate and rotate transforms of the asset.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
         dict: Stores the transforms. Keys: tx, ty, tz, rx, ry, rz.
    """
    asset_transforms = {
        "tx": mc.getAttr(f"{asset_name}.tx"),
        "ty": mc.getAttr(f"{asset_name}.ty"),
        "tz": mc.getAttr(f"{asset_name}.tz"),
        "rx": mc.getAttr(f"{asset_name}.rx"),
        "ry": mc.getAttr(f"{asset_name}.ry"),
        "rz": mc.getAttr(f"{asset_name}.rz"),
        "sx": mc.getAttr(f"{asset_name}.sx"),
        "sy": mc.getAttr(f"{asset_name}.sy"),
        "sz": mc.getAttr(f"{asset_name}.sz"),
    }

    return asset_transforms


def center_element_world(asset_name):
    """
    Places the asset at the center of world coordinates, and rotates it to 0,0,0.

    Parameters:
        asset_name (str): Name of the asset.
    """
    transforms = ["tx", "ty", "tz", "rx", "ry", "rz"]
    for transform in transforms:
        mc.setAttr(f"{asset_name}.{transform}", 0)


def restore_element_transforms(asset_name, asset_transforms):
    """
    Restores the transforms of the asset stored in the asset_transforms dict.

    Parameters:
        asset_name (str): Name of the asset.
        asset_transforms (dict): Translate and rotate of the asset.
    """
    for key, value in asset_transforms.items():
        mc.setAttr(f"{asset_name}.{key}", value)


def create_render_group(prp_group):
    """
    Creates the render_asset group inside the PRP group.

    Parameters:
        prp_group (str): Name of the PRP group where you want to add the render group.

    Returns:
        str: Name of the render_asset group.
    """
    prp_transforms = store_element_transforms(prp_group)

    short_name = prp_group.split("_")[1]
    render_group = mc.group(name=f"render_{short_name}", empty=True)
    for key, value in prp_transforms.items():
        mc.setAttr(f"{render_group}.{key}", value)
    mc.parent(render_group, prp_group)
    return render_group
