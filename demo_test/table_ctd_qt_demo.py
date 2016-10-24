#!/usr/bin/env python

"""

ctd_table_qt_demo.py

----
Modification of table_qt_demo.py



http://stackoverflow.com/questions/11736560/edit-table-in-pyqt-using-qabstracttablemodel

"""

# system stack
import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#user stack
# Relative User Stack
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(1, parent_dir)
from io_utils.EcoFOCI_netCDF_read import EcoFOCI_netCDF



def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

# creation of the container
class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.load_netcdf()
        rawdata, header = self.dic2list()

        tablemodel = MyTableModel(rawdata, header, self)
        #tableview = QTableView()
        tableview.setModel(tablemodel)

        #set view sizes
        tableview.setMinimumSize(800,300)
        tableview.resizeColumnsToContents()

        layout = QVBoxLayout(self)
        layout.addWidget(tableview)
        self.setLayout(layout)

    # data ingest
    def load_netcdf( self, file=parent_dir+'/example_data/example_ctd_data.nc'):
        df = EcoFOCI_netCDF(unicode(file))
        self.vars_dic = df.get_vars()
        self.ncdata = df.ncreadfile_dic()
        df.close()

        return self.ncdata

    def dic2list(self, test=False):
        """ Converts a dictionary array of numpy data into a list of lists for the table viewer such that 
                columns are per variable and rows are per depth

            Hard coded in this routine is the name of the dimensions expected (lat,lon,dep,time,time2)
            
            Todo: remove variable naming dependency

        """
        if test:
            tabledata = [[1234567890,2,3,4,5],
                         [6,7,8,9,10],
                         [11,12,13,14,15],
                         [16,17,18,19,20]]     
            header = ['col1','col2','col3','col4','col5']
        else:
            tabledata = [val[0,:,0,0].tolist() for key, val in self.ncdata.iteritems() if key not in ['lat','lon','dep','time','time2']]
            tabledata = [self.ncdata['dep'].tolist()] + tabledata
            trans_tabledata = map(list, zip(*tabledata))

            header = [key for key in self.ncdata.keys() if key not in ['lat','lon','dep','time','time2'] ]
            header = ['dep'] + header

        return trans_tabledata, header


# creattion of the table model
class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

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

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

if __name__ == "__main__":
    main()