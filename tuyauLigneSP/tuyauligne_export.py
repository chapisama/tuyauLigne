import substance_painter.export
import substance_painter.project
import substance_painter.resource
import substance_painter.textureset
from PySide2 import QtWidgets

from tuyauLigneSP import project_manager as pm


def get_mat_sets_list():
    mat_sets = []
    texture_sets_id = substance_painter.textureset.all_texture_sets()
    for texture_set in texture_sets_id:
        set_name = texture_set.name()
        if "mat_" in set_name:
            mat_sets.append(set_name)

    return mat_sets


def get_usdprev_sets_list():
    usdprev_sets = []
    texture_sets_id = substance_painter.textureset.all_texture_sets()
    for texture_set in texture_sets_id:
        set_name = texture_set.name()
        if "usdPrev_" in set_name:
            usdprev_sets.append(set_name)

    return usdprev_sets


def dict_export_list(texture_sets):
    export_list = {
        "exportList": []
    }
    for texture_set in texture_sets:
        export_list["exportList"].append({"rootPath": texture_set})

    return export_list


def set_resolution(combo_resolution):
    resolution = combo_resolution.currentText()
    size_log = 10
    if resolution == "512":
        size_log = 9
    elif resolution == "1024":
        size_log = 10
    elif resolution == "2048":
        size_log = 11
    elif resolution == "4096":
        size_log = 12
    elif resolution == "8192":
        size_log = 13
    return size_log


