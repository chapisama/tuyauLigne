import os
import shutil

import maya.cmds as mc
import maya.mel as mel
import ufe


def duplicate_matx_template(textures_folder, short_name):
    """
    Duplicates a MaterialX template file and renames it based on the asset short name.

    Parameters:
        textures_folder (str): The folder where the textures are stored.
        short_name (str): The short name of the asset.

    Returns:
        tuple: Contains the path to the duplicated MaterialX file and the document name.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'matx_template', 'template.mtlx')
    if not os.path.isfile(template_path):
        print(f"file 'template.matx' not found at {template_path}")
        return
    doc_name = f'doc_{short_name}'
    file_name = f"{doc_name}.mtlx"
    destination_path = os.path.join(textures_folder, file_name)
    shutil.copyfile(template_path, destination_path)
    return destination_path, doc_name


def create_matx_stack_shape(short_name):
    """
    create a materialXStack, name based on the asset name

    Parameters:
        short_name (str): short name of the asset. (example : nameA)

    Returns:
        matx_stack_shape (str) : name of the materialxStack shape. (example : matXStack_nameAShape)
    """
    matx_stack_name = f"matXStack_{short_name}Shape"
    matx_stack_shape = mc.createNode("materialxStack", name=matx_stack_name)

    return matx_stack_shape


def import_matx_document(matx_stack_shape, matx_path):
    """
    import a .matx document and parent it to a specified stack

    Parameters:
        matx_stack_shape (str): name of the materialxStack shape.
        matx_path (str) : file path to the .matx document.
    """
    stack_shape_path = mel.eval('ls -l {}'.format(matx_stack_shape))[0]
    stack_shape_item = ufe.Hierarchy.createItem(ufe.PathString.path(stack_shape_path))
    context_ops = ufe.ContextOps.contextOps(stack_shape_item)
    context_ops.doOp(['MxImportDocument', matx_path])


def export_matx_document(matx_stack_shape, matx_path):
    # TODO : not working. Waiting for a solution on the forum
    # stack_shape_path = mel.eval('ls -l {}'.format(matx_stack_shape))[0]
    stack_shape_item = ufe.Hierarchy.createItem(ufe.PathString.path(matx_stack_shape))
    context_ops = ufe.ContextOps.contextOps(stack_shape_item)
    context_ops.doOp(['MxExportDocument', matx_path])


def rename_main_nodes(short_name, matx_stack_shape, doc_name):
    """
    rename the matx document based on the asset name

    Parameters:
        short_name (str): short name of the asset. (example : nameA)
        matx_stack_shape (str) : name of the materialxStack shape. (example : matXStack_nameAShape)
        doc_name (str) : name of the document you want to rename

    Returns:
        renamed_document (str): new name of the document (example : doc_nameA)

    """

    stack_shape_path = mel.eval('ls -l {}'.format(matx_stack_shape))[0]
    doc_name = f"{stack_shape_path},%{doc_name}"
    shader_name = mc.rename(f"{doc_name}%matx_template", f'matx_{short_name}')
    shader_sg_name = mc.rename(f"{doc_name}%matx_templateSG", f'matx_{short_name}SG')
    compound_name = mc.rename(f"{doc_name}%compound_template", f'compound_{short_name}')
    return shader_sg_name, compound_name


def assign_matx(shader_name):
    """
    Assigns a MaterialX shader to all meshes inside the render group.

    Parameters:
        shader_name (str): The name of the MaterialX shader to assign.
    """
    meshes = mc.listRelatives("render_*", allDescendents=True, fullPath=True, type="mesh")
    for mesh in meshes:
        mc.materialxAssign(edit=True, assign=True, sourcePath=shader_name)


def set_texture_path(compound_name, texture_path, texture_files, texture_types):
    """
    Sets the texture file paths for the specified compound node.

    Parameters:
        compound_name (str): The name of the compound node.
        texture_path (str): The path to the texture files.
        texture_files (list): A list of texture file names.
        texture_types (list): A list of texture types.
    """
    for texture_type in texture_types:
        for file in texture_files:
            if "mat_" in file and texture_type in file:
                file_path = os.path.join(texture_path, file).replace("\\", "/")
                mc.setAttr(f"{compound_name}%img_{texture_type}.file", file_path)


def set_color_space(compound_name):
    """
    Sets the color space for specific texture attributes in the compound node.

    Parameters:
        compound_name (str): The name of the compound node.
    """
    mc.setAttr(f"{compound_name}%img_roughness.colorSpace", "Raw")
    mc.setAttr(f"{compound_name}%img_metallic.colorSpace", "Raw")
    mc.setAttr(f"{compound_name}%img_normal.colorSpace", "Raw")
    mc.setAttr(f"{compound_name}%img_scatteringMask.colorSpace", "Raw")
