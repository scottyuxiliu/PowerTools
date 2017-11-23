help_message = '''
PPO POWER ANALYSIS PYTHON SCRIPT

Download Anaconda Python Package v2.7 from: http://continuum.io/downloads

    Summary:
        This script plots rails specified by the input config file using values from the input data file.
        To plot rails indicated by config file, uncomment rail names from config file.
        eg.
        TOTAL_APU_POWER
        #TOTAL_MEM_POWER
        #TOTAL_APU_MEM_POWER
        will only plot the TOTAL_APU_POWER rail.

    Syntax:
        -h      displays help message
        -c      creates config file
        -s      combines graphs of the same data type (eg. plot 3 voltage rails into 1 graph instead of 3 separate graphs)
        --dat   file name of data file
        --con   file name of config file
        --avg   file name of output file for averaged rail data; suppresses graphical output
        --int   moving average interval size (seconds) default 1s
        --step  moving average step size (seconds) default 1s

    Example:
        Python PowerAnalysis.py --dat=cz_data.csv --con=cz_config.txt --int=60 --step=30 -s

    Version | Description | Editor | Date
    0.1 | Initial Release | Rose Li | March 2015
    0.2 | Fixed bugs: can't plot less than 8192 points, last rail does not get plotted | Rose Li | March 2015
    0.3 | Added moving average support | Rose Li | March 2015
    0.4 | Added min, max, average inset | Rose Li | April 2015
    0.5 | Added feature for only calculating averages (no plotting), changed xaxis to min instead of s, round min/max/avg to 3 dec points | Rose Li | April 2015
    0.6 | Modified input argument style | Ben Ling | April 2015
    0.7 | Merge Ben's modifications, output --avg data to text file | Rose Li | May 2015
    0.8 | Enable plotting selected rails on same graph with -s (includes draggable legend) | Rose Li | July 2015
    0.8.1 | Fixed auto scientific notation on axis bug | Rose Li | July 2015
    0.9 | Changed script to GUI format, removed all functionalities except basic plotting | Rose Li | July 2015
    0.9.1 | Added button to create config file | Rose Li | July 2015
    0.9.2 | Re-added feature to stack like rails | Rose Li | July 2015
    0.9.3 | Re-added feature to output average straight to file and moving average and see config file | Rose Li | July 2015
    0.9.4 | Rewrote GUI to feature relative positioning, added toggle-to-plot checkboxes | Rose Li | Aug 2015
    0.9.5 | Minor changes for ppt presentation | Rose Li | Aug 2015
    0.9.6 | Added min/max to csv output, re-added support for <1s moving avg, added error msgs, suppress warnings | Rose Li | Aug 2015
    1.0 | Final Release | Rose Li | Aug 2015
    
    2.0 June 2016
    -can open multiple graphs from different data files 
    -added feature: stacked plots will update if different rails are selected and plot again
    -added output to clipboard
    -minor GUI changes
    -added select buttons
    -added auto load for config file
    -optimized unstacked plotting 
    -disabled webbrowser loading of config files
    
    2.1 July 2016
    -filter getopenfilename types
    -Major GUI changes
    -added tooltips
    -name plots
    
    2.2 July 2016
    -deprecated config file
    -fixed bug where rails don't load if there are different rails after switching datafiles
    -added feature where switching to different data file will check all rails that were previously checked if they exist
    
    
    Useful additions:
    colour choices to rail
    plot data that have been modified with ctrl+shift+R excel script
    save interactive figures
    package script as .exe
    grid
    2 Y axis
'''

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox, QGridLayout, QGroupBox, QHBoxLayout, QScrollArea, QFileDialog
from PyQt5.QtGui import QIcon

