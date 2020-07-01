from numpy import linspace, random, genfromtxt,zeros
from time import sleep
from os import path


#print(sp.list_devices())
#maya = sp.Spectrometer(sp.list_devices()[0])
#print(maya.model)
#maya.close()

class Maya():
    def __init__(self,parent=None):

        self.name = ''
        self.baseline = []
        self.avg= 1
        self.int_time = 1   # always in milisecond!!!
        self.x_data = []
        self.y_data = []
        self.raw_y_data = []
        self.connected = False
        self.instrument = 0
        self.corr_nonlinear=True
        self.corr_dark=True
        self.corr_burnt=True
        self.burnt_pixels=[]
        self.progress = 0
        self.acqtime = 0

    def __del__(self):
        if self.connected:
            self.instrument.close()

    def connect(self):
        try:
            import seabreeze.spectrometers as sp
            self.instrument = sp.Spectrometer(sp.list_devices()[0])
            self.name = self.instrument.model
            print(self.name)
            self.connected = True
        except:
            print('Spectrometer not connected')
            self.name = 'Virtual device'
        # self.getBurntPixels()

    # def getBurntPixels(self):
    #     try:
    #         cwd = path.dirname(__file__)
    #         pixels = genfromtxt(cwd+'\\'+'burnt_pixels.txt',dtype='float',usecols=0)
    #         self.burnt_pixels=zeros(len(pixels))
    #         wl=self.getWL()
    #         for i in range(len(pixels)):
    #             self.burnt_pixels[i]=abs(wl - pixels[i]).argmin()
    #     except:
    #         self.burnt_pixels=[]

    def getWL(self):
        if self.connected:
            wl = self.instrument.wavelengths()
        else: # virtual device
            wl= linspace(200,1100,1000)
        return wl

    def getData(self):
        if self.connected:
            try:
                try:
                    spec = self.instrument.intensities(correct_dark_counts=self.corr_dark,correct_nonlinearity=self.corr_nonlinear)
                except:
                    spec = self.instrument.intensities(correct_nonlinearity=self.corr_nonlinear)
            except:
                print('Data Transfer Error')        
        else: # virtual device
            spec=random.normal(size=1000)*self.int_time
            sleep(self.int_time/1000)
        if self.corr_burnt and len(self.burnt_pixels):
            for i in self.burnt_pixels:
                i=int(i)
                spec[i]=(spec[i-1]+spec[i+1])/2
        return spec

    def setIntegrationTime(self,new_inttime):
        self.int_time = new_inttime
        if self.connected:
            self.instrument.integration_time_micros(self.int_time*1000)

    def getBaseline(self):
        if self.connected:
#            self.baseline = self.getData()
#            for i in range(self.avg-1):
#                self.baseline=(self.baseline+self.getData()[1])
            self.baseline = self.raw_y_data#self.baseline / self.avg

    def Acquire(self):
        self.progress = 0
        self.acqtime = self.avg #* self.int_time/10
        wl = self.getWL()
        spec = self.getData()
        self.progress+=1
        for i in range(self.avg-1):
            spec=(spec+self.getData())
            self.progress+=1
        spec = spec / self.avg
        self.raw_y_data = spec
        self.y_data = spec
        self.x_data = wl
        if len(self.baseline):
            self.y_data= self.raw_y_data - self.baseline


#    def check_integration(self):
#        spec= self.instrument.intensities(correct_dark_counts=True,correct_nonlinearity=True)
#        while max(spec)>55000:
#            if self.int_time<=8:
#                print('Warning!!! Detector saturating!!')
#                break
#            self.int_time=self.int_time-10
#            self.setIntegrationTime(self.int_time)
#            spec= self.instrument.intensities(correct_dark_counts=True,correct_nonlinearity=True)
#
#        while max(spec)<1000:
#            if self.int_time>=1000: break
#            self.int_time=self.int_time+10
#            self.setIntegrationTime(self.int_time)
#            spec= self.instrument.intensities(correct_dark_counts=True,correct_nonlinearity=True)
