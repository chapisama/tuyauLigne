import os

import maya.cmds as mc

from tuyauLigne import material_manager as matm
from tuyauLigne import naming_convention as naco


def create_core_nodes(short_name):
    """
    Creates the core shading nodes including an aiStandardSurface shader and a shading group.

    Parameters:
        short_name (str): The short name of the asset.

    Returns:
        tuple: Contains the created shading node and shading group.
    """
    shading_node = mc.shadingNode('aiStandardSurface', asShader=True, name=f'mat_{short_name}')
    shading_group = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'mat_{short_name}_SG')
    mc.connectAttr(f'{shading_node}.outColor', f'{shading_group}.surfaceShader')
    return shading_node, shading_group


def create_base_color(short_name, textures_path, texture_files, shading_node):
    """
    Creates and connects the base color texture to the shading node.

    Parameters:
        short_name (str): The short name for the asset.
        textures_path (str): The directory path where texture files are located.
        texture_files (list): List of texture file names.
        shading_node (str): The shading node to which the texture will be connected.

    Returns:
        str: The created base color texture node.
    """
    basecolor_files = []
    texture_to_set = ""
    basecolor_node = None

    for texture_file in texture_files:
        if "_baseColor" in texture_file and "mat_" in texture_file:
            basecolor_files.append(texture_file)
            if len(basecolor_files) == 1:
                texture_to_set = texture_file
            if len(basecolor_files) > 1:
                for basecolor_file in basecolor_files:
                    if "1001" in basecolor_file:
                        texture_to_set = basecolor_file

    if basecolor_files:
        basecolor_path = os.path.join(textures_path, texture_to_set).replace("\\", "/")
        basecolor_node = mc.shadingNode('aiImage', asTexture=True, name=f'img_baseColor_{short_name}')
        color_correct_node = mc.shadingNode("aiColorCorrect", asUtility=True,
                                            name=f"colorCorrect_baseColor_{short_name}")
        mc.connectAttr(f'{basecolor_node}.outColor', f'{color_correct_node}.input')
        mc.connectAttr(f'{color_correct_node}.outColor', f'{shading_node}.baseColor')

        mc.setAttr(f'{basecolor_node}.filename', f'{basecolor_path}', type='string')
        mc.setAttr(f'{basecolor_node}.ignoreColorSpaceFileRules', True)
        mc.setAttr(f'{basecolor_node}.colorSpace', "sRGB", type='string')
        mc.setAttr(f'{basecolor_node}.autoTx', 0)
        if "1001" in texture_to_set:
            mc.setAttr(f'{basecolor_node}.uvTilingMode', 3)

    return basecolor_node


def create_roughness(short_name, textures_path, texture_files, shading_node):
    """
    Creates and connects the roughness texture to the shading node.

    Parameters:
        short_name (str): The short name for the asset.
        textures_path (str): The directory path where texture files are located.
        texture_files (list): List of texture file names.
        shading_node (str): The shading node to which the texture will be connected.

    Returns:
        str: The created roughness texture node.
    """
    roughness_files = []
    texture_to_set = ""
    roughness_node = None

    for texture_file in texture_files:
        if "_roughness" in texture_file and "mat_" in texture_file:
            roughness_files.append(texture_file)
            if len(roughness_files) == 1:
                texture_to_set = texture_file
            if len(roughness_files) > 1:
                for roughness_file in roughness_files:
                    if "1001" in roughness_file:
                        texture_to_set = roughness_file

    if roughness_files:
        roughness_path = os.path.join(textures_path, texture_to_set).replace("\\", "/")
        roughness_node = mc.shadingNode('aiImage', asTexture=True, name=f'img_roughness_{short_name}')
        range_node = mc.shadingNode("aiRange", asUtility=True, name=f"range_roughness_{short_name}")
        clamp_node = mc.shadingNode("aiClamp", asUtility=True, name=f"clamp_roughness_{short_name}")
        color_to_float = mc.shadingNode("aiColorToFloat", asUtility=True, name="color_to_float_roughness")
        mc.connectAttr(f'{roughness_node}.outColor ', f'{range_node}.input')
        mc.connectAttr(f'{range_node}.outColor', f'{clamp_node}.input')
        mc.connectAttr(f'{clamp_node}.outColor', f'{color_to_float}.input')
        mc.connectAttr(f'{color_to_float}.outValue', f'{shading_node}.specularRoughness')

        mc.setAttr(f'{roughness_node}.filename', f'{roughness_path}', type='string')
        mc.setAttr(f'{roughness_node}.ignoreColorSpaceFileRules', True)
        mc.setAttr(f'{roughness_node}.colorSpace', "Raw", type='string')
        mc.setAttr(f'{roughness_node}.autoTx', 0)
        if "1001" in texture_to_set:
            mc.setAttr(f'{roughness_node}.uvTilingMode', 3)

    return roughness_node


def create_metallic(short_name, textures_path, texture_files, shading_node):
    """
    Creates and connects the metallic texture to the shading node.

    Parameters:
        short_name (str): The short name for the asset.
        textures_path (str): The directory path where texture files are located.
        texture_files (list): List of texture file names.
        shading_node (str): The shading node to which the texture will be connected.

    Returns:
        str: The created metallic texture node.
    """
    metallic_files = []
    texture_to_set = ""
    metallic_node = None

    for texture_file in texture_files:
        if "_metallic" in texture_file and "mat_" in texture_file:
            metallic_files.append(texture_file)
            if len(metallic_files) == 1:
                texture_to_set = texture_file
            if len(metallic_files) > 1:
                for metallic_file in metallic_files:
                    if "1001" in metallic_file:
                        texture_to_set = metallic_file

    if metallic_files:
        metallic_path = os.path.join(textures_path, texture_to_set).replace("\\", "/")
        metallic_node = mc.shadingNode('aiImage', asTexture=True, name=f'img_metallic_{short_name}')
        range_node = mc.shadingNode("aiRange", asUtility=True, name=f"range_metallic_{short_name}")
        clamp_node = mc.shadingNode("aiClamp", asUtility=True, name=f"clamp_metallic_{short_name}")
        color_to_float = mc.shadingNode("aiColorToFloat", asUtility=True, name="color_to_float_metallic")
        mc.connectAttr(f'{metallic_node}.outColor ', f'{range_node}.input')
        mc.connectAttr(f'{range_node}.outColor', f'{clamp_node}.input')
        mc.connectAttr(f'{clamp_node}.outColor', f'{color_to_float}.input')
        mc.connectAttr(f'{color_to_float}.outValue', f'{shading_node}.metalness')

        mc.setAttr(f'{metallic_node}.filename', f'{metallic_path}', type='string')
        mc.setAttr(f'{metallic_node}.ignoreColorSpaceFileRules', True)
        mc.setAttr(f'{metallic_node}.colorSpace', "Raw", type='string')
        mc.setAttr(f'{metallic_node}.autoTx', 0)
        if "1001" in texture_to_set:
            mc.setAttr(f'{metallic_node}.uvTilingMode', 3)

    return metallic_node


def create_normal(short_name, textures_path, texture_files, shading_node):
    """
    Creates and connects the normal texture to the shading node.

    Parameters:
        short_name (str): The short name for the asset.
        textures_path (str): The directory path where texture files are located.
        texture_files (list): List of texture file names.
        shading_node (str): The shading node to which the texture will be connected.

    Returns:
        str: The created normal texture node.
    """
    normal_files = []
    texture_to_set = ""
    normal_node = None

    for texture_file in texture_files:
        if "_normal" in texture_file and "mat_" in texture_file:
            normal_files.append(texture_file)
            if len(normal_files) == 1:
                texture_to_set = texture_file
            if len(normal_files) > 1:
                for normal_file in normal_files:
                    if "1001" in normal_file:
                        texture_to_set = normal_file

    if normal_files:
        normal_path = os.path.join(textures_path, texture_to_set).replace("\\", "/")
        normal_node = mc.shadingNode('aiImage', asTexture=True, name=f'img_normal_{short_name}')
        normal_param = mc.shadingNode('aiNormalMap', asUtility=True, name=f'normal_{short_name}')
        mc.connectAttr(f'{normal_node}.outColor ', f'{normal_param}.input')
        mc.connectAttr(f'{normal_param}.outValue', f'{shading_node}.normalCamera')

        mc.setAttr(f'{normal_node}.filename', f'{normal_path}', type='string')
        mc.setAttr(f'{normal_node}.ignoreColorSpaceFileRules', True)
        mc.setAttr(f'{normal_node}.colorSpace', "Raw", type='string')
        mc.setAttr(f'{normal_node}.autoTx', 0)
        if "1001" in texture_to_set:
            mc.setAttr(f'{normal_node}.uvTilingMode', 3)

    return normal_node