#import time 
#import webbrowser


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
    def initUI(self):

        """labels"""
        ###Text Written directly onto the GUI (Qt.GUI.QLabel)###
        #Labels in "Input Files"
        #self.label_configfile = QLabel('Config File Name:', self)
        self.label_datafile = QLabel('Data File Name:', self)

        #Labels in "Figure Options"
        #Qiwei Zong came up with the idea of putting spaces to align the line edits. Much easier than using stretch on HBoxes.
        #QWidget.setToolTip - Creates a bubble popup when hovering over the label
        #QWidget.setDisabled - Disables the label. Only Stacked/Unstacked can be used at a time.
        self.label_figurename = QLabel('Stacked Figure Name:    ', self)
        self.label_unstackedfigurename = QLabel('Unstacked Figure Name:', self)
        self.label_unstackedfigurename.setToolTip('Change Figure Title to the format "Figure Name - Railname"')
        self.label_figurename.setToolTip('Change Figure Title to the format "Figure Name"')
        self.label_figurename.setDisabled(True)

        #Labels in "Moving Average"
        self.label_MV_int = QLabel('Interval (secs):', self)
        self.label_MV_int.setToolTip('Number of seconds of data condensed into a single point (Can be <1s)')
        self.label_MV_int.setDisabled(True)
        self.label_MV_step = QLabel('Step size (secs):', self)
        self.label_MV_step.setToolTip('Number of seconds between each interval (Can be <1s)')
        self.label_MV_step.setDisabled(True)

        #Label in "Scrolling Area"
        #QWidget.setAlignment - Sets the alignment
        self.label_scrolllist = QLabel('Please select a data file to load the rails', self)
        self.label_scrolllist.setAlignment(QtCore.Qt.AlignCenter)

        '''line edits'''
        ###Area where user can input text###
        #Input Config name
        #QLineEdit.textChanged - Sets off a signal when the text is modified by either the user or programatically
        #QWidget.QSignal.connect - Jumps to a functions when a signal is raised

        #Input Datafile name
        self.le_datafilename = QLineEdit(self)
        self.le_datafilename.textChanged.connect(self.loadDatafile)

        #Input stacked figure name
        self.le_stacked_figure_name = QLineEdit(self)
        self.le_stacked_figure_name.setDisabled(True)

        #input unstacked figure name
        self.le_unstacked_figure_name = QLineEdit(self)

        #input moving average interval
        self.le_MV_int = QLineEdit(self)
        self.le_MV_int.setText("1") #Sets text initially to 1
        self.le_MV_int.setDisabled(True)

        #input moving average step size
        self.le_MV_step = QLineEdit(self)
        self.le_MV_step.setText("1")
        self.le_MV_step.setDisabled(True)

        '''checkboxes'''
        ###Self explanatory name###
        self.cb_stack = QCheckBox('Plot multiple rails to one graph', self)
        self.cb_stack.setToolTip('Plot multiple rails of the same type (i.e. Power, Voltage or Current) to one graph')
        self.cb_stack.stateChanged.connect(self.stackPlot)
        self.cb_MV = QCheckBox('Use moving average', self)
        self.cb_MV.setToolTip('Reduces noise in chosen rails')
        self.cb_MV.stateChanged.connect(self.MVenable)

        '''buttons'''
        ###Load Filename buttons###
        #Browse Config
        #self.button_browseconfig = QPushButton('Browse', self)
        #self.button_browseconfig.clicked.connect(self.selectConfigFile)

        #Browse Data
        self.button_browsedata = QPushButton('Browse', self)
        self.button_browsedata.clicked.connect(self.selectDataFile)

        ###Plot/computation buttons###
        self.button_plot = QPushButton('Plot', self)
        self.button_plot.setToolTip('Plot the selected rails')
        self.button_plot.clicked.connect(self.mainOutput)
        self.button_avg = QPushButton('Output min/max/avg to csv', self)
        self.button_avg.setToolTip('Output the min/max/avg of the selected rails to a csv file in the same directory as the data file')
        self.button_avg.clicked.connect(self.avgOutput)
        self.button_clipboard = QPushButton('Copy avg to clipboard', self)
        self.button_clipboard.setToolTip('Copy the average of the selected rails in order to the clipboard. Press Ctrl+V to Paste.')
        self.button_clipboard.clicked.connect(self.avgClipboard)

        #select all buttons
        self.button_selectP = QPushButton('Select all P', self)
        self.button_selectP.setToolTip('Select all Power rails')
        self.button_selectP.clicked.connect(self.selectallP)
        self.button_selectV = QPushButton('Select all V', self)
        self.button_selectV.setToolTip('Select all Voltage rails')
        self.button_selectV.clicked.connect(self.selectallV)
        self.button_selectI = QPushButton('Select all I', self)
        self.button_selectI.setToolTip('Select all Current rails')
        self.button_selectI.clicked.connect(self.selectallI)
        self.button_selectall = QPushButton('Select All', self)
        self.button_selectall.setToolTip('Select all rails')
        self.button_selectall.clicked.connect(self.selectAll)
        self.button_clearall = QPushButton('Clear All', self)
        self.button_clearall.setToolTip('Clear all rails')
        self.button_clearall.clicked.connect(self.clearAll)

        #Load and Save config buttons
        #self.button_load = QPushButton('Save Config File', self)
        #self.button_load.setToolTip('Save the current selected rails to a config file')
        #self.button_load.clicked.connect(self.saveConfig)

        '''Other variables'''
        self.stack = False
        self.stack_changed = False
        self.useMV = False
        self.MV_change = False
        self.useAVG = False
        self.useClipboard = False
        self.useFN = [False, True] #useFN[0] is for stacked, #useFN[1] is for unstacked
        self.useShowConfig = True
        self.data_filename_changed = True
        self.data_filename_previous = " "
        self.data_filename_list = []
        self.cb_config_list = []
        self.cb_test = QCheckBox("test")
        self.config_file_content_detail = []
        self.msgBox = QMessageBox();

        '''Layout'''
        self.parentlayout = QGridLayout()

        #Layout/Sections
        #Input Layout
        self.gb_input = QGroupBox('Input Files')
        self.gb_input.setToolTip('Browse for a data file (ie. raw output file from DAQJammer)to load the rails')
        self.layout_input = QGridLayout()
        self.gb_input.setLayout(self.layout_input)

        #Plot Options Layout
        self.gb_plotoptions = QGroupBox('Plot Options')
        self.layout_plotoptions = QGridLayout()
        self.gb_plotoptions.setLayout(self.layout_plotoptions)

        #Moving Average Layout
        self.gb_movingaverage = QGroupBox('Moving Average')
        self.layout_movingaverage = QGridLayout()
        self.gb_movingaverage.setLayout(self.layout_movingaverage)

        #Figure Options Layout
        self.gb_figure_options = QGroupBox('Figure Options')
        self.layout_figure_options = QGridLayout()
        self.gb_figure_options.setLayout(self.layout_figure_options)
        #Rail Options Layout
        self.gb_railoptions = QGroupBox('Rails')
        self.layout_railoptions = QGridLayout()
        self.gb_railoptions.setLayout(self.layout_railoptions)
        #Output Layout
        self.gb_output = QGroupBox('Output')
        self.layout_output = QGridLayout()
        self.gb_output.setLayout(self.layout_output)

        '''Widgets/buttons/checkboxes/sub layouts/line edits'''
        #Add labels, line edits and browse button to "Input Files"
        self.layout_input.addWidget(self.label_datafile, 1, 0)
        self.layout_input.addWidget(self.le_datafilename, 1, 1)
        self.layout_input.addWidget(self.button_browsedata, 1, 2)

        #Add Checkbox and Line edits to "Moving Average"
        self.layout_movingaverage.addWidget(self.cb_MV, 1, 0)
        self.layout_movingaverage.addWidget(self.label_MV_int, 2, 0)
        self.layout_movingaverage.addWidget(self.le_MV_int, 2, 1)
        self.layout_movingaverage.addWidget(self.label_MV_step, 3, 0)
        self.layout_movingaverage.addWidget(self.le_MV_step, 3, 1)

        #Create Hbox stacked figure name inside "Figure options"
        self.hbox_figure_name = QHBoxLayout()
        self.hbox_figure_name.addWidget(self.label_figurename)
        self.hbox_figure_name.addWidget(self.le_stacked_figure_name)
        #Create Hbox unstacked figures name option inside "Figure options"
        self.hbox_unstackedfigure_name = QHBoxLayout()
        self.hbox_unstackedfigure_name.addWidget(self.label_unstackedfigurename)
        self.hbox_unstackedfigure_name.addWidget(self.le_unstacked_figure_name)
        #Add Figure Name Hboxes and Stacked checkbox to "Figure Options"
        self.layout_figure_options.addWidget(self.cb_stack, 1, 0)
        self.layout_figure_options.addLayout(self.hbox_unstackedfigure_name, 2, 0)
        self.layout_figure_options.addLayout(self.hbox_figure_name, 3, 0)

        #Add the "Figure Options Layout" and "Moving Average Layout" to "Plot Options"
        self.layout_plotoptions.addWidget(self.gb_figure_options, 1, 1)
        self.layout_plotoptions.addWidget(self.gb_movingaverage, 1, 0)

        #Create Scroll list area for the rails
        self.scroll_configlist = QScrollArea()
        self.scroll_configlist.setWidgetResizable(True)
        self.scroll_configlist.setFixedHeight(200)
        self.widget_scrollareacontent = QWidget()
        self.scroll_configlist.setWidget(self.widget_scrollareacontent)
        self.layout_scrollarealayout = QGridLayout()
        self.widget_scrollareacontent.setLayout(self.layout_scrollarealayout)
        self.layout_scrollarealayout.addWidget(self.label_scrolllist)

        #Add select all buttons "Rail"
        self.layout_railoptions.addWidget(self.scroll_configlist, 1, 0, 1, 5)
        self.layout_railoptions.addWidget(self.button_selectV, 2, 0)
        self.layout_railoptions.addWidget(self.button_selectI, 2, 1)
        self.layout_railoptions.addWidget(self.button_selectP, 2, 2)
        self.layout_railoptions.addWidget(self.button_selectall, 2, 3)
        self.layout_railoptions.addWidget(self.button_clearall, 2, 4)
        #self.layout_railoptions.addWidget(self.button_load, 2, 5)

        #Create Hbox option inside "Output"
        #Add the plot and output buttons
        self.hbox_output = QHBoxLayout()
        self.hbox_output.addWidget(self.button_avg)
        self.hbox_output.addWidget(self.button_clipboard)
        self.hbox_output.addWidget(self.button_plot)
        self.layout_output.addLayout(self.hbox_output, 1, 0)

        #Add sections to the Main Window/GUI
        self.parentlayout.addWidget(self.gb_input, 1, 0)
        self.parentlayout.addWidget(self.gb_railoptions, 2, 0)
        self.parentlayout.addWidget(self.gb_plotoptions, 3, 0)
        self.parentlayout.addWidget(self.gb_output, 4, 0)
        self.setLayout(self.parentlayout)

        #Display GUI
        self.setGeometry(50, 50, 600, 339)
        self.setWindowTitle('PPO Power Analysis Tool')
        self.show()
        
    """GUI functions"""
    def selectDataFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "Data File (*.csv)")
        self.le_datafilename.setText(fileName)
    def loadDatafile(self):
        #Check to see if the datafile exists before loading
        if QtCore.QFile.exists(self.le_datafilename.text()):
            self.layout_scrollarealayout.removeWidget(self.label_scrolllist)
            self.label_scrolllist.hide()
            self.loadConfig()
            self.useShowConfig = True
            self.scroll_configlist.show()
        else:
            if str(self.le_datafilename.text()) == "":
                self.label_scrolllist.setText('Please select a config file or data file to load the rails')
            else:
                self.label_scrolllist.setText('The data file selected does not exist')
    def loadConfig(self):
        self.config_file_content_detail = self.createRailList() #config_file_content_detail is a list of tuples in the form of {rail name, bool}
        #delete any existing loaded checkboxes from config file
        if self.cb_config_list != []:
            for x in xrange (0, len(self.cb_config_list)):
                self.layout_scrollarealayout.removeWidget(self.cb_config_list[x])
                self.cb_config_list[x].deleteLater()
            self.cb_config_list = []
        #load new checkboxes
        for x in xrange (0, len(self.config_file_content_detail)):
            self.cb_new = QCheckBox(self.config_file_content_detail[x][0], self)
            if self.config_file_content_detail[x][1]:
               self.cb_new.toggle()
            self.cb_config_list.append(self.cb_new)
            self.cb_config_list[x].stateChanged.connect(self.configToggled)
            self.layout_scrollarealayout.addWidget(self.cb_config_list[x], x%7, x/7)
    def createRailList(self):
        #Check if there are rails
        if not self.config_file_content_detail: #No Rails
            rail_temp = ["Rail", False] #All rails False because, it's the first data file being loaded
            rail_list = [] #Contains final list of all rails
            #data_raw = pd.read_csv(str(self.le_datafilename.text()), header=1, index_col=0, skiprows=[2], nrows=2) #Read the data file and skip blank lines header row
            data_raw = pd.read_csv(str(self.le_datafilename.text()), index_col=0, skip_blank_lines=True, nrows=2) #Read the data file and skip blank lines header row

            for x in xrange(1, len(data_raw.iloc[0])):
                #Parse the Rail names
                config_railname = data_raw.columns[x].split('=', 1) #Rails name are in the form "RAILNAME = FORMULA" or "RAILNAME". Split at '='.
                rail_temp[0] = config_railname[0] #Take first element for Railname
                rail_list.append(rail_temp) #Appended to list
                rail_temp = ["Rail", False]
            return rail_list
        else:
            data_raw = pd.read_csv(str(self.le_datafilename.text()), index_col=0, skip_blank_lines=True, nrows=2)
            if len(data_raw.iloc[0]) == len(self.config_file_content_detail): #Same numbers of rails. Same rails.
                return
            else: #data file has more rails.
                rail_temp = ["Rail", False] #All rails False because, it's the first data file being loaded
                rail_list = [] #Contains final list of all rails
                for x in xrange(1, len(data_raw.iloc[0])):
                    #Parse the Rail names
                    config_railname = data_raw.columns[x].split('=', 1) #Rails name are in the form "RAILNAME = FORMULA" or "RAILNAME". Split at '='.
                    rail_temp[0] = config_railname[0] #Take first element for Railname
                    rail_list.append(rail_temp) #Appended to list
                    rail_temp = ["Rail", False]

                #Check all rails that were previously checked
                checked_rails = self.config_read_checkboxes() #List of checked rails
                temp = [] #Make a list to use index method
                for x in xrange(0,len(rail_list)):
                    temp.append(rail_list[x][0])

                #Loop through checked rails.
                for x in xrange(0, len(checked_rails)):
                    try:
                        location = temp.index(checked_rails[x]) #If the old rail exists in the new data file. Set boolean to TRUE. Otherwise jump to next iteration.
                    except:
                        continue
                    else:
                        rail_list[location][1] = True
                return rail_list

    def selectAll(self):
        for x in xrange (0, len(self.config_file_content_detail)):
            if not self.config_file_content_detail[x][1]:
                self.cb_config_list[x].toggle()
                self.config_file_content_detail[x][1] = True
    def selectallV(self):
        for x in xrange (0, len(self.config_file_content_detail)):
            if self.config_file_content_detail[x][0][-1] == 'V':
                if not self.config_file_content_detail[x][1]:
                    self.cb_config_list[x].toggle()
                    self.config_file_content_detail[x][1] = True
    def selectallI(self):
        for x in xrange (0, len(self.config_file_content_detail)):
            if self.config_file_content_detail[x][0][-1] == 'I':
                if not self.config_file_content_detail[x][1]:
                    self.cb_config_list[x].toggle()
                    self.config_file_content_detail[x][1] = True
    def selectallP(self):
        for x in xrange (0, len(self.config_file_content_detail)):
            if self.config_file_content_detail[x][0][-1] == 'P':
                if not self.config_file_content_detail[x][1]:
                    self.cb_config_list[x].toggle()
                    self.config_file_content_detail[x][1] = True
    def clearAll(self):
        for x in xrange (0, len(self.config_file_content_detail)):
            if self.config_file_content_detail[x][1]:
                self.cb_config_list[x].toggle()
                self.config_file_content_detail[x][1] = False

    def config_read_checkboxes(self):
        config_file_content_parsed = []
        for x in xrange (0, len(self.config_file_content_detail)):
            if (self.config_file_content_detail[x][1]):
                config_file_content_parsed.append(self.config_file_content_detail[x][0])
        return config_file_content_parsed

    """
    def saveConfig(self):
        config_filename = str(self.le_configfilename.text())
        config_file = open(config_filename, "w")
        if self.cb_config_list !=[]:
            for x in xrange (0, len(self.cb_config_list)):
                if (not self.cb_config_list[x].isChecked()):
                    config_file.write("#%s\n" % self.cb_config_list[x].text())
                else:
                    config_file.write("%s\n" % self.cb_config_list[x].text())
            config_file.close()
        #webbrowser.open(config_filename)
    """

    def dataFilename(self):
        self.data_filename_changed = True
    def stackPlot(self):
        self.stack_changed = True
        if self.cb_stack.isChecked():
            #Enable naming of figures.
            self.label_figurename.setDisabled(False)
            self.le_stacked_figure_name.setDisabled(False)
            self.label_unstackedfigurename.setDisabled(True)
            self.le_unstacked_figure_name.setDisabled(True)
            #Use stack plot
            self.stack = True
        else:
            #Disable naming of figures
            self.label_figurename.setDisabled(True)
            self.le_stacked_figure_name.setDisabled(True)
            self.label_unstackedfigurename.setDisabled(False)
            self.le_unstacked_figure_name.setDisabled(False)
            #Disable Stack plot
            self.stack = False
    def configToggled(self):
        sender = self.sender()
        for x in xrange (0, len(self.cb_config_list)):
            if sender.text() == self.config_file_content_detail[x][0]:
                self.config_file_content_detail[x][1] = not self.config_file_content_detail[x][1]
                break
    def MVenable(self):
        self.MV_change = True
        if self.cb_MV.isChecked():
            self.label_MV_int.setDisabled(False)
            self.label_MV_step.setDisabled(False)
            self.le_MV_int.setDisabled(False)
            self.le_MV_step.setDisabled(False)
            self.useMV = True
        else:
            self.label_MV_int.setDisabled(True)
            self.label_MV_step.setDisabled(True)
            self.le_MV_int.setDisabled(True)
            self.le_MV_step.setDisabled(True)
            self.useMV = False
    def avgClipboard(self):
        self.useClipboard = True
        self.useAVG = False
        self.mainPlot()
    def avgOutput(self):
        self.useAVG = True
        self.useClipboard = False
        self.mainPlot()
    def mainOutput(self):
        self.useAVG = False
        self.useClipboard = False
        self.mainPlot()
    def mainPlot(self):
        #""" Variables """
        ##Get config and data file names
        #data_filename = str(self.le_datafilename.text())
        #figure_name = []
        #figure_name.append(str(self.le_stacked_figure_name.text()))
        #figure_name.append(str(self.le_unstacked_figure_name.text()))

        ##Check if user has input a figure title to use.
        ##Checking stacked figure name
        #if figure_name[0] == '':
        #	self.useFN[0] = False
        #else:
        #	self.useFN[0] = True
        ##Checking unstacked figure name
        #if figure_name[1] == '':
        #	self.useFN[1] = False
        #else:
        #	self.useFN[1] = True


        ##If data filenames is empty
        #if data_filename == '':
        #	self.msgBox.setText("Please choose a data file");
        #	self.msgBox.exec_();
        #	return

        ##Check if data file has changed. Check to see if a new figure needs to be made instead of updating current figures.
        #if data_filename != self.data_filename_previous:
        #	self.data_filename_changed = True
        #else:
        #	self.data_filename_changed = False
        #self.data_filename_previous = data_filename

        ##Read inverval and step data for Moving Average, if there is data
        #MVinterval = float(self.le_MV_int.text())
        #MVstep = float(self.le_MV_step.text())
        
  #      """ Main Script Read data from .csv file """
  #      data_raw = pd.read_csv(data_filename, index_col=0, skip_blank_lines=True) #read .csv data into data_raw
  #      #print(data_raw.head(5))

        ##If no config file; Make a config file.
        #if(self.useShowConfig):
  #          config_file_content_parsed = self.config_read_checkboxes()
        #data_file_content_parsed = data_getrail(config_file_content_parsed, data_raw)

        ##Output to Clipboard
        ##Optimize by making a bool so if datafilename and cb_config_list hasn't changed, can just use the data stored in self.average data.
        ##Can use the bool for self.useAVG/output to CSV as well
        #if self.useClipboard:
        #	temp = []
        #	for x in xrange(1, len(data_file_content_parsed)):
        #		(max, min, avg) = data_average(data_file_content_parsed[x])
        #		temp.append(avg)
        #	clipboard_text = "\t".join(map(str, temp))
        #	clipboard = QApplication.clipboard()
        #	clipboard.setText(clipboard_text)

        ##Output to CSV
        #elif self.useAVG:
        #	if len(data_file_content_parsed) <= 1:
        #		self.msgBox.setText("No rails to calculate");
        #		self.msgBox.exec_();
        #		return
        #	avg_filename = data_filename[:-4]+"_avg.csv"
        #	avg_write(avg_filename, config_file_content_parsed, data_file_content_parsed)
        #	#webbrowser.open(avg_filename)

        ##Plot Rails
        #else:
        #	if len(data_file_content_parsed) <= 1:
        #		self.msgBox.setText("No rails to plot");
        #		self.msgBox.exec_();
        #		return
        #	if self.useMV:
        #		data_content_MV = data_moving_average(data_file_content_parsed, config_file_content_parsed, MVinterval, MVstep)
        #		plt.ion()
        #		data_plot(data_content_MV, config_file_content_parsed, data_filename, figure_name, self.stack, self.data_filename_changed, self.stack_changed, self.MV_change, self.useFN)
        #	else:
        #		plt.ion()
        #		data_plot(data_file_content_parsed, config_file_content_parsed, data_filename, figure_name, self.stack, self.data_filename_changed, self.stack_changed, self.MV_change, self.useFN)
        #	plt.draw()
        #	self.stack_changed = False
        #	self.MV_change = False





