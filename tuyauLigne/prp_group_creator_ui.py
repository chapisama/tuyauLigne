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

import string
import sys

import maya.OpenMayaUI as omui
import maya.cmds as mc
from tuyauLigne import outliner_manager as outm


class GroupCreatorLaunch:
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
            win = GroupCreatorUi(parent=self.parent)

        if win.isHidden():
            win.show()
        else:
            win.raise_()
            win.activateWindow()

        win.show()
        return win


class GroupCreatorUi(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(GroupCreatorUi, self).__init__(parent)
        self.setWindowTitle('"prp" group creator')
        self.setFixedWidth(350)
        self.setFixedHeight(60)
        self.create_widgets()
        self.create_connections()
        self.initial_state_ui()
        self.create_layout()

    def create_widgets(self):
        self.lbl_name = QtWidgets.QLabel("prp_name :")
        self.entry_name = QtWidgets.QLineEdit()
        self.combo_increment = QtWidgets.QComboBox()
        self.btn_create = QtWidgets.QPushButton("create")

        self.lbl_primitive = QtWidgets.QLabel("create primitive(s) :")
        self.chkbox_cube = QtWidgets.QCheckBox()
        self.lbl_cube = QtWidgets.QLabel("cube")
        self.chkbox_cylinder = QtWidgets.QCheckBox()
        self.lbl_cylinder = QtWidgets.QLabel("cylinder")
        self.chkbox_frame = QtWidgets.QCheckBox()
        self.lbl_frame = QtWidgets.QLabel("frame")

    def create_layout(self):
        # main boxes
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.vbox_main = QtWidgets.QVBoxLayout(self)
        self.hbox_entry = QtWidgets.QHBoxLayout(self)
        self.hbox_primitives = QtWidgets.QHBoxLayout(self)

        self.grid_layout.addLayout(self.vbox_main, 0, 0, 1, 1)
        self.vbox_main.addLayout(self.hbox_entry)
        self.vbox_main.addLayout(self.hbox_primitives)

        # add widgets
        self.hbox_entry.addWidget(self.lbl_name)
        self.hbox_entry.addWidget(self.entry_name)
        self.hbox_entry.addWidget(self.combo_increment)
        self.hbox_entry.addWidget(self.btn_create)

        self.hbox_primitives.addWidget(self.lbl_primitive)
        self.hbox_primitives.addWidget(self.chkbox_cube)
        self.hbox_primitives.addWidget(self.lbl_cube)
        self.hbox_primitives.addWidget(self.chkbox_cylinder)
        self.hbox_primitives.addWidget(self.lbl_cylinder)
        self.hbox_primitives.addWidget(self.chkbox_frame)
        self.hbox_primitives.addWidget(self.lbl_frame)

        self.hbox_primitives.addStretch()

    def create_connections(self):
        self.btn_create.clicked.connect(self.create_prp_groups)

    def initial_state_ui(self):
        self.chkbox_cube.setChecked(True)
        increments = list(string.ascii_uppercase)
        self.combo_increment.addItems(increments)

    def get_entry_name(self):
        """
        Get the name specified by the user.

        Returns:
            str: The name specified by the user with the alphabetical increment at the end of the name.
        """
        name = self.entry_name.text()
        increment = self.combo_increment.currentText()
        short_name = name + increment
        return short_name

    def create_default_cube(self):
        """
        Create a cube primitive with default name and default position at 0,0,0.

        Returns:
            str: Name of the primitive.
        """
        default_cube = mc.polyCube(name="lo_cube")
        mc.select(default_cube)
        mc.move(0, 0.5, 0)
        mc.select(d=True)
        mc.xform(default_cube, piv=[0, 0, 0], worldSpace=True)
        mc.makeIdentity(default_cube, apply=True)
        return default_cube

    def create_default_cylinder(self):
        """
        Create a cylinder primitive with default name and default position at 0,0,0.

        Returns:
            str: Name of the primitive.
        """
        default_cylinder = mc.polyCylinder(name="lo_cylinder")
        mc.select(default_cylinder)
        mc.move(0, 1, 0)
        mc.select(d=True)
        mc.xform(default_cylinder, piv=[0, 0, 0], worldSpace=True)
        mc.makeIdentity(default_cylinder, apply=True)
        return default_cylinder

    def create_frame(self):
        """
        Create a frame primitive with default name and default position at 0,0,0.

        Returns:
            str: Name of the primitive.
        """
        default_frame = mc.polyPlane(name="lo_frame", subdivisionsHeight=1, subdivisionsWidth=1)
        mc.select(d=True)
        edges_to_select = [f"{default_frame[0]}.e[{i}]" for i in range(4)]
        mc.polyExtrudeEdge(edges_to_select, offset=0.1)
        face_to_delete = f"{default_frame[0]}.f[0]"
        mc.delete(face_to_delete)
        mc.polyExtrudeFacet(default_frame[0], thickness=0.1)
        mc.select(default_frame, replace=True)
        mc.delete(default_frame, ch=True)
        mc.rotate(90, 0, 0)
        mc.move(0, 0.6, -0.05)
        mc.xform(default_frame[0], piv=[0, 0, 0], worldSpace=True)
        mc.makeIdentity(default_frame[0], apply=True)
        return default_frame

    def create_prp_groups(self):
        """
        Create the prp_group inside the Maya scene, with the name given by the user. Add primitives if selected by the 
        user.
        """
        name = self.get_entry_name()
        master_grp = outm.get_master_grp_name()
        if not self.entry_name.text():
            mc.confirmDialog(message="no name specified", button="ok")
        elif not mc.objExists(master_grp):
            mc.confirmDialog(message=f"no group '{master_grp}' found", button="ok")
        elif mc.objExists(f"prp_{name}"):
            mc.confirmDialog(message=f"prp_{name} already exists", button="ok")
        else:
            prp_group = mc.group(name=f"prp_{name}", empty=True)
            proxy_group = mc.group(name=f"proxy_{name}", empty=True)
            mc.parent(proxy_group, prp_group)
            if self.chkbox_cube.isChecked():
                default_cube = self.create_default_cube()
                mc.parent(default_cube[0], proxy_group)
            if self.chkbox_cylinder.isChecked():
                default_cylinder = self.create_default_cylinder()
                mc.parent(default_cylinder[0], proxy_group)
            if self.chkbox_frame.isChecked():
                default_frame = self.create_frame()
                mc.parent(default_frame[0], proxy_group)
            mc.parent(prp_group, master_grp)
