print('- OceanOptics Spectra - the Python Suite')
print('Initializing....')

ncount=11
def ProgressBar(i=0,n=ncount,label='importing modules...'):
    from sys import stdout
    i=ProgressBar.counter
    p= int((i/(n))*20)
    pbar = p*'%'+(20-p)*'-'+' '
    stdout.write('\r'+label+": "+pbar)
    ProgressBar.counter+=1
    stdout.flush()
ProgressBar.counter=0
import sys
ProgressBar()
from os import linesep,path
ProgressBar()
from os.path import isdir
ProgressBar()
from PyQt4 import QtGui
ProgressBar()
from PyQt4.QtCore import QTimer
ProgressBar()
from numpy import linspace,zeros,abs,array,savetxt,transpose,genfromtxt
ProgressBar()
# from time import sleep,time
import time
from datetime import datetime
ProgressBar()
from class_Maya import *
ProgressBar()
from pyqtgraph.Qt import QtGui, QtCore
ProgressBar()
import pyqtgraph as pg
ProgressBar()
from io import BytesIO
ProgressBar()
from threading import Thread
ProgressBar()


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None, width=10, height=6):
        super(Window, self).__init__(parent)
        self.setWindowTitle("OceanOptics SpectraPySuite")
        self.move(200,200)
        self.status = QtGui.QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage('OceanOptics SpectraPySuite')
#-Initializing menus
    #File
        self.menu_file = QtGui.QMenu('&File', self)
        self.menuBar().addMenu(self.menu_file)
        self.savespec = self.menu_file.addAction('&Save', self.save_screen)
        self.loadspec = self.menu_file.addAction('&Load spectrum from .txt file', self.load_spectrum)
        self.menu_file.addAction('&Quit', QtCore.QCoreApplication.instance().quit)

    #Help
        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction('&About', self.about)
        self.help_menu.addAction('&Help', self.helps)
#-Initializing widgets
        self.main = QtGui.QWidget(self)

        self.toolbar_1 = QtGui.QFrame(self.main)
        self.toolbar_1.setStyleSheet("QFrame {background: rgb(255, 255, 255); }")

