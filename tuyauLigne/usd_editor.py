import os

import maya.cmds as mc
from pxr import Usd, Sdf, UsdGeom, UsdUtils, UsdShade

from tuyauLigne import material_manager as matm
from tuyauLigne import project_manager as pm

"""
part of this code is from here (repath_properties and move_prim_spec): 
https://gist.github.com/BigRoy/44250f5d9fdba79d127ce96e88bcc197
By Roy Nieterau 

Glossary :
    Path : Prims and properties are identified by unique paths inside the scene hierarchy. They are a textual 
    representation of a hierarchy - similar to folder paths in most operating systems - where each prim is separated 
    from its parent or child via the / delimiter.

    Prims : Prims are the nodes within a hierarchy and can thus have parent/child relationships with other prims; 
    meaning that prims can have other prims as children or siblings, or have another prim as a parent.

    Purpose : Purpose is an attribute that can be used to give a prim and its descendants a high-level "visibility flag" 
    in context of rendering.
    For example, if a prim has its purpose attribute set to render, it will be excluded from being drawn in a 
    renderer that only wants to draw proxy prims.
"""


def get_prim_proxy_path(asset_name):
    """
    Get the path of the proxy prim (the proxy group inside Maya).

    Parameters:
        asset_name (str): Name of the asset selected.

    Returns:
        prim_proxy_path (str): Usd path of the proxy's group asset.
    """
    short_name = asset_name.split("_")[1]
    prim_proxy_path = f"/{asset_name}/proxy_{short_name}"
    return prim_proxy_path


def get_prim_render_path(asset_name):
    """
    Get the path of the render prim (the render group inside Maya).

    Parameters:
        asset_name (str): Name of the asset selected.

    Returns:
        prim_render_path (str): Usd path of the render's group asset.
    """
    no_prefix_name = asset_name.split("_")[1]
    prim_render_path = f"/{asset_name}/render_{no_prefix_name}"
    return prim_render_path


def set_purpose_proxy(file_path, asset_name):
    """
    Set the purpose of the prim proxy to proxy.

    Parameters:
        file_path (str): Path of the USD file.
        asset_name (str): Name of the asset.
    """
    stage = Usd.Stage.Open(file_path)
    prim_proxy_path = get_prim_proxy_path(asset_name)
    proxy_prim = stage.GetPrimAtPath(prim_proxy_path)
    if proxy_prim:
        purpose_attr = proxy_prim.GetAttribute("purpose")
        if not purpose_attr:
            purpose_attr = proxy_prim.CreateAttribute("purpose", Sdf.ValueTypeNames.Token)
        purpose_attr.Set(UsdGeom.Tokens.proxy)
    stage.GetRootLayer().Save()


def set_purpose_render(file_path, asset_name):
    """
    Set the purpose of the prim render to render.

    Parameters:
        file_path (str): Path of the USD file.
        asset_name (str): Name of the asset.
    """
    stage = Usd.Stage.Open(file_path)
    prim_render_path = get_prim_render_path(asset_name)
    render_prim = stage.GetPrimAtPath(prim_render_path)
    if render_prim:
        purpose_attr = render_prim.GetAttribute("purpose")
        if not purpose_attr:
            purpose_attr = render_prim.CreateAttribute("purpose", Sdf.ValueTypeNames.Token)
        purpose_attr.Set(UsdGeom.Tokens.render)
    stage.GetRootLayer().Save()


