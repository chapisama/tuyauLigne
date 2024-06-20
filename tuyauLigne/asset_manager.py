import os

import maya.cmds as mc

from tuyauLigne import json_manager as jsm
from tuyauLigne import naming_convention as naco
from tuyauLigne import outliner_manager as outm
from tuyauLigne import project_manager as pm
from tuyauLigne import usd_editor as ue


def create_modeling_maya(asset_name):
    """
    Creates the Maya modeling file inside the WIP folder.

    Parameters:
        asset_name (str): Name of the asset.
    """
    mc.select(asset_name, r=True)
    maya_scene_folder = pm.get_wip_modeling_folder(asset_name)
    asset_type = asset_name.split("_")[0]
    maya_file_name = asset_type + "_" + asset_name.split("_")[1] + "_001"
    maya_file_path = maya_scene_folder + "/" + maya_file_name
    mc.file(maya_file_path, options=";v=0;", typ="mayaAscii", pr=True, ch=True, chn=True,
            exportSelected=True, f=True)
    mc.select(d=True)


def create_proxy_maya(asset_name):
    """
    Creates the Maya PRX file inside the PRX asset folder.

    Parameters:
        asset_name (str): Name of the asset.
    """
    proxy_folder = pm.get_proxy_folder(asset_name)
    maya_file_path = proxy_folder + "/" + asset_name + "_001"
    mc.file(new=True, force=True)
    mc.file(rename=maya_file_path)
    mc.file(save=True, type="mayaAscii")
    jsm.add_value(asset_name)


def create_prp_maya(asset_name, asset_folder):
    """
    Creates the Maya PRP file inside the PRP asset folder.

    Parameters:
        asset_name (str): Name of the asset.
        asset_folder (str): Folder of the PRP asset.
    """
    maya_file_path = asset_folder + "/" + asset_name + "/wip/maya/" + asset_name + "_001"
    mc.file(new=True, force=True)
    mc.file(rename=maya_file_path)
    mc.file(save=True, type="mayaAscii")
    jsm.add_value(asset_name)


def create_asset_from_proxy():
    """
    Creates all the asset USD and Maya files for each asset in the Maya proxy scene file currently opened.
    Looks at the name of the groups. For each group starting with PRP, it creates its asset files.
    """
    if not pm.check_workspace():
        print("this maya scene is not in the right workspace")
    elif mc.file(q=True, sceneName=True, shortName=True).split("_")[0] != "prx":
        print("this maya scene is not a proxy scene")
    else:
        all_objects = mc.ls(type="transform")
        asset_list = []
        file_name = naco.get_file_name()
        short_name = naco.dict_file_name_part(file_name).get("asset_short_name")
        main_grp = naco.dict_file_name_part(file_name).get("asset_name")
        set_name = "set_" + short_name
        publish_set_name = set_name + "_publish.usda"
        publish_set_folder = pm.get_publish_set_folder(set_name)
        publish_set_path = os.path.join(publish_set_folder, publish_set_name)

        # create set usd files and folders
        pm.create_sub_set_folders(set_name)
        usd_assembly_path = ue.create_assembly_set_usd(set_name)
        usd_layout_path = ue.create_layout_set_usd(set_name)
        set_usd_path = ue.create_set_usd(set_name, usd_layout_path, usd_assembly_path)

        # create individual assets found in the prx scene
        for obj in all_objects:
            if obj.split("_")[0] == 'prp':
                asset_list.append(obj)

        for asset_name in asset_list:
            publish_folder = pm.get_publish_folder(asset_name)
            publish_file_name = asset_name + "_publish.usdc"
            publish_file_path = os.path.join(publish_folder, publish_file_name)
            if not jsm.check_existing_value(asset_name):
                jsm.add_value(asset_name)
            render_group = outm.create_render_group(asset_name)
            outm.toggle_visibility_on(all_objects)
            outm.unparent(asset_name)
            asset_transforms = outm.store_element_transforms(asset_name)
            outm.center_element_world(asset_name)
            outm.lock_main_attr(asset_name)
            pm.create_sub_asset_folders(asset_name)
            create_modeling_maya(asset_name)
            usd_mod_path = ue.create_mod_sublayer_usd(asset_name)
            usd_surf_path = ue.create_surf_sublayer_usd(asset_name)
            usd_prp_path = ue.create_stage_usd(asset_name, usd_mod_path, usd_surf_path)
            ue.rename_mtl_scope(asset_name)
            ue.flattening_usd_files(usd_prp_path, publish_file_path)
            outm.unlock_main_attr(asset_name)
            outm.restore_element_transforms(asset_name, asset_transforms)
            outm.parent(asset_name, main_grp)
            mc.delete(render_group)
            ue.add_usd_reference(asset_name, usd_assembly_path, publish_file_path)
            ue.edit_prim_xform(usd_assembly_path, asset_name, asset_transforms)

        ue.flattening_usd_files(set_usd_path, publish_set_path)


def create_asset_from_prp():
    """
    Publish the asset USD and Maya file from the 'prp' maya scene.
    """
    if not pm.check_workspace():
        print("this maya scene is not in the right workspace")
    elif mc.file(q=True, sceneName=True, shortName=True).split("_")[0] != "prp":
        print("this maya scene is not a prop scene")
    else:
        all_objects = mc.ls(type="transform")
        outm.toggle_visibility_on(all_objects)
        asset_name = outm.get_master_grp_name()
        publish_folder = pm.get_publish_folder(asset_name)
        publish_file_name = asset_name + "_publish.usdc"
        publish_file_path = os.path.join(publish_folder, publish_file_name)
        if not jsm.check_existing_value(asset_name):
            jsm.add_value(asset_name)
        usd_mod_path = ue.create_mod_sublayer_usd(asset_name)
        usd_surf_path = ue.create_surf_sublayer_usd(asset_name)
        usd_prp_path = ue.create_stage_usd(asset_name, usd_mod_path, usd_surf_path)
        ue.rename_mtl_scope(asset_name)
        ue.flattening_usd_files(usd_prp_path, publish_file_path)