#
        self.toolbar_2 = QtGui.QFrame(self.main)
        self.toolbar_2.setStyleSheet("QFrame {margin:0px; background: rgb(255, 255, 255); }")

        self.toolbar_3 = QtGui.QFrame(self.main)
        self.toolbar_3.setStyleSheet("QFrame {margin:0px; background: rgb(255, 255, 255); }")

        self.frame_integ = QtGui.QFrame(self.main)
        self.frame_integ.setStyleSheet("QFrame {margin:0px; background: rgb(255, 255, 255); }")#{margin:1px; border:1px solid rgb(0, 0, 0); }")

        self.label_device = QtGui.QLabel('Starting')

        self.qlbl_integ = QtGui.QLabel('Integration time (ms):')
        self.qlbl_avg = QtGui.QLabel('Number of averages:')


        self.label_integ = QtGui.QLineEdit('10')
        self.label_avg = QtGui.QLineEdit('1')
        self.correc_dark = QtGui.QCheckBox('correct dark counts')
        self.correc_nonlinear = QtGui.QCheckBox('correct nonlinearity')
        self.correc_dark.setChecked(True)
        self.correc_nonlinear.setChecked(True)
        self.label_integ.editingFinished.connect(self.setIntTime)
        self.label_avg.editingFinished.connect(self.setAvg)
        self.label_maxcts = QtGui.QLineEdit('60000')


        self.but_freerun = QtGui.QPushButton('Free run')
        self.but_freerun.clicked.connect(self.free_run)

        self.but_stop = QtGui.QPushButton('stop')
        self.but_stop.clicked.connect(self.scan_stop)

        self.but_dark = QtGui.QPushButton('Take dark')
        self.but_dark.clicked.connect(self.take_dark)
        self.but_dark.setEnabled(False)

        self.save_folder = QtGui.QPushButton('Folder')
        self.save_folder.clicked.connect(self.ask_folder)
        self.save_name = QtGui.QLineEdit('sample name')


        self.but_savespec = QtGui.QPushButton('Save')
        self.but_savespec.clicked.connect(self.save_screen)
        self.but_savespec.setEnabled(False)

        self.but_scantime = QtGui.QPushButton('Integrate\nin time')
        self.but_scantime.clicked.connect(self.scan_time)
        self.but_scantime.setEnabled(False)

        self.plot_log = QtGui.QPushButton('Semilog Y')
        self.plot_log.setCheckable(True)
        self.plot_cps = QtGui.QPushButton('Plot CPS')
        self.plot_cps.setCheckable(True)
        self.plot_dark = QtGui.QPushButton('Subtract dark')
        self.plot_dark.setCheckable(True)
        self.plot_dark.setChecked(True)
        self.snapshot = QtGui.QPushButton('Snapshot')
        self.snapshot.setCheckable(True)
        self.snapshot.clicked.connect(self.take_snapshot)
        self.auto_range = QtGui.QPushButton('Auto range')
        self.auto_range.clicked.connect(self.set_autorange)

        self.auto_integration = QtGui.QPushButton('Auto integration')
        self.auto_integration.setCheckable(True)

        self.qlbl_counts = QtGui.QLabel('Counts')
        self.qlbl_progress = QtGui.QLabel(20*'\u25a1')
        self.qlbl_progress.setStyleSheet("QLabel {margin:0px ; background: rgb(255, 255, 255); font-style: consolas}")
        self.qlbl_progress.setFixedWidth(200)

        self.lim_wl1 = QtGui.QLineEdit('400')
        self.lim_wl2 = QtGui.QLineEdit('800')
        self.step = QtGui.QLineEdit('5')


#-Setting the layout (row, column, rowspan, columnspan)
        layout = QtGui.QGridLayout(self.main)
        layout_1 = QtGui.QGridLayout(self.toolbar_1)
        layout_2 = QtGui.QGridLayout(self.toolbar_2)
        layout_3 = QtGui.QGridLayout(self.toolbar_3)
        layout_integ = QtGui.QGridLayout(self.frame_integ)

        layout.addWidget(self.label_device,1,1,1,10)

        layout_1.addWidget(self.qlbl_integ,1,1,1,1)
        layout_1.addWidget(self.label_integ,1,2,1,1)
        self.label_integ.setValidator(QtGui.QDoubleValidator())
        self.label_integ.setFixedWidth(50)
        layout_1.addWidget(self.qlbl_avg,2,1,1,1)
        layout_1.addWidget(self.label_avg,2,2,1,1)
        self.label_integ.setValidator(QtGui.QDoubleValidator())
        self.label_avg.setFixedWidth(50)
        layout_1.addWidget(self.correc_dark,1,3,1,1)
        layout_1.addWidget(self.correc_nonlinear,2,3,1,1)
        self.toolbar_1.setLayout(layout_1)
        layout.addWidget(self.toolbar_1,2,1,2,1)

#        layout_1.addWidget(self.frame_integ,1,4,2,2)
        layout_integ.addWidget(self.auto_integration,1,1,1,2)
        layout_integ.addWidget(QtGui.QLabel('Max Counts:'),2,1,1,1)
        layout_integ.addWidget(self.label_maxcts,2,2,1,1)
        self.label_maxcts.setValidator(QtGui.QDoubleValidator())
        self.label_maxcts.setFixedWidth(50)

        self.frame_integ.setLayout(layout_integ)
        layout.addWidget(self.frame_integ,2,2,2,1)
        self.toolbar_1.setFixedWidth(400)
        self.frame_integ.setFixedWidth(150)
