# EcoFOCI_VisualEdit
GUI CTD and Timeseries visualization and editing

Developed for PMEL EcoFOCI Program

<pre>
.
├── EcoFOCI_CTD_viewer.py
├── README.md
├── __init__.py
├── calc
│   ├── EPIC2Datetime.py
│   ├── EPIC2Datetime.pyc
│   ├── __init__.py
│   └── __init__.pyc
├── demo_test
│   ├── ctd_qt_demo.py
│   ├── mpl_qt_demo.py
│   ├── table_ctd_qt_demo.py
│   ├── table_qt_demo.py
│   └── timeseries_qt_demo.py
├── example_data
│   ├── example_ctd_data.ed.nc
│   ├── example_ctd_data.nc
│   └── example_timeseries_data.nc
└── io_utils
    ├── EcoFOCI_netCDF_read.py
    ├── EcoFOCI_netCDF_read.pyc
    ├── EcoFOCI_netCDF_write.py
    ├── EcoFOCI_netCDF_write.pyc
    ├── __init__.py
    └── __init__.pyc
</pre>


## Available routines

demo_test
+ ctd_qt_demo.py --- ctd profile plots
+ timeseries_qt_demo.py --- timeseries plots
+ mpl_qt_demo.py --- original code for basis   
+ table_ctd_qt_demo.py --- ctd table demo (using data from netcdf)
+ table_qt_demo.py --- basic table view for qt