def create_scattering_mask(short_name, textures_path, texture_files, shading_node):
    """
    Creates and connects the scattering mask texture to the shading node.

    Parameters:
        short_name (str): The short name for the asset.
        textures_path (str): The directory path where texture files are located.
        texture_files (list): List of texture file names.
        shading_node (str): The shading node to which the texture will be connected.

    Returns:
        str: The created scattering mask texture node.
    """
    scatter_msk_files = []
    texture_to_set = ""
    scatter_msk_node = None

    for texture_file in texture_files:
        if "_scatteringMask" in texture_file and "mat_" in texture_file:
            scatter_msk_files.append(texture_file)
            if len(scatter_msk_files) == 1:
                texture_to_set = texture_file
            if len(scatter_msk_files) > 1:
                for scatter_msk_file in scatter_msk_files:
                    if "1001" in scatter_msk_file:
                        texture_to_set = scatter_msk_file

    if scatter_msk_files:
        scatter_msk_path = os.path.join(textures_path, texture_to_set).replace("\\", "/")
        scatter_msk_node = mc.shadingNode('aiImage', asTexture=True, name=f'img_scatter_msk_{short_name}')
        range_node = mc.shadingNode("aiRange", asUtility=True, name=f"range_scatter_msk_{short_name}")
        clamp_node = mc.shadingNode("aiClamp", asUtility=True, name=f"clamp_scatter_msk_{short_name}")
        color_to_float = mc.shadingNode("aiColorToFloat", asUtility=True, name="color_to_float_scatter_msk")
        mc.connectAttr(f'{scatter_msk_node}.outColor ', f'{range_node}.input')
        mc.connectAttr(f'{range_node}.outColor', f'{clamp_node}.input')
        mc.connectAttr(f'{clamp_node}.outColor', f'{color_to_float}.input')
        mc.connectAttr(f'{color_to_float}.outValue', f'{shading_node}.subsurface')

        mc.setAttr(f'{scatter_msk_node}.filename', f'{scatter_msk_path}', type='string')
        mc.setAttr(f'{scatter_msk_node}.ignoreColorSpaceFileRules', True)
        mc.setAttr(f'{scatter_msk_node}.colorSpace', "Raw", type='string')
        mc.setAttr(f'{scatter_msk_node}.autoTx', 0)
        if "1001" in texture_to_set:
            mc.setAttr(f'{scatter_msk_node}.uvTilingMode', 3)

    return scatter_msk_node


def connect_placed_texture(short_name, texture_nodes):
    """
    Creates and connects a placed texture node to the provided texture nodes.

    Parameters:
        short_name (str): The short name for the asset.
        texture_nodes (list): List of texture nodes to connect to the placed texture node.
    """
    attributes_output = ['outUV']
    attributes_input = ['uvcoords']

    place2d_name = f'place2dTexture_{short_name}'
    place2d_node = mc.shadingNode('place2dTexture', asUtility=True, name=f'{place2d_name}')

    for texture_node in texture_nodes:
        for att_output, att_input in zip(attributes_output, attributes_input):
            mc.connectAttr(f'{place2d_node}.{att_output}', f'{texture_node}.{att_input}')


def create_scattering_color(short_name, textures_path, texture_files, shading_node):
    """
    Creates and connects the scattering color texture to the shading node.

    Parameters:
        short_name (str): The short name for the asset.
        textures_path (str): The directory path where texture files are located.
        texture_files (list): List of texture file names.
        shading_node (str): The shading node to which the texture will be connected.

    Returns:
        str: The created scattering color texture node.
    """
    scattercolor_files = []
    texture_to_set = ""
    scattercolor_node = None

    for texture_file in texture_files:
        if "_scatteringColor" in texture_file and "mat_" in texture_file:
            scattercolor_files.append(texture_file)
            if len(scattercolor_files) == 1:
                texture_to_set = texture_file
            if len(scattercolor_files) > 1:
                for scattercolor_file in scattercolor_files:
                    if "1001" in scattercolor_file:
                        texture_to_set = scattercolor_file

    if scattercolor_files:
        scattercolor_path = os.path.join(textures_path, texture_to_set).replace("\\", "/")
        scattercolor_node = mc.shadingNode('aiImage', asTexture=True, name=f'img_scattercolor_{short_name}')
        color_correct_node = mc.shadingNode("aiColorCorrect", asUtility=True,
                                            name=f"colorCorrect_scattercolor_{short_name}")
        mc.connectAttr(f'{scattercolor_node}.outColor', f'{color_correct_node}.input')
        mc.connectAttr(f'{color_correct_node}.outColor', f'{shading_node}.subsurfaceColor')

        mc.setAttr(f'{scattercolor_node}.filename', f'{scattercolor_path}', type='string')
        mc.setAttr(f'{scattercolor_node}.ignoreColorSpaceFileRules', True)
        mc.setAttr(f'{scattercolor_node}.colorSpace', "sRGB", type='string')
        mc.setAttr(f'{scattercolor_node}.autoTx', 0)
        if "1001" in texture_to_set:
            mc.setAttr(f'{scattercolor_node}.uvTilingMode', 3)

    return scattercolor_node