#        self.toolbar_1.setFixedHeight(80)


        layout_3.addWidget(QtGui.QLabel('WL1') ,1,1,1,1)
        layout_3.addWidget(self.lim_wl1,1,2,1,1)
        self.lim_wl1.setValidator(QtGui.QDoubleValidator())
        self.lim_wl1.setFixedWidth(50)
        layout_3.addWidget(QtGui.QLabel('WL2') ,2,1,1,1)
        layout_3.addWidget(self.lim_wl2,2,2,1,1)
        self.lim_wl2.setValidator(QtGui.QDoubleValidator())
        self.lim_wl2.setFixedWidth(50)
        layout_3.addWidget(self.but_scantime,1,3,2,1)
        self.but_scantime.setFixedWidth(70)
        self.but_scantime.setFixedHeight(60)
        self.toolbar_3.setLayout(layout_3)
        layout.addWidget(self.toolbar_3,2,3,2,1)

        size_plot_buttons = 90
        layout_2.addWidget(self.plot_log,1,1,1,1)
        self.plot_log.setFixedWidth(size_plot_buttons)
        self.plot_log.clicked.connect(self.trigger_update)
        layout_2.addWidget(self.plot_cps,1,2,1,1)
        self.plot_cps.clicked.connect(self.trigger_update)
        self.plot_cps.setFixedWidth(size_plot_buttons)
        layout_2.addWidget(self.plot_dark,1,3,1,1)
        self.plot_dark.setFixedWidth(size_plot_buttons)
        layout_2.addWidget(self.snapshot,1,4,1,1)
        self.snapshot.setFixedWidth(size_plot_buttons)
        layout_2.addWidget(self.auto_range,1,5,1,1)
        self.auto_range.setFixedWidth(size_plot_buttons)
        layout_2.addWidget(self.qlbl_counts,1,11,1,1)
        layout_2.addWidget(self.qlbl_progress,1,15,1,1)
        layout.addWidget(self.toolbar_2,18,1,1,12)

        self.toolbar_1.setFixedWidth(400)
        # self.toolbar_2.setFixedWidth(200)
        self.toolbar_3.setFixedWidth(200)


        self.save_folder.setFixedWidth(300)
        self.save_name.setFixedWidth(200)
        # self.save_spec.setFixedWidth(300)
#        self.toolbar_2.setFixedHeight(60)


        layout.addWidget(self.but_freerun,2,10,2,1)
        self.but_freerun.setFixedHeight(60)

        layout.addWidget(self.but_dark,2,11,2,1)
        self.but_dark.setFixedHeight(60)

        layout.addWidget(self.save_folder,1,10,1,2)
        layout.addWidget(self.save_name,1,12,1,1)
        layout.addWidget(self.but_savespec,2,12,2,1)
        self.but_savespec.setFixedHeight(60)

        self.main.setLayout(layout)
        self.setCentralWidget(self.main)


        self.graph = pg.PlotWidget(name='Spectrum',background=(255,255,255))
        layout.addWidget(self.graph,4,1,12,12)

        pg.setConfigOptions(antialias=True)
        self.spectrum = self.graph.plot(pen='r',width=2,fillLevel=0, brush=(255,220,220))
        self.snapspec = self.graph.plot(pen='k',width=2)
        self.graph.setLabel('bottom', "Wavelength", units='nm')
        self.graph.setLabel('left', "Counts")
        self.graph.showGrid(x=True, y=True)


        self.maya = Maya()
        self.running=False
        self.timeplot=False
        self.update_display = False
        self.path=0
#        self.auto_integration=True
        self.cts = 0
        self.progress = 0
#
        self.x_data = linspace(400,700,500)
        self.y_data = zeros(500)
        self.saved_snapshot = []
        self.connect()
        self.initialize()
