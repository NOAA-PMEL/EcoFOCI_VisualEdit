"""

table_qt_demo.py

http://stackoverflow.com/questions/11736560/edit-table-in-pyqt-using-qabstracttablemodel

"""

# system stack
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# data
my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22']]

def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

# creation of the container
class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        tablemodel = MyTableModel(my_array, self)
        tableview = QTableView()
        tableview.setModel(tablemodel)

        layout = QVBoxLayout(self)
        layout.addWidget(tableview)
        self.setLayout(layout)

# creattion of the model
class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return (self.arraydata[index.row()][index.column()])

    def setData(self, index, value, role):
        self.arraydata[index.row()][index.column()] = value
        return True
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

if __name__ == "__main__":
    main()