import maya.cmds as mc
import maya.mel as mel
import ufe


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
    # TODO : long name = stack_shape_path ?
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


def rename_matx_document(short_name, matx_stack_shape, matx_import_name):
    """
    rename the matx document based on the asset name

    Parameters:
        short_name (str): short name of the asset. (example : nameA)
        matx_stack_shape (str) : name of the materialxStack shape. (example : matXStack_nameAShape)
        matx_import_name (str) : name of the document you want to rename

    Returns:
        renamed_document (str): new name of the document (example : doc_nameA

    """
    stack_shape_path = mel.eval('ls -l {}'.format(matx_stack_shape))[0]
    renamed_document = mc.rename(f"{stack_shape_path},%{matx_import_name}", f'doc_{short_name}')
    return renamed_document


# TEST    
# def assign_matx():
#     mc.select("hi_bolA")
#     mc.materialxAssign(edit=True, assign=True, sourcePath = "|matXStack_bolA|matXStack_bolAShape,%Magnolia_Curtain_Fabric%Magnolia_Curtain_Fabric")

# def set_attr_matx():
#     mc.setAttr("|matXStack_bolA|matXStack_bolAShape,%jojo%standard_surface1.base_color",0.8,0.6,0.4)

if __name__ == "__main__":
    # mc.file(new=True, force=True)
    # matx_import_name = "Magnolia_Curtain_Fabric"
    # matx_path=r'F:\projets\testPipeline\020_mod_surf\prp_bolA\publish\{}.mtlx'.format(matx_import_name)
    # matx_export_path =r"F:\projets\testPipeline\020_mod_surf\prp_bolA\publish\{}.mtlx".format(matx_import_name)
    # short_name="bolA"
    # matx_stack_shape=create_matx_stack_shape(short_name)
    # import_matx_document(matx_stack_shape,matx_path)
    # new_document_name=rename_matx_document(short_name, matx_stack_shape, matx_import_name)

    export_matx_document('|matXStack_bolA|matXStack_bolAShape,%doc_bolA', matx_export_path)
    docLongName = "|matXStack_bolA|matXStack_bolAShape,%document1"
    docItem = ufe.Hierarchy.createItem(ufe.PathString.path(docLongName))
    contextOps = ufe.ContextOps.contextOps(docItem)
    contextOps.doOp(['MxExportDocument', r"F:\projets\testPipeline\020_mod_surf\prp_bolA\publish\test.mtlx"])