def repath_properties(layer, old_path, new_path):
    """Re-path property relationship targets and attribute connections.
    This will replace any relationship or connections from old path
    to new path by replacing start of any path that matches the new path.
    Parameters:
        layer (Sdf.Layer): Layer to move prim spec path.
        old_path (Union[Sdf.Path, str]): Source path to move from.
        new_path (Union[Sdf.Path, str]): Destination path to move to.
    Returns:
        bool: Whether any re-pathing occurred for the given paths.
    """

    old_path_str = str(old_path)
    peformed_repath = False

    def replace_in_list(spec_list):
        """Replace paths in SdfTargetProxy or SdfConnectionsProxy"""
        list_attrs = ['addedItems', 'appendedItems', 'deletedItems', 'explicitItems',
                      'orderedItems', 'prependedItems']
        for attr in list_attrs:
            entries = getattr(spec_list, attr)
            for i, entry in enumerate(entries):
                entry_str = str(entry)
                if entry == old_path or entry_str.startswith(
                        old_path_str + "/"):
                    # Repath
                    entries[i] = Sdf.Path(
                        str(new_path) + entry_str[len(old_path_str):])
                    peformed_repath = True

    def repath(path):
        spec = layer.GetObjectAtPath(path)
        if isinstance(spec, Sdf.RelationshipSpec):
            replace_in_list(spec.targetPathList)
        if isinstance(spec, Sdf.AttributeSpec):
            replace_in_list(spec.connectionPathList)

    # Repath any relationship pointing to this src prim path
    layer.Traverse("/", repath)

    return peformed_repath


def move_prim_spec(layer, src_prim_path, dest_prim_path):
    """Move a PrimSpec and repath connections.
    Note that the parent path of the destination must
    exist, otherwise the namespace edit to that path
    will fail.
    Parameters:
        layer (Sdf.Layer): Layer to move prim spec path.
        src_prim_path (Union[Sdf.Path, str]): Source path to move from.
        dest_prim_path (Union[Sdf.Path, str]): Destination path to move to.
    Returns:
        bool: Whether the move was successful
    """

    src_prim_path = Sdf.Path(src_prim_path)
    dest_prim_path = Sdf.Path(dest_prim_path)
    dest_parent = dest_prim_path.GetParentPath()
    dest_name = dest_prim_path.name
    layer.GetPrimAtPath(dest_prim_path)

    with Sdf.ChangeBlock():
        reparent_edit = Sdf.NamespaceEdit.ReparentAndRename(
            src_prim_path,
            dest_parent,
            dest_name,
            -1
        )

        edit = Sdf.BatchNamespaceEdit()
        edit.Add(reparent_edit)
        if not layer.Apply(edit) and layer.GetPrimAtPath(src_prim_path):
            print("Failed prim spec move")
            return False

        repath_properties(layer, src_prim_path, dest_prim_path)

    return True


def rename_mtl_scope(asset_name):
    """
    Renames the default material scope created by Maya to include the asset name.

    Parameters:
        asset_name (str): Name of the asset to rename the material scope for.
    """
    wip_usd_folder = pm.get_wip_usd_folder(asset_name)
    short_name = asset_name.split("_")[1]
    usd_file_name = "modeling_" + asset_name.split("_")[1]
    usd_file_path = wip_usd_folder + "/" + usd_file_name + ".usd"

    layer = Sdf.Layer.FindOrOpen(usd_file_path)

    src_prim_path = f"/{asset_name}/mtl"
    dest_prim_path = f"/{asset_name}/mtl_{short_name}"

    move_prim_spec(layer, src_prim_path, dest_prim_path)

    layer.Save()


def edit_prim_xform(usd_path, prim_name, transforms):
    """
    Modifies the transformation (translation, rotation, and scale) of a USD primitive.

    Parameters:
        usd_path (str): Path to the USD file containing the primitive.
        prim_name (str): Name of the primitive to modify.
        transforms (dict): Dictionary containing translation, rotation, and scale values.
    """
    stage = Usd.Stage.Open(usd_path)
    prim_path = stage.GetPrimAtPath(f"/{prim_name}")
    tx = transforms.get("tx")
    ty = transforms.get("ty")
    tz = transforms.get("tz")
    rx = transforms.get("rx")
    ry = transforms.get("ry")
    rz = transforms.get("rz")
    sx = transforms.get("sx")
    sy = transforms.get("sy")
    sz = transforms.get("sz")
    if (tx, ty, tz) != (0, 0, 0):
        UsdGeom.XformCommonAPI(prim_path).SetTranslate((tx, ty, tz))
    if (rx, ry, rz) != (0, 0, 0):
        UsdGeom.XformCommonAPI(prim_path).SetRotate((rx, ry, rz))
    if (sx, sy, sz) != (1, 1, 1):
        UsdGeom.XformCommonAPI(prim_path).SetScale((sx, sy, sz))
    stage.GetRootLayer().Save()