"""computational functions"""
#make a list of the selected rails in the config file
def config_read(config_filename):
    config_file = open(config_filename, "r")
    config_file_content = config_file.readlines()
    config_file.close()
    config_file_content_parsed = []

    for x in xrange(0, len(config_file_content)):
        if config_file_content[x][0] != "#":
            config_file_content_parsed.append(config_file_content[x].split('\n', 1)[0])
    return config_file_content_parsed

#Used for reading the config file to determine which rails need to be checked in the scroll list
def config_read_detail(config_filename):
    config_file = open(config_filename, "r")
    config_file_content = config_file.readlines()
    config_file.close()
    config_file_content_detail = []
    config_file_content_detail_temp = []

    for x in xrange(0, len(config_file_content)):
        #if '#' is the not the first character, add rail name and True to be checked
        if config_file_content[x][0] != "#":
            config_file_content_detail_temp.append(config_file_content[x].split('\n', 1)[0])
            config_file_content_detail_temp.append(True)
            #config_file_content_detail_temp.append(np.random.rand(3)) I have no idea why Rose has this.
        else: #add name and False to leave unchecked
            config_file_content_detail_temp.append(config_file_content[x][1:].split('\n', 1)[0])
            config_file_content_detail_temp.append(False)
            #config_file_content_detail_temp.append(np.random.rand(3))
        config_file_content_detail.append(config_file_content_detail_temp)
        config_file_content_detail_temp = []
    return config_file_content_detail

