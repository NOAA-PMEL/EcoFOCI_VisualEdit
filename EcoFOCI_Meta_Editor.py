#!/usr/bin/env python

"""
 Background:
 --------
 EcoFOCI_Meta_Editor.py
 
 
 Purpose:
 --------
 GUI routine to edit and update NetCDF meta data 
 
 Usage:
 ------

 Layout done with QT Designer


"""
# System Packages
import datetime, os, sys
import yaml, json
import xarray as xr

# GUI Packages
from PyQt4 import QtGui 
import gui_ui.meta_editor_design as design 
			  # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 01, 29)
__modified__ = datetime.datetime(2014, 10, 13)
__version__  = "0.2.0"
__status__   = "Development"

class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        self.inputButton.clicked.connect(self.input_files)  
        self.loadButton.clicked.connect(self.loadMeta)
        self.saveButton.clicked.connect(self.saveMeta)
        self.exitButton.clicked.connect(self.exit_main)

    def input_files(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                                                           "Pick a folder")
        self.inputlistWidget.clear()

        if directory: # if user didn't pick a directory don't continue
            self.directory = str(directory)

            for file_name in os.listdir(directory): # for all files, if any, in the directory
                self.inputlistWidget.addItem(file_name)  # add file to the listWidget

    def loadMeta(self):
        
        self.filename = os.path.join(self.directory, str(self.inputlistWidget.currentItem().text()))
        self.load_netcdf()
        self.yaml_dump()
        self.textEdit.setPlainText(self.yaml_dump())

    def yaml_dump(self):
        for k in self.glob_atts.keys():
            self.glob_atts[k] = str(self.glob_atts[k])
        return yaml.safe_dump(self.glob_atts, default_flow_style=False)
        

    def load_netcdf(self):
        with xr.open_dataset(self.textbox.text(), decode_cf=False) as xrdf:
            self.glob_atts = xrdf.attrs
            self.vars_dic = xrdf.keys()
            self.ncdata = xrdf.load()

    def saveMeta(self):
        pass

    def exit_main(self):
        self.close()

def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function