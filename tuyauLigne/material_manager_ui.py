try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtWidgets

try:
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2.QtCore import Qt

try:
    from shiboken6 import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

import sys

import maya.OpenMayaUI as omui

from tuyauLigne import material_manager as matm


class MaterialManagerLaunch:
    def __init__(self):
        self.parent = self.maya_main_window()

    def maya_main_window(self):
        main_window_ptr = omui.MQtUtil.mainWindow()

        if sys.version_info.major >= 3:
            try:
                return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
            except:
                return None
        else:
            return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def run(self):
        """  builds our UI
        """
        win = None

        if not win:
            win = MaterialManagerUi(parent=self.parent)

        if win.isHidden():
            win.show()
        else:
            win.raise_()
            win.activateWindow()

        win.show()
        return win


class MaterialManagerUi(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(MaterialManagerUi, self).__init__(parent)
        self.setWindowTitle('material manager')
        self.setFixedWidth(350)
        self.setFixedHeight(200)
        self.create_widgets()
        self.create_connections()
        # self.initial_state_ui()
        self.create_layout()

    def create_widgets(self):
        self.btn_proxy_mat = QtWidgets.QPushButton("assign mat to proxy")
        self.btn_render_mat = QtWidgets.QPushButton("assign mat to render")
        self.btn_proxy_txt = QtWidgets.QPushButton("assign texture to proxy")
        self.btn_render_txt = QtWidgets.QPushButton("assign texture to render")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout(self)

        grid_layout.addWidget(self.btn_proxy_mat, 0, 0)
        grid_layout.addWidget(self.btn_render_mat, 1, 0)
        grid_layout.addWidget(self.btn_proxy_txt, 2, 0)
        grid_layout.addWidget(self.btn_render_txt, 3, 0)

        # add grid_layout to a widget
        layout_widget = QtWidgets.QWidget()
        layout_widget.setLayout(grid_layout)

        main_layout.addWidget(layout_widget)

        self.setLayout(main_layout)

    def create_connections(self):
        self.btn_proxy_mat.clicked.connect(matm.assign_preview_mat)
        self.btn_render_mat.clicked.connect(matm.assign_tmp_mat)
        self.btn_proxy_txt.clicked.connect(matm.assign_preview_texture)
        self.btn_render_txt.clicked.connect(matm.assign_arnold_mat)