def data_getrail(config_file_content_parsed, data_raw):
    data_file_content_parsed = []
    #slices the first column
    data_file_content_parsed.append(data_raw.iloc[0:, 0:1])

    for x in xrange(0, len(config_file_content_parsed)):
        for y in xrange(0, len(data_raw.columns)):
            # if the header in data_raw is == the name in config file parsed, grab the column
            if config_file_content_parsed[x] == data_raw.columns[y].split('=', 1)[0]:
                data_file_content_parsed.append(data_raw.iloc[0:, y:y + 1])
    return data_file_content_parsed

def data_plot(data_file_content_parsed, config_file_content_parsed, data_filename, figure_name, stack_graph = False, data_filename_changed = False, stack_graph_change = False, MV_change = False, FN_enable = False):
    #No rails are selected. Data File content parsed contains data of selected rails.
    if len(data_file_content_parsed) <= 1:
        print "No rails chosen"
        return

    #Only clear a figure if filename and figure options haven't been changed (i.e. only updating current figures and not making/modifying more)
    if not data_filename_changed:
        if not stack_graph_change:
            if not MV_change:
                #Make sure figures exist and haven't been closed
                if plt.get_fignums():
                    plt.clf()

    #One figure for each plot
    if not stack_graph:
        for x in xrange(1, len(data_file_content_parsed)):
            fig = plt.figure(data_filename.split('/')[-1] + " - " + config_file_content_parsed[x - 1])
            ax = fig.add_subplot(111)
            ax.set_xlabel('Time [s]')
            if config_file_content_parsed[x - 1][-1] == 'P':
                ax.set_ylabel('Power [W]')
                #Yellow and Green
                line_colour = [np.random.rand(), 1 , 0]
            elif config_file_content_parsed[x - 1][-1] == 'I':
                ax.set_ylabel('Current [A]')
                #Blue and Purple
                line_colour = [np.random.rand(), 0, 1]
            elif config_file_content_parsed[x - 1][-1] == 'V':
                ax.set_ylabel('Voltage [V]')
                #Green and Teal
                line_colour = [0, 1, np.random.rand()]
            #SR Voltage and others
            else:
                ax.set_ylabel('Voltage [V]')
                #Green and Teal
                line_colour = [0, 1, np.random.rand()]
            (max, min, avg) = data_average(data_file_content_parsed[x])

            fig.text(0.18, 0.82, "Max: %.3f\nMin: %.3f\nAvg: %.3f" % (max, min, avg), size=10, ha="left", va="center",
                     bbox=dict(boxstyle="square", ec=(0.5, 0.5, 0.5), facecolor=(1, 1, 1)))
            if FN_enable[1]:
                ax.set_title(figure_name[1] + " - " + config_file_content_parsed[x - 1])
            else:
                ax.set_title(config_file_content_parsed[x - 1])
            plt.plot(data_file_content_parsed[0], data_file_content_parsed[x], color= line_colour)
            plt.axhline(avg, 0, 1, color="red")
    else:
        #if multiple figures exist from the same file , clear all
        # optimize by making it if STACKED figures exist, clear all (currently if any figures exist)
        if len(plt.get_fignums()) > 1:
            #Selecting the stacked figures and clearing them
            for x in xrange(1, len(data_file_content_parsed)):
                if config_file_content_parsed[x - 1][-1] == 'P':
                    fig = plt.figure(data_filename.split('/')[-1] + " - Power")
                elif config_file_content_parsed[x - 1][-1] == 'I':
                    fig = plt.figure(data_filename.split('/')[-1] + " - Current")
                elif config_file_content_parsed[x - 1][-1] == 'V':
                    fig = plt.figure(data_filename.split('/')[-1] + " - Voltage")
                elif (config_file_content_parsed[x - 1][-2] == 'S') & (config_file_content_parsed[x - 1][-1] == 'R'):
                    fig = plt.figure(data_filename.split('/')[-1] + " - Voltage across sense resistor")
                else:
                    fig = plt.figure(data_filename.split('/')[-1] + " - Calibration rails")
                plt.clf()

        #Update/Create Stacked plots
        for x in xrange(1, len(data_file_content_parsed)):
            if config_file_content_parsed[x - 1][-1] == 'P':
                fig = plt.figure(data_filename.split('/')[-1] + " - Power")
                ax = fig.add_subplot(111)
                ax.set_ylabel('Power [W]')
            elif config_file_content_parsed[x - 1][-1] == 'I':
                fig = plt.figure(data_filename.split('/')[-1] + " - Current")
                ax = fig.add_subplot(111)
                ax.set_ylabel('Current [A]')
            elif config_file_content_parsed[x - 1][-1] == 'V':
                fig = plt.figure(data_filename.split('/')[-1] + " - Voltage")
                ax = fig.add_subplot(111)
                ax.set_ylabel('Voltage [V]')
            elif (config_file_content_parsed[x - 1][-2] == 'S') & (config_file_content_parsed[x - 1][-1] == 'R'):
                fig = plt.figure(data_filename.split('/')[-1] + " - Voltage across sense resistor")
                ax = fig.add_subplot(111)
                ax.set_ylabel('Voltage [V]')
            else:
                fig = plt.figure(data_filename.split('/')[-1] + " - Calibration rails")
                ax = fig.add_subplot(111)
                ax.set_ylabel('Voltage [V]')
            plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
            ax.set_xlabel('Time [s]')
            if FN_enable[0]:
                ax.set_title(figure_name[0])
            else:
                ax.set_title(data_filename.split('/')[-1])
            plt.plot(data_file_content_parsed[0], data_file_content_parsed[x], color=np.random.rand(3),
                     label=config_file_content_parsed[x - 1])
            legend = plt.legend()
            legend.draggable()
    return

