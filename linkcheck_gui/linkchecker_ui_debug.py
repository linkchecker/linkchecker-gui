# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/debug.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DebugDialog(object):
    def setupUi(self, DebugDialog):
        DebugDialog.setObjectName("DebugDialog")
        DebugDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DebugDialog.resize(564, 547)
        self.verticalLayout = QtWidgets.QVBoxLayout(DebugDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(DebugDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit = QtWidgets.QPlainTextEdit(self.frame)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText("")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(DebugDialog)
        QtCore.QMetaObject.connectSlotsByName(DebugDialog)

    def retranslateUi(self, DebugDialog):
        _translate = QtCore.QCoreApplication.translate
        DebugDialog.setWindowTitle(_translate("DebugDialog", "LinkChecker debug log"))