#

    def data_listener(self):
        while True:
            if self.running:
                self.maya.corr_dark = self.correc_dark.isChecked()
                self.maya.corr_nonlinear = self.correc_nonlinear.isChecked()
                if self.timeplot:
                    self.x_data = []
                    self.y_data = []
                    name = 'Spectrometer: %s' %self.maya.name
                    integration = 'Integration time (ms): %d' %self.maya.int_time
                    average = 'Number of averages: %d' %self.maya.avg
                    head= name+linesep+integration+linesep+average+linesep+'Wavelength (nm) \t Counts'+linesep
                    now = time.time()
                    while self.timeplot:
                        self.maya.Acquire()
                        self.x_data.append(time.time()-now)
                        self.y_data.append(sum(self.maya.y_data[self.i1:self.i2]))
                        # self.save_spectrum(self.path+'_'+str(len(self.x_data)+1)+'.txt',self.maya.x_data,self.maya.y_data)
                        # filedata = array([self.x_data,self.y_data])
                        filedata = array([self.maya.x_data,self.maya.y_data])
                        pathstr = self.path+'_'+str(len(self.x_data)+1)+'.txt'
                        savetxt(pathstr,transpose(filedata),delimiter='\t',header=head,comments='',newline=linesep)

                else:
                    self.maya.Acquire()
                    self.x_data=(self.maya.x_data)
                    if self.plot_dark.isChecked():
                        self.y_data=(self.maya.y_data)
                    else:
                        self.y_data=(self.maya.raw_y_data)

                    if len(self.maya.raw_y_data):
                        self.cts = max(self.maya.raw_y_data)

                    # if self.auto_integration.isChecked():
                    #     while self.cts>int(self.label_maxcts.text()):
                    #         if self.maya.int_time<=8:
                    #             print('Warning!!! Detector saturating!!')
                    #             break
                    #         print(self.maya.int_time)
                    #         self.maya.setIntegrationTime(self.maya.int_time-10)
                    #         self.label_integ.setText(str(self.maya.int_time))
                    #         self.maya.Acquire()
                    #         self.x_data=(self.maya.x_data)
                    #         self.y_data=(self.maya.y_data)
                    #         self.cts = max(self.maya.raw_y_data)
            else:
                time.sleep(0.5)

    def ProgressBar(self,i,n):
        # if n>1000 and (i/10 - int(i/10))!=0:
        #     return
        # if n>
        p= int((i/(n))*20)
        pbar = p*'\u25a0'+(20-p)*'\u25a1'
        if len(pbar)>20:
            pbar = 20*'\u25a0'
        return pbar
# print('\u25a0')
    def update(self):
        if self.running:
            if self.maya.int_time*self.maya.avg>500:
                 self.qlbl_progress.setText(self.ProgressBar(self.maya.progress,self.maya.acqtime))
            else:
                self.qlbl_progress.setText(20*'\u25a0')
            if self.update_display:
                if self.timeplot:
                    self.graph.setLabel('bottom', "Time",units='s')
                    # self.graph.autoRange()
                else:
                    self.graph.setLabel('bottom', "Wavelength", units='nm')

                if self.plot_cps.isChecked():
                    self.graph.setLabel('left', "Counts Per Second")
                    self.y_data = self.y_data / (self.maya.int_time/1000)
                else:
                    self.graph.setLabel('left', "Counts")

                if self.plot_log.isChecked():
                    self.graph.setLogMode(x=False, y=True)
                else:
                    self.graph.setLogMode(x=False, y=False)
                self.update_display = False

            self.spectrum.setData(self.x_data,self.y_data)
            self.qlbl_counts.setText('Max Counts: %i' %self.cts)
        # else:
        #     if self.plot_cps.isChecked():
        #         self.graph.setLabel('left', "Counts Per Second")
        #         self.y_data = self.y_data / (self.maya.int_time/1000)
        #     else:
        #         self.graph.setLabel('left', "Counts")
        #
        #     if self.plot_log.isChecked():
        #         self.graph.setLogMode(x=False, y=True)
        #     else:
        #         self.graph.setLogMode(x=False, y=False)
        #     self.spectrum.setData(self.x_data,self.y_data)
        #     self.qlbl_counts.setText('Max Counts: %i' %self.cts)

    def connect(self):
        self.maya.connect()
