# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/editor.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorDialog(object):
    def setupUi(self, EditorDialog):
        EditorDialog.setObjectName("EditorDialog")
        EditorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        EditorDialog.resize(640, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditorDialog.sizePolicy().hasHeightForWidth())
        EditorDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditorDialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.menubar = QtWidgets.QMenuBar(EditorDialog)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.verticalLayout.addWidget(self.menubar)
        self.frame = QtWidgets.QFrame(EditorDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.actionSave = QtWidgets.QAction(EditorDialog)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(EditorDialog)
        QtCore.QMetaObject.connectSlotsByName(EditorDialog)

    def retranslateUi(self, EditorDialog):
        _translate = QtCore.QCoreApplication.translate
        EditorDialog.setWindowTitle(_translate("EditorDialog", "LinkChecker source view"))
        self.menuFile.setTitle(_translate("EditorDialog", "&File"))
        self.actionSave.setText(_translate("EditorDialog", "&Save"))
        self.actionSave.setShortcut(_translate("EditorDialog", "Ctrl+S"))