def data_average(data_file_content_parsed_col):
    if type(data_file_content_parsed_col) is not list:  # Moving average calls this function and with data_file_content_parsed_col being a list
        ''' Deprecated. Revert if errors occur
        max = min = avg = data_file_content_parsed_col.iloc[0][0]
        for x in xrange(0, len(data_file_content_parsed_col)):
            cur_point = data_file_content_parsed_col.iloc[x][0]  # to avoid calling iloc three times
            avg = avg * 1.0 * x / (x + 1) + cur_point * 1.0 / (x + 1)
            if cur_point > max:
                max = cur_point
            if cur_point < min:
                min = cur_point
        '''
        sum = data_file_content_parsed_col.sum()
        avg = sum/len(data_file_content_parsed_col)
        avg = avg[0]
        #Finds max
        max = data_file_content_parsed_col.max()[0]
        #Finds min
        min = data_file_content_parsed_col.min()[0]
    else: #Can optimize this by using df functions (change moving average function to using dataframes)
        max = min = avg = data_file_content_parsed_col[0]
        for x in xrange(0, len(data_file_content_parsed_col)):
            cur_point = data_file_content_parsed_col[x]
            avg = avg * 1.0 * x / (x + 1) + cur_point * 1.0 / (x + 1)
            if cur_point > max:
                max = cur_point
            if cur_point < min:
                min = cur_point
    return (max, min, avg)