def create_mod_sublayer_usd(asset_name):
    """
    Create the USD sublayer for the modeling department of the asset.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
        usd_mod_path (str): Path of the USD modeling file.
    """
    extension_usd = "usda"
    mc.select(asset_name, r=True)
    wip_usd_folder = pm.get_wip_usd_folder(asset_name)
    usd_file_name = "modeling_" + asset_name.split("_")[1]
    usd_mod_path = wip_usd_folder + "/" + usd_file_name + ".usd"
    if not matm.check_arnold_connection():
        print("gogo sans arnold")
        mc.file(usd_mod_path.split(".")[0],
                options=f";exportColorSets=0;mergeTransformAndShape=1;exportComponentTags=0;"
                        f"defaultUSDFormat={extension_usd}",
                typ="USD Export", pr=True, ch=True, chn=True, exportSelected=True, f=True)
    else:
        print("gogo avec arnold")
        mc.file(usd_mod_path.split(".")[0],
                options=f";exportColorSets=0;mergeTransformAndShape=1;exportComponentTags=0;"
                        f"defaultUSDFormat={extension_usd};jobContext=[Arnold];convertMaterialsTo=[UsdPreviewSurface];"
                        f"defaultMeshScheme=catmullClark;exportRelativeTextures=relative",
                typ="USD Export", pr=True, ch=True, chn=True, exportSelected=True, f=True)
    mc.select(d=True)
    set_purpose_proxy(usd_mod_path, asset_name)
    set_purpose_render(usd_mod_path, asset_name)

    return usd_mod_path


def create_surf_sublayer_usd(asset_name):
    """
    Create the USD sublayer for the surfacing department of the asset.

    Parameters:
        asset_name (str): Name of the asset.

    Returns:
        usd_surf_path (str): Path of the USD surfacing file.
    """
    extension_usd = "usda"
    wip_usd_folder = pm.get_wip_usd_folder(asset_name)
    usd_file_name = "surfacing_" + asset_name.split("_")[1]
    usd_surf_path = wip_usd_folder + "/" + usd_file_name + "." + extension_usd
    surfacing_usd = Sdf.Layer.CreateNew(usd_surf_path)

    return usd_surf_path


def create_stage_usd(asset_name, usd_mod_path, usd_surf_path):
    """
    Create the USD stage layer of the asset and sublayering of the USD modeling file and USD surfacing file.

    Parameters:
        asset_name (str): Name of the asset.
        usd_mod_path (str): Path of the USD modeling file.
        usd_surf_path (str): Path of the USD surfacing file.

    Returns:
        usd_file_path (str) path of the stage usd
    """
    extension_usd = ".usda"
    wip_usd_folder = pm.get_wip_usd_folder(asset_name)
    asset_type = asset_name.split("_")[0]
    usd_file_name = asset_type + "_" + asset_name.split("_")[1]
    usd_file_path = wip_usd_folder + "/" + usd_file_name + extension_usd
    mod_relative_path = os.path.relpath(usd_mod_path, usd_file_path).replace("..\\", "./")
    surf_relative_path = os.path.relpath(usd_surf_path, usd_file_path).replace("..\\", "./")
    stage_usd = Usd.Stage.CreateNew(usd_file_path)
    stage_usd.GetRootLayer().subLayerPaths.append(surf_relative_path)
    stage_usd.GetRootLayer().subLayerPaths.append(mod_relative_path)
    stage_usd.GetRootLayer().Save()

    return usd_file_path


