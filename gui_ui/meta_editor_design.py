# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meta_editor_design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(363, 529)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.inputButton = QtGui.QPushButton(self.centralwidget)
        self.inputButton.setGeometry(QtCore.QRect(20, 10, 330, 32))
        self.inputButton.setObjectName(_fromUtf8("inputButton"))
        self.exitButton = QtGui.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(20, 490, 330, 32))
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(20, 50, 327, 436))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.inputlistWidget = QtGui.QListWidget(self.splitter)
        self.inputlistWidget.setObjectName(_fromUtf8("inputlistWidget"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.saveButton = QtGui.QPushButton(self.widget)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.gridLayout.addWidget(self.saveButton, 0, 5, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        self.loadButton = QtGui.QPushButton(self.widget)
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.gridLayout.addWidget(self.loadButton, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.splitter)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit.raise_()
        self.inputButton.raise_()
        self.loadButton.raise_()
        self.saveButton.raise_()
        self.inputlistWidget.raise_()
        self.saveButton.raise_()
        self.exitButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.inputButton.setText(_translate("MainWindow", "Select Folder", None))
        self.exitButton.setText(_translate("MainWindow", "Exit", None))
        self.saveButton.setText(_translate("MainWindow", "Save Edits", None))
        self.loadButton.setText(_translate("MainWindow", "Load File", None))