#
    def initialize(self):
        self.status.showMessage('Initializing...')

        self.thread_scan = Thread(target=self.data_listener)
        self.thread_scan.daemon=True
        self.thread_scan.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0.01)
        # sleep(0.02)

        if self.maya.connected:
            self.setIntTime()
            self.label_device.setText('Spectrometer: '+self.maya.name)
            self.status.showMessage('Ready! Spectrometer connected, press free run to start acquisition.')
#        self.free_run()
        else:
            self.label_device.setText('Spectrometer not connected - Simulation mode')
            self.status.showMessage('No device connected, running with virtual spectrometer. Press free run to start simulated acquisition.')

        try:
            if getattr(sys, 'frozen', False):
                # cwd = sys._MEIPASS
                cwd=path.dirname(sys.executable)
            else:
                cwd = path.dirname(path.abspath(__file__))
            pixels = genfromtxt(cwd+'\\'+'burnt_pixels.txt',dtype='float',usecols=0)
            self.maya.burnt_pixels=zeros(len(pixels))
            wl=self.maya.getWL()
            print('Burnt pixels: '+str(pixels))
            for i in range(len(pixels)):
                self.maya.burnt_pixels[i]=abs(wl - pixels[i]).argmin()
        except:
            self.maya.burnt_pixels=[]
###


    def setIntTime(self):
#        if self.maya.connected:
        int_time = int(self.label_integ.text())
        self.maya.setIntegrationTime(int_time)

    def setAvg(self):
        # if self.maya.connected:
        avg = (self.label_avg.text())
        if avg: self.maya.avg = int(avg)

    def free_run(self):