def create_set_usd(set_name, usd_layout_path, usd_assembly_path):
    """
    Create the USD stage layer of the set and sublayering of the USD layout file and USD assembly file.

    Parameters:
        set_name (str): Name of the asset.
        usd_layout_path (str): Path of the USD layout file.
        usd_assembly_path (str): Path of the USD assembly file.

    Returns:
        usd_file_path (str) path of the set usd
    """
    extension_usd = ".usda"
    usd_file_path = pm.get_wip_usd_set_folder(set_name) + "/" + set_name + extension_usd
    assembly_relative_path = os.path.relpath(usd_assembly_path, usd_file_path).replace("..\\", "./")
    layout_relative_path = os.path.relpath(usd_layout_path, usd_file_path).replace("..\\", "./")
    stage_usd = Usd.Stage.CreateNew(usd_file_path)
    stage_usd.GetRootLayer().subLayerPaths.append(layout_relative_path)
    stage_usd.GetRootLayer().subLayerPaths.append(assembly_relative_path)
    stage_usd.GetRootLayer().Save()

    return usd_file_path


def create_assembly_set_usd(set_name):
    """
    Create the USD assembly sublayer.

    Parameters:
        set_name (str): Name of the asset.

    Returns:
        usd_assembly_path (str): Path of the USD assembly file.
    """
    extension_usd = ".usda"
    assembly_name = set_name.replace("set_", "assembly_")
    usd_assembly_path = pm.get_wip_usd_set_folder(set_name) + "/" + assembly_name + extension_usd
    set_usd = Usd.Stage.CreateNew(usd_assembly_path)

    return usd_assembly_path


def create_layout_set_usd(set_name):
    """
    Create the USD layout sublayer.

    Parameters:
        set_name (str): Name of the asset.

    Returns:
        usd_layout_path (str): Path of the USD layout file.
    """
    extension_usd = ".usda"
    layout_name = set_name.replace("set_", "lay_")
    usd_layout_path = pm.get_wip_usd_set_folder(set_name) + "/" + layout_name + extension_usd
    set_usd = Usd.Stage.CreateNew(usd_layout_path)

    return usd_layout_path


def create_prp_layer(asset_name, usd_file_path):
    """
    Create the USD layer of the prop inside the USD layer Editor of Maya.

    Parameters:
        asset_name (str): Name of the asset.
        usd_file_path (str): Path of the USD file.
    """
    shape_node = mc.createNode("mayaUsdProxyShape", skipSelect=True, name=asset_name + "Shape")
    mc.setAttr(shape_node + ".filePath", usd_file_path, type="string")


def add_usd_reference(asset_name, file_path, ref_path):
    """
    Adds a reference to a USD layer.

    Parameters:
        asset_name (str): Name of the asset to reference in the USD layer.
        file_path (str): Path to the USD file where the reference should be added.
        ref_path (str): Path to the USD file to be referenced.
    """
    stage = Usd.Stage.Open(file_path)
    prim_path = Sdf.Path(f"/{asset_name}")
    reference_prim = stage.OverridePrim(prim_path)
    reference_prim.GetReferences().AddReference(ref_path)
    stage.GetRootLayer().Save()


def flattening_usd_files(usd_path, target_path):
    """
    Flattens a USD layer and its sublayers into a single USD file.

    Parameters:
        usd_path (str): Path to the main USD file to be flattened.
        target_path (str): Path to save the flattened USD file.
    """
    stage = Usd.Stage.Open(usd_path)
    flattened_stage = UsdUtils.FlattenLayerStack(stage)
    flattened_stage.Export(target_path)


if __name__ == "__main__":
    usd_path = "F:/testScript/exampleB/020_mod_surf/prp_bolA/wip/usd/modeling_bolA.usd"
    mtlx_file_path = "./doc_bolA.mtlx"
    stage = Usd.Stage.Open(usd_path)
    # prim_path = stage.GetPrimAtPath(f"/{prim_name}")

    material_prim_path = "/prp_bolA/mtl_bolA"
    material_prim = stage.GetPrimAtPath(material_prim_path)
    usd_material = UsdShade.Material(material_prim)
    material_prim.GetReferences().AddReference(Sdf.Reference(mtlx_file_path))
    stage.GetRootLayer().Save()
