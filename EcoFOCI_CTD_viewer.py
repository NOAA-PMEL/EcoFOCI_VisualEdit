#!/usr/bin/env python

"""

Background
----------

EcoFOCI_CTD_viewer.py

----

Merge of ctd_qt_demo.py (matplotlib data viewer based on mpl_qt_demo.py)
and
table_ctd_qt_demo.py (qt tableview with editable columns)

Purpose:
--------

    View and Edit EcoFOCI CTD data in netcdf (EPIC flavored currently) and save edited files

History:
--------

2016-10-24: Bell - Begin merging ctd_qt_demo and table_ctd_qt_demo.py

"""

# system stack
import sys, os, datetime 
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#science stack
import numpy as np
import json

#visual stack
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#user stack
from io_utils.EcoFOCI_netCDF_read import EcoFOCI_netCDF
from io_utils.EcoFOCI_netCDF_write import NetCDF_QCD_CTD
from io_utils import ConfigParserLocal
from calc.EPIC2Datetime import EPIC2Datetime


__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2016, 10, 24)
__modified__ = datetime.datetime(2016, 10, 24)
__version__  = "0.1.0"
__status__   = "Development"

class AppForm(QMainWindow):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    example_path = parent_dir+'/example_data/example_ctd_data.nc'

    def __init__(self, parent=None, active_file=example_path):
        super(AppForm, self).__init__(parent)

        self.dim_list = ['lat','lon','time','time2']
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('EcoFOCI CTD Viewer')

        self.create_menu()
        self.create_main_frame()

        self.textbox.setText(active_file)
        self.populate_dropdown()
        self.load_netcdf()
        self.load_datetime()
        self.create_status_bar()
        self.load_table()
        self.on_draw()

        self.clip = QtGui.QApplication.clipboard()

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = unicode(QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def on_about(self):
        msg = """ EcoFOCI CTD Viewer and {soon .... Editor}:
        
         * Use the matplotlib navigation bar to explore the plot
         * Change the file explored (Reload)
         * Show or hide the grid
         * Allow edits or not of table data
         * Save the plot to a file using the File menu
        """
        QMessageBox.about(self, "About the program", msg.strip())
    
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        xdata = event.artist.get_xdata()
        ydata = event.artist.get_ydata()
        ind = event.ind
        msg = "You've clicked on a point with coords:\n {0}".format( tuple(zip(xdata[ind], ydata[ind])))
        
        QMessageBox.information(self, "Click!", msg)


    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selected = self.tableview.selectedRanges()

            if e.key() == QtCore.Qt.Key_C: #copy
                s = "\t".join([str(self.tableview.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
                s = s + '\n'

                for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
                    #s += self.tableview.verticalHeaderItem(r).text() + '\t'
                    for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.tableview.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)                

    """-------------------------------------
    matplotlib graphics window - plot data 
    ----------------------------------------"""

    def on_draw(self):
        """ 
        Draws/Redrwas the figure

        """
        #choose data source to plot from, table or file
        if self.update_table_cb.isChecked():
            var1 = str(self.param_dropdown.currentText())
            tabledata_updated = self.table2dic()

            xdata = np.array(tabledata_updated[var1],dtype=float)
            y = np.array(tabledata_updated['dep'],dtype=float)
            #make missing data unplotted
            ind = xdata > 1e34
            xdata[ind] = np.nan
            # clear the axes and redraw the plot anew
            #
            self.axes.clear()        
            self.axes.grid(self.grid_cb.isChecked())
            
            if self.datapoints_cb.isChecked():
                self.axes.plot(
                    xdata,y,
                    marker='*',
                    picker=5)
            else:
                self.axes.plot(
                    xdata,y,
                    picker=5)                


            self.fig.suptitle(self.station_data, fontsize=12)

            if self.invert_cb.isChecked():
                self.fig.gca().set_ylim(self.axes.get_ylim()[::-1])

        else:

            var1 = str(self.param_dropdown.currentText())
            try:
                #make missing data unplotted
                xdata = np.copy(self.ncdata[var1][0,:,0,0])
                ind = xdata >1e34
                xdata[ind] = np.nan
                y = self.ncdata['dep'][:]

                # clear the axes and redraw the plot anew
                #
                self.axes.clear()        
                self.axes.grid(self.grid_cb.isChecked())
                
                if self.datapoints_cb.isChecked():
                    self.axes.plot(
                        xdata,y,
                        marker='*',
                        picker=5)
                else:
                    self.axes.plot(
                        xdata,y,
                        picker=5)           

            except:
                #make missing data unplotted
                xdata = np.copy(self.ncdata[var1][:])
                ind = xdata >1e34
                xdata[ind] = np.nan
                y = self.ncdata['dep'][:]

                # clear the axes and redraw the plot anew
                #
                self.axes.clear()        
                self.axes.grid(self.grid_cb.isChecked())
                
                if self.datapoints_cb.isChecked():
                    self.axes.plot(
                        xdata,y,
                        marker='*',
                        picker=5)
                else:
                    self.axes.plot(
                        xdata,y,
                        picker=5) 

            self.fig.suptitle(self.station_data, fontsize=12)

            if self.invert_cb.isChecked():
                self.fig.gca().set_ylim(self.axes.get_ylim()[::-1])

        self.canvas.draw()

        self.highlight_table_column()

    def highlight_table_column(self):
        #higlight column with chosen variable plotted
        self.tableview.selectColumn(self.table_header.index(self.param_dropdown.currentText()))

    def on_table_header_doubleClicked(self, index):
        activeHeader = self.tableview.horizontalHeaderItem(index).text()
        self.param_dropdown.setCurrentIndex(self.param_dropdown.keys().index(activeHeader))
        print str(self.param_dropdown.currentText())
    """-------------------------------------
    Buttons and Actions
    ----------------------------------------"""

    def on_make_missing(self, missing_value=1e35):
        """
        make selected variable all missing values
        """
        if self.update_table_cb.isChecked():
            var1 = str(self.param_dropdown.currentText())
            tabledata_updated = self.table2dic()
            print "setting {var} to {missing}".format(var=var1,missing=missing_value)
            for col in range(self.tableview.columnCount() ):
                if (str(self.tableview.horizontalHeaderItem(col).text()) == var1):
                    for k,v in enumerate(tabledata_updated[var1]):
                        newitem = QTableWidgetItem(str(1e35))
                        self.tableview.setItem(k, col, newitem)
            #self.reload_table(tabledata_updated, from_table=True)
            self.on_draw()
        else:
            var1 = str(self.param_dropdown.currentText())
        

    def on_save(self):
        """
        save to same location with .ed.nc ending
        """
        updated_data = self.table2dic()
        file_out = unicode(self.textbox.text()).replace('.nc','.ed.nc')
        self.save_netcdf(file_out,data=updated_data)
    

    def on_reload(self):
        """
            Reloads (or loads) selected data file
        """
        self.grid_cb.setChecked(True)
        self.update_table_cb.setChecked(False)
        self.invert_cb.setChecked(True)
        self.populate_dropdown()
        self.load_netcdf()
        self.load_datetime()
        self.load_table(reload_table=True)
        self.on_draw()

    def populate_dropdown(self):
        self.load_netcdf()
        self.load_datetime()
        self.station_data = {}
        self.param_dropdown.clear()
        for k in self.vars_dic.keys():
            if k not in ['time','time2','lat','lon']:
                self.param_dropdown.addItem(k)
            elif k not in ['time2','lat','lon']:
                self.station_data[k] =str(self.str_time)
                continue
            elif k not in ['time2']:
                self.station_data[k] =str(self.ncdata[k][0])

    def create_status_bar(self):
        self.status_text = QLabel(json.dumps(self.station_data))
        self.statusBar().addWidget(self.status_text, 1)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot, 
            tip="Save the plot")

        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu, 
            (load_file_action, None, quit_action))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        
    """-------------------------------------
    Main Frame
    ----------------------------------------"""

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.resize(1280,640)
        # Create the mpl Figure and FigCanvas objects. 
        # 5x8 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((2.5, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        
        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        # Other GUI controls
        # 
        self.textbox = QLineEdit()
        self.textbox.setMaximumWidth(400)
        self.textbox.setMinimumWidth(200)
        self.connect(self.textbox, SIGNAL('editingFinished ()'), self.on_draw)
        
        self.draw_button = QPushButton("&Draw")
        self.connect(self.draw_button, SIGNAL('clicked()'), self.on_draw)

        self.reload_button = QPushButton("&Reload")
        self.connect(self.reload_button, SIGNAL('clicked()'), self.on_reload)

        self.save_button = QPushButton("&save")
        self.connect(self.save_button, SIGNAL('clicked()'), self.on_save)

        self.make_missing_button = QPushButton("&make missing")
        self.connect(self.make_missing_button, SIGNAL('clicked()'), self.on_make_missing)

        self.datapoints_cb = QCheckBox("Show &DataPoints")
        self.datapoints_cb.setChecked(True)
        self.connect(self.datapoints_cb, SIGNAL('stateChanged(int)'), self.on_draw)

        self.grid_cb = QCheckBox("Show &Grid")
        self.grid_cb.setChecked(True)
        self.connect(self.grid_cb, SIGNAL('stateChanged(int)'), self.on_draw)

        self.invert_cb = QCheckBox("Show &Invert")
        self.invert_cb.setChecked(True)
        self.connect(self.invert_cb, SIGNAL('stateChanged(int)'), self.on_draw)

        self.update_table_cb = QCheckBox("Use Updated Table")
        self.update_table_cb.setChecked(False)
        self.connect(self.update_table_cb, SIGNAL('stateChanged(int)'), self.on_draw)
                
        self.param_dropdown = QComboBox()

        self.connect(self.param_dropdown, SIGNAL('activated(int)'), self.on_draw)
        
        self.tableview = QTableWidget()
        self.tableview.setMaximumWidth(600)
        self.tableview.setMaximumHeight(600)

        #
        # Layout with box sizers
        # 
        mhbox = QHBoxLayout()
        
        for w in [  self.textbox, self.reload_button]:
            mhbox.addWidget(w)
            mhbox.setAlignment(w, Qt.AlignVCenter)
        mhbox.addStretch()

        mhbox2 = QHBoxLayout()

        for w2 in [ self.grid_cb, self.invert_cb, self.update_table_cb, self.datapoints_cb]:
            mhbox2.addWidget(w2)
            mhbox2.setAlignment(w2, Qt.AlignVCenter)

        mhbox2.addStretch()
        
        mhbox3 = QVBoxLayout()

        for w2 in [ self.param_dropdown, self.make_missing_button, self.draw_button, self.save_button]:
            mhbox3.addWidget(w2)

        mhbox3.addStretch()

        lv_box = QVBoxLayout()
        lv_box.addWidget(self.canvas)
        lv_box.addWidget(self.mpl_toolbar)
        lv_box.addLayout(mhbox)
        lv_box.addLayout(mhbox2)
        lv_box.addStretch()

        h_box = QHBoxLayout()
        h_box.addLayout(lv_box, 7)
        h_box.addWidget(self.tableview, 10)
        h_box.addLayout(mhbox3,1)
       
        self.main_frame.setLayout(h_box)
        self.setCentralWidget(self.main_frame)

    """-------------------------------------
    Convert Data Format
    ----------------------------------------"""

    def dic2list(self):
        """ Converts a dictionary array of numpy data into a list of lists for the table viewer such that 
                columns are per variable and rows are per depth

            Hard coded in this routine is the name of the dimensions expected (lat,lon,dep,time,time2)
            
            Todo: remove variable naming dependency

        """

        header = [key for key in sorted(self.ncdata.keys()) if key not in self.dim_list]
        return header

    def table2dic(self):
        """
        cycle through each column
        """
        updated_data = {}
        

        for col in range(self.tableview.columnCount() ):
            temp = []
            for row in range(0,self.tableview.rowCount() ):
                value = self.tableview.item(row,col).text()
                if float(value) > 1e34:
                    temp = temp + ['1e+35']
                else:
                    temp = temp + [float("{0:.4f}".format(float(value)))]
            updated_data[str(self.tableview.horizontalHeaderItem(col).text())] = temp
        return updated_data

    """-------------------------------------
    Load and Save Data
    ----------------------------------------"""

    def load_table(self, reload_table=False):
        
        if not reload_table:
            self.table_rawdata = self.ncdata
            self.table_header = self.dic2list()
            self.tableview = MyTable(self.table_rawdata, self.dim_list, parent=self.tableview)
        else:
            self.table_rawdata = self.ncdata
            self.tableview.updatedata(self.table_rawdata, self.dim_list)

    def reload_table(self, data, from_table=False):
        self.tableview.updatedata(data, self.dim_list, from_table)

    def load_netcdf(self):
        df = EcoFOCI_netCDF(unicode(self.textbox.text()))
        self.glob_atts = df.get_global_atts()
        self.vars_dic = df.get_vars()
        self.ncdata = df.ncreadfile_dic()
        df.close()

    def load_datetime(self):
        dt_from_epic =  EPIC2Datetime(self.ncdata['time'], self.ncdata['time2'])
        self.str_time = dt_from_epic[0].strftime('%Y-%m-%d %H:%M:%S')


    def save_netcdf( self, file, **kwargs):
        data=kwargs['data']

        #remove attributes that will get autogenerated in netcdf generation
        map(lambda x: self.glob_atts.pop(x,None), ['EPIC_FILE_GENERATOR'])

        #read in basic epic key parameters
        df = EcoFOCI_netCDF(unicode(self.textbox.text()))
        nchandle = df._getnchandle_()

        ncinstance = NetCDF_QCD_CTD(savefile=file)
        ncinstance.file_create()
        ncinstance.sbeglobal_atts(**self.glob_atts)
        ncinstance.dimension_init(depth_len=len(self.ncdata['dep']))
        ncinstance.variable_init(nchandle)
        ncinstance.add_coord_data(depth=self.ncdata['dep'], latitude=self.ncdata['lat'], 
                longitude=self.ncdata['lon'], time1=self.ncdata['time'], time2=self.ncdata['time2'],)
        ncinstance.add_data(data_dic=data)
        ncinstance.add_history('Profile edited and QC\'d')

        df.close()
        ncinstance.close()

"""-------------------------------------QTable Widget ----------------------------------------------"""

class MyTable(QTableWidget):
    def __init__(self, data, dim_list, parent = None, *args):
        QTableWidget.__init__(self, parent, *args)
        self.data = data
        self.dim_list = dim_list
        self.setRowCount(np.shape(self.data['dep'])[0])
        self.setColumnCount(len(self.data) - len(self.dim_list))
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setMinimumSize(600,600)
        self.connect(self.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.onClick)

    def onClick(self):
        print("test")
        
    def flags(self):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def updatedata(self, data, dim_list, from_table=False):
        self.dim_list = dim_list
        self.data.clear()
        self.data.update(data)
        self.setRowCount(np.shape(data['dep'])[0])
        if not from_table:
            #refreshing from the table doesn't have any spatial dimensions
            self.setColumnCount(len(data) - len(self.dim_list))
        else:
            self.setColumnCount(len(data))

        self.setmydata(from_table)

    def setmydata(self, from_table=False):
 
        horHeaders = []
        valCol = 0
        if not from_table:
            for n, key in enumerate(sorted(self.data.keys())):
                if (key not in self.dim_list):
                    horHeaders.append(key)
                    poparray = np.array(self.data[key])
                    try:
                        for m, item in enumerate(poparray[0,:,0,0]):
                            newitem = QTableWidgetItem(str(item))
                            self.setItem(m, valCol, newitem)
                            verHeaders=m
                    except IndexError:
                        for m, item in enumerate(poparray[:]):
                            newitem = QTableWidgetItem(str(item))
                            self.setItem(m, valCol, newitem)
                            verHeaders=m
                    valCol += 1
        else:
            for n, key in enumerate(sorted(self.data.keys())):
                if (key not in self.dim_list):
                    print "Updating {key}".format(key=key)
                    horHeaders.append(key)
                    poparray = np.array(self.data[key])
                    for m, item in enumerate(poparray):
                        newitem = QTableWidgetItem(str(item))
                        self.setItem(m, valCol, newitem)
                        verHeaders=m

        self.setHorizontalHeaderLabels(horHeaders)
        self.setVerticalHeaderLabels([str(x) for x in range(0,verHeaders+1)])


"""-------------------------------------Main Loop----------------------------------------------"""

def main():
    app = QApplication(sys.argv)
    args = app.arguments()
    try:
        form = AppForm(active_file=args[1])
    except:
        form = AppForm()
    app.setStyle("plastique")
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()