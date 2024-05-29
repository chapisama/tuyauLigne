import maya.cmds as mc
import maya.mel as mel

from tuyauLigne import naming_convention as naco


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


def delete_unused_shaders():
    """
    Deletes unused shaders in the Maya scene.
    """
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