def export_textures(combo_resolution):
    export_directory = pm.get_textures_folder()
    if not isinstance(export_directory, str):
        print("Error: export_directory is not a string.")
        return
    mat_sets = get_mat_sets_list()
    export_mat_list = dict_export_list(mat_sets)
    usdprev_sets = get_usdprev_sets_list()
    export_usdprev_list = dict_export_list(usdprev_sets)
    size_log = set_resolution(combo_resolution)

    export_mat_config = {"exportPath": export_directory,
                         "exportShaderParams": False,
                         "defaultExportPreset": "tuyauligne_preset",
                         "exportPresets": [
                             {
                                 "name": "tuyauligne_preset",
                                 "maps": [
                                     {
                                         "fileName": "$textureSet_baseColor(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "R",
                                                 "srcChannel": "R",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "basecolor"
                                             },
                                             {
                                                 "destChannel": "G",
                                                 "srcChannel": "G",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "basecolor"
                                             },
                                             {
                                                 "destChannel": "B",
                                                 "srcChannel": "B",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "basecolor"
                                             },
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "16",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                     {
                                         "fileName": "$textureSet_roughness(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "L",
                                                 "srcChannel": "L",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "roughness"
                                             }
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "8",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                     {
                                         "fileName": "$textureSet_metallic(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "L",
                                                 "srcChannel": "L",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "metallic"
                                             }
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "8",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                     {
                                         "fileName": "$textureSet_normal(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "R",
                                                 "srcChannel": "R",
                                                 "srcMapType": "virtualMap",
                                                 "srcMapName": "Normal_OpenGL"
                                             },
                                             {
                                                 "destChannel": "G",
                                                 "srcChannel": "G",
                                                 "srcMapType": "virtualMap",
                                                 "srcMapName": "Normal_OpenGL"
                                             },
                                             {
                                                 "destChannel": "B",
                                                 "srcChannel": "B",
                                                 "srcMapType": "virtualMap",
                                                 "srcMapName": "Normal_OpenGL"
                                             },
                                             {
                                                 "destChannel": "A",
                                                 "srcChannel": "A",
                                                 "srcMapType": "virtualMap",
                                                 "srcMapName": "Normal_OpenGL"
                                             },
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "16",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                     {
                                         "fileName": "$textureSet_height(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "L",
                                                 "srcChannel": "L",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "height"
                                             }
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "16",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                     {
                                         "fileName": "$textureSet_emissive(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "R",
                                                 "srcChannel": "R",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "emissive"
                                             },
                                             {
                                                 "destChannel": "G",
                                                 "srcChannel": "G",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "emissive"
                                             },
                                             {
                                                 "destChannel": "B",
                                                 "srcChannel": "B",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "emissive"
                                             },
                                             {
                                                 "destChannel": "A",
                                                 "srcChannel": "A",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "emissive"
                                             }
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "8",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                     {
                                         "fileName": "$textureSet_scatteringMask(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "L",
                                                 "srcChannel": "L",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "scattering"
                                             }
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "8",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                     {
                                         "fileName": "$textureSet_scatteringColor(_$udim)",
                                         "channels": [
                                             {
                                                 "destChannel": "R",
                                                 "srcChannel": "R",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "scatteringcolor"
                                             },
                                             {
                                                 "destChannel": "G",
                                                 "srcChannel": "G",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "scatteringcolor"
                                             },
                                             {
                                                 "destChannel": "B",
                                                 "srcChannel": "B",
                                                 "srcMapType": "documentMap",
                                                 "srcMapName": "scatteringcolor"
                                             },
                                         ],
                                         "parameters": {
                                             "fileFormat": "png",
                                             "bitDepth": "16",
                                             "dithering": False,
                                             "sizeLog2": size_log,
                                             "paddingAlgorithm": "diffusion",
                                             "dilationDistance": 16
                                         }
                                     },
                                 ]
                             }
                         ],
                         "exportList": export_mat_list["exportList"]}
    export_usdprev_config = {"exportPath": export_directory,
                             "exportShaderParams": False,
                             "defaultExportPreset": "usdprev_preset",
                             "exportPresets": [
                                 {
                                     "name": "usdprev_preset",
                                     "maps": [
                                         {
                                             "fileName": "$textureSet_baseColor",
                                             "channels": [
                                                 {
                                                     "destChannel": "R",
                                                     "srcChannel": "R",
                                                     "srcMapType": "documentMap",
                                                     "srcMapName": "basecolor"
                                                 },
                                                 {
                                                     "destChannel": "G",
                                                     "srcChannel": "G",
                                                     "srcMapType": "documentMap",
                                                     "srcMapName": "basecolor"
                                                 },
                                                 {
                                                     "destChannel": "B",
                                                     "srcChannel": "B",
                                                     "srcMapType": "documentMap",
                                                     "srcMapName": "basecolor"
                                                 },
                                             ],
                                             "parameters": {
                                                 "fileFormat": "png",
                                                 "bitDepth": "8",
                                                 "dithering": False,
                                                 "sizeLog2": 9,
                                                 "paddingAlgorithm": "diffusion",
                                                 "dilationDistance": 16
                                             }
                                         }
                                     ]
                                 }
                             ],
                             "exportList": export_usdprev_list["exportList"]}

    # Perform the actual export
    export_mat_result = substance_painter.export.export_project_textures(export_mat_config)
    export_usdprev_result = substance_painter.export.export_project_textures(export_usdprev_config)

    # Check for errors and display messages
    if export_mat_result.status != substance_painter.export.ExportStatus.Success:
        print(export_mat_result.message)
    if export_usdprev_result.status != substance_painter.export.ExportStatus.Success:
        print(export_usdprev_result.message)

    # Display the details of what was exported
    for k, v in export_mat_result.textures.items():
        print(f"Stack {k}:")
        for texture in v:
            print(texture)
    for k, v in export_usdprev_result.textures.items():
        print(f"Stack {k}:")
        for texture in v:
            print(texture)

    pm.rename_textures()


def create_ui():
    """
    Returns:
        QWidget: The main widget containing the plugin's UI.
    """
    resolutions = ["512", "1024", "2048", "4096", "8192"]
    # Create the main widgets
    export_widget = QtWidgets.QWidget()
    export_layout = QtWidgets.QVBoxLayout(export_widget)
    export_widget.setWindowTitle("Tuyau Ligne Export ")

    # Creates the boxes
    hbox_export = QtWidgets.QHBoxLayout()

    # Creates the widgets
    combo_resolution = QtWidgets.QComboBox()
    btn_export = QtWidgets.QPushButton("Export")

    # add the widgets to the boxes
    hbox_export.addWidget(combo_resolution)
    hbox_export.addWidget(btn_export)

    # add the boxes to the main box
    export_layout.addLayout(hbox_export)

    # sets initial states
    combo_resolution.addItems(resolutions)
    # creates connexions
    btn_export.clicked.connect(lambda: export_textures(combo_resolution))

    return export_widget