#        if self.maya.connected:
        self.running = not self.running
        if self.running:
            self.update_display=True
            # self.graph.enableAutoRange()
            self.but_scantime.setEnabled(True)
            self.but_dark.setEnabled(True)
            self.but_savespec.setEnabled(True)
            self.but_freerun.setText('Pause')
            self.status.showMessage('Live! tip: right-click and drag to zoom the graph.')
        else:
            self.but_freerun.setText('Free run')
            self.status.showMessage('Paused.')

    def take_snapshot(self):
        if self.snapshot.isChecked():
            self.saved_snapshot = self.y_data
            self.snapspec.setData(self.x_data,self.saved_snapshot)
            self.status.showMessage('Live! Showing snapshot taken at %s' %datetime.now().strftime('%H:%M:%S'))
        else:
            self.snapspec.setData([],[])
            self.status.showMessage('Live! tip: right-click and drag to zoom the graph.')


    def load_spectrum(self):
        pathstr = QtGui.QFileDialog.getOpenFileName(filter='*.txt')
        if pathstr:
            if self.snapshot.isChecked():
                self.snapshot.setChecked(False)
                self.snapspec.setData([],[])

            for headerlines in range(1,20):
                try:
                    preread = open(pathstr).read().replace(',','.')
                    load_x = genfromtxt(BytesIO(preread.encode()),dtype='float',
                                         delimiter='\t',skip_header=headerlines,skip_footer=1,
                                         usecols=0)
                    load_y = genfromtxt(BytesIO(preread.encode()),dtype='float',
                                     delimiter='\t',skip_header=headerlines,skip_footer=1,
                                     usecols=1)
                    self.snapspec.setData(load_x,load_y)
                    if self.running:
                        self.status.showMessage('Live! Showing spectrum loaded from %s' %pathstr)
                    else:
                        self.status.showMessage('Showing spectrum loaded from %s' %pathstr)
                    loaded=True
                    break;
                except:
                    loaded=False
            if not loaded:
                QtGui.QMessageBox.information(self, "Error",'Failed to load file.')



    def scan_stop(self):
        self.running=False
        self.status.showMessage('Paused')
        self.but_freerun.setText('Free run')

    def scan_time(self):
        if self.timeplot:
            self.timeplot = False
            self.running=False
            self.but_scantime.setText('Integrate\nin time')
            self.but_freerun.setText('Free run')
            self.but_freerun.setEnabled(True)
            self.status.showMessage('Paused.')
            self.save_timeplot(self.path)
        else:
            path = self.ask_path()[:-4]
            if path:
                self.path = path
                self.i1 = abs(self.maya.x_data - int(self.lim_wl1.text())).argmin()
                self.i2 = abs(self.maya.x_data - int(self.lim_wl2.text())).argmin()
                self.but_scantime.setText('Stop')
                self.but_freerun.setEnabled(False)
                self.status.showMessage('Scanning...')
                self.graph.enableAutoRange()
                self.timeplot = True
                self.update_display=True
                self.running=True
                # time.sleep(1)

    def set_autorange(self):
        self.graph.autoRange()
    def trigger_update(self):
        self.update_display = True

    def take_dark(self):
        if self.maya.connected:
            self.maya.getBaseline()

    def save_screen(self):
        if not self.save_name.text():
            path = self.ask_path()
        else:
            if isdir(self.save_folder.text()):
                path = self.save_folder.text()+'/'+self.save_name.text()+'.txt'
            else:
                QtGui.QMessageBox.information(self, "Error","Please enter a valid folder.")
                folder = QtGui.QFileDialog.getExistingDirectory(self, "Select Folder")
                if folder:
                    self.save_folder.setText(folder)
                    path = self.save_folder.text()+'/'+self.save_name.text()+'.txt'
                else:
                    path=False
        if path:
            self.save_spectrum(path)

    def ask_path(self):
        pathstr = QtGui.QFileDialog.getSaveFileName(filter='*.txt')
        return pathstr

    def ask_folder(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.save_folder.setText(folder)

    def save_spectrum(self,pathstr,x=[],y=[]):
        if not len(x):
            x = self.x_data
        if not len(y):
            y = self.y_data

        file = array([x,y])
        name = 'Spectrometer: %s' %self.maya.name
        integration = 'Integration time (ms): %d' %self.maya.int_time
        average = 'Number of averages: %d' %self.maya.avg
        head= name+linesep+integration+linesep+average+linesep+'Wavelength (nm) \t Counts'+linesep
        try:
            savetxt(pathstr,transpose(file),delimiter='\t',header=head,comments='',newline=linesep)
            QtGui.QMessageBox.information(self, "Saved","Spectrum saved at "+pathstr)
        except:
            QtGui.QMessageBox.information(self, "Error","File not saved")

    def save_timeplot(self,pathstr,x=[],y=[]):
        if not len(x):
            x = self.x_data
        if not len(y):
            y = self.y_data
        file = array([x,y])
        name = 'Spectrometer: %s \n' %self.maya.name
        integration = 'Integration time (ms): %d\n' %self.maya.int_time
        average = 'Number of averages: %d\n' %self.maya.avg
        head= name+linesep+integration+linesep+average+linesep+'Time (s) \t Integrated counts \n'+linesep
        savetxt(pathstr+'_timeplot.txt',transpose(file),delimiter='\t',header=head,comments='',newline=linesep)

    def about(self):
        QtGui.QMessageBox.about(self, "About",
                                "It's a work in progress!"
                                )

    def helps(self):
        ParamDialog = QtGui.QDialog(self)
        ParamDialog.setWindowTitle("Help")
        ParamDialog.resize(700,300)
        ParamDialog.move(300,300)
        from help_text import helpstr
        # helpstr = ''
        ps = QtGui.QLabel(helpstr)
        scroll = QtGui.QScrollArea()
        scroll.setWidget(ps)
        vL = QtGui.QVBoxLayout(ParamDialog)
        vL.addWidget(scroll)
        ParamDialog.show()

# print('boh')
if __name__ == '__main__':

    print('\n\nStarting app')
    app = QtGui.QApplication(sys.argv)
    # print('\n\nStarting app')

    main = Window()
    main.show()

    app.exec_()
