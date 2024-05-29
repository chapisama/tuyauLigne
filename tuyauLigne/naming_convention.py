import maya.cmds as mc

"""
GLOSSARY :
A

asset : design all main files composing the project. It can be a prop file, a proxy file, variant file, ...

asset name : is composed of the type and the short asset name. Example : prp_jarA

asset short name : the name describing the asset. Example : jarA

asset type : specific asset. Example : prp, prx, var, ...

E

element : design all the elements inside the outliner

F

file name :  name of the maya file with this structure : prp_jarA_001.ma
            prp : asset type
            prp_jarA : asset name
            jarA : asset short name
            001: inc number
            ma : file type    
"""


def get_file_name():
    """
    Gets the short name of the file currently open in Maya.
    """
    file_name = mc.file(q=True, sceneName=True, shortName=True)
    return file_name


def dict_file_name_part(file_name):
    """
    Stores all the components of the asset name, given the file name.

    Parameters:
        file_name (str): Name of the file.
            Example: prp_jarA_001.ma
            prp: asset type
            prp_jarA: asset_name
            jarA: short name
            001: inc number
            ma: file_type

    Returns:
        dict: All components of the file name.
    """
    dict_file_name = {
        "asset_type": file_name.split("_")[0],
        "asset_name": file_name.split("_")[0] + "_" + file_name.split("_")[1],
        "asset_short_name": file_name.split("_")[1],
        "inc_number": int("{:03d}".format(int(file_name.split("_")[2].split(".")[0]))),
        "file_type": file_name.split(".")[-1],
    }
    return dict_file_name


def dict_element_name_part(element_name):
    """
    Stores all the components of an element name.

    Parameters:
        element_name (str): Name of the element.
            Example: grp_jarA
            element_type: grp
            element_name: grp_jarA
            element short name: jarA

    Returns:
        dict: All components of the element name.
    """
    dict_element_name = {
        "element_type": element_name.split("_")[0],
        "element_name": element_name.split("_")[0] + "_" + element_name.split("_")[1],
        "element_short_name": element_name.split("_")[1]
    }
    return dict_element_name
