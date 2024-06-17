import os

import maya.cmds as mc
import maya.mel as mel

from tuyauLigne import arnold_shader as ars
from tuyauLigne import matx_manager as matxm
from tuyauLigne import naming_convention as naco
from tuyauLigne import project_manager as pm


def check_arnold_connection():
    """
    Checks if any mesh in the scene is connected to an aiStandardSurface shader.

    Returns:
        bool: True if an Arnold shader connection is found, False otherwise.
    """
    arnold_connection = False
    render_meshes = mc.listRelatives("render_*", allDescendents=True, fullPath=True, type="mesh")
    for mesh in render_meshes:
        connections = mc.listConnections(mesh + ".instObjGroups", destination=True, source=False)
        for connection in connections:
            shader_connexions = mc.listConnections(connection + ".surfaceShader", destination=False,
                                                   source=True)
        for shader_connexion in shader_connexions:
            if mc.nodeType(shader_connexion) == "aiStandardSurface":
                arnold_connection = True
    return arnold_connection


def list_texture_types():
    """
    Lists the types of textures that are used.

    Returns:
        list: A list of texture type strings.
    """
    texture_types = ["baseColor", "roughness", "metallic", "normal", "emissive", "scatteringMask", "scatteringColor"]
    return texture_types


def get_textures_list(asset_name):
    """
    Gets the list of texture files for a given asset name.

    Parameters:
        asset_name (str): The name of the asset.

    Returns:
        tuple: Contains the textures path and a list of texture files.
    """
    asset_folder = pm.dict_main_folders().get("asset_folder")
    textures_folder = pm.dict_sub_asset_folders().get("texture_map_folder")
    textures_path = os.path.join(asset_folder, asset_name, textures_folder).replace("\\", "/")
    files = os.listdir(textures_path)
    texture_files = [file for file in files if file.endswith('.png')]
    return textures_path, texture_files


def assign_preview_mat():
    """
    Assigns one usdPreviewSurface on all meshes inside proxy groups.
    """
    delete_unused_shaders()
    proxy_groups = mc.ls("proxy_*", type="transform")
    for proxy_group in proxy_groups:
        prp_name = proxy_group.split("_")[1]
        usd_preview = mc.shadingNode("usdPreviewSurface", name=f"usdPrev_{prp_name}", asShader=True)
        usd_preview_sg = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"usdPrev_{prp_name}SG")
        mc.connectAttr(f"{usd_preview}.outColor", f"{usd_preview_sg}.surfaceShader")
        proxy_meshes = mc.listRelatives(proxy_group, allDescendents=True, type="mesh")
        for proxy_mesh in proxy_meshes:
            connections = mc.listConnections(proxy_mesh + ".instObjGroups", destination=True, source=False)
            for connection in connections:
                if mc.nodeType(connection) == 'shadingEngine' and connection != f"usdPrev_{prp_name}SG":
                    mc.select(proxy_mesh)
                    mc.hyperShade(assign=usd_preview)
                    mc.select(d=True)
    delete_unused_shaders()


def assign_tmp_mat():
    """
    Assigns one usdPreviewSurface on all meshes inside render group.
    """
    delete_unused_shaders()
    render_group = mc.ls("render_*", type="transform")
    if len(render_group) != 1:
        print("there is no render group, or more than one render group")
    else:
        render_meshes = mc.listRelatives(render_group, allDescendents=True, type="mesh")
        file_name = naco.get_file_name()
        short_name = naco.dict_file_name_part(file_name).get("asset_short_name")
        usd_preview = mc.shadingNode("usdPreviewSurface", name=f"mat_{short_name}", asShader=True)
        usd_preview_sg = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"mat_{short_name}SG")
        mc.connectAttr(f"{usd_preview}.outColor", f"{usd_preview_sg}.surfaceShader")
        for mesh in render_meshes:
            connections = mc.listConnections(mesh + ".instObjGroups", destination=True, source=False)
            for connection in connections:
                if mc.nodeType(connection) == 'shadingEngine' and connection != f"mat_{short_name}SG":
                    mc.select(mesh)
                    mc.hyperShade(assign=usd_preview)
                    mc.select(d=True)
        delete_unused_shaders()


def assign_matx():
    """
    Assigns a MaterialX shader to all meshes in the render group.
    """
    file_name = naco.get_file_name()
    asset_name = naco.dict_file_name_part(file_name).get("asset_name")
    short_name = naco.dict_file_name_part(file_name).get("asset_short_name")
    render_meshes = mc.listRelatives("render_*", allDescendents=True, fullPath=True, type="mesh")

    textures_path, texture_files = get_textures_list(asset_name)
    matx_stack_shape = matxm.create_matx_stack_shape(short_name)
    matx_path, doc_name = matxm.duplicate_matx_template(textures_path, short_name)
    matxm.import_matx_document(matx_stack_shape, matx_path)
    shader_name, compound_name = matxm.rename_main_nodes(short_name, matx_stack_shape, doc_name)
    texture_types = list_texture_types()
    matxm.set_texture_path(compound_name, textures_path, texture_files, texture_types)
    # matxm.set_color_space(compound_name)
    for mesh in render_meshes:
        mc.materialxAssign(edit=True, assign=True, sourcePath=shader_name, tg=mesh)


def assign_arnold_mat():
    """
    Assigns an Arnold shader to all meshes in the render group.
    """
    delete_unused_shaders()
    file_name = naco.get_file_name()
    asset_name = naco.dict_file_name_part(file_name).get("asset_name")
    short_name = naco.dict_file_name_part(file_name).get("asset_short_name")
    render_meshes = mc.listRelatives("render_*", allDescendents=True, fullPath=True, type="mesh")
    texture_nodes = []
    shading_node, shading_group = ars.create_core_nodes(short_name)
    textures_path, texture_files = get_textures_list(asset_name)
    basecolor_node = ars.create_base_color(short_name, textures_path, texture_files, shading_node)
    roughness_node = ars.create_roughness(short_name, textures_path, texture_files, shading_node)
    metallic_node = ars.create_metallic(short_name, textures_path, texture_files, shading_node)
    scatter_msk_node = ars.create_scattering_mask(short_name, textures_path, texture_files, shading_node)
    normal_node = ars.create_normal(short_name, textures_path, texture_files, shading_node)
    scattercolor_node = ars.create_scattering_color(short_name, textures_path, texture_files, shading_node)
    if basecolor_node:
        texture_nodes.append(basecolor_node)
    if roughness_node:
        texture_nodes.append(roughness_node)
    if metallic_node:
        texture_nodes.append(metallic_node)
    if normal_node:
        texture_nodes.append(normal_node)
    if scatter_msk_node:
        texture_nodes.append(scatter_msk_node)
    if scattercolor_node:
        texture_nodes.append(scattercolor_node)
    ars.connect_placed_texture(short_name, texture_nodes)
    for mesh in render_meshes:
        connections = mc.listConnections(mesh + ".instObjGroups", destination=True, source=False)
        for connection in connections:
            if mc.nodeType(connection) == 'shadingEngine':
                mc.select(mesh)
                mc.hyperShade(assign=shading_node)
                mc.select(d=True)
    delete_unused_shaders()


def delete_unused_shaders():
    """
    Deletes unused shaders in the Maya scene.
    """
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