def data_moving_average(data_file_content_parsed, config_file_content_parsed, MVinterval, MVstep):
    data_content_MV = []  # store final MVed data points of all rails
    data_content_MV_singlerail = []  # store final MVed data points of one rail
    sampleperiod = data_file_content_parsed[0].iloc[len(data_file_content_parsed[0]) - 1][0] - \
                   data_file_content_parsed[0].iloc[len(data_file_content_parsed[0]) - 2][0]
    MVinterval_row = int(np.ceil(MVinterval / sampleperiod))
    MVstep_row = int(np.ceil(MVstep / sampleperiod))
    MVcenter_row = int(np.ceil(MVinterval_row / 2.0))  # keep track of center point of one interval

    for z in xrange(0, len(config_file_content_parsed) + 1):
        data_content_MV_singlerail = []
        MVcurrent_row = 0  # keep track of start point of current interval
        x = 0  # number of steps taken
        while (x * MVstep_row + MVinterval_row <= len(data_file_content_parsed[0])):
            data_content_MV_singleinterval = []
            MVcurrent_row = x * MVstep_row

            for y in xrange(MVcurrent_row, MVcurrent_row + MVinterval_row):
                data_content_MV_singleinterval.append(data_file_content_parsed[z].iloc[y][0])
            data_content_MV_singlerail.append(reduce(lambda a, b: a + b,
                                                     data_content_MV_singleinterval) / MVinterval_row)  # takes average of data_content_MV_singleinterval
            # data_content_MV_singlerail.append(data_average(data_file_content_parsed, MVcurrent_row, MVcurrent_row+MVinterval_row, z))#takes average of data_content_MV_singleinterval
            x = x + 1
        data_content_MV.append(data_content_MV_singlerail)

    return data_content_MV

def avg_write(avg_filename, config_file_content_parsed, data_file_content_parsed):
    avg_file = open(avg_filename, "w")
    avg_file.write("rails, max, min, avg\n")
    for x in xrange(1, len(data_file_content_parsed)):
        (max, min, avg) = data_average(data_file_content_parsed[x])
        avg_file.write("%s, %s, %s, %s\n" % (config_file_content_parsed[x - 1], max, min, avg))
    avg_file.close()
    return

#Used to debug
def print_to_csv(temp, filename):
    file = open(filename + ".csv", "w")
    file.write("%s\n" % temp)
    file.close()

# def handler(msg_type, msg_string):
    # pass

# QtCore.qInstallMsgHandler(handler)

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    #ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()