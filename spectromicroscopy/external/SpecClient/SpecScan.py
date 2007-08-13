"""Helper module for managing scans"""
import SpecConnectionsManager
import SpecEventsDispatcher
import SpecWaitObject
import logging
import types
import time

__author__ = 'Matias Guijarro'
__version__ = 1


(TIMESCAN) = (16)


class SpecScanA:
    def __init__(self, specVersion = None):
        self.scanParams = {}
        self.scanCounterMne = None
        self.__scanning = False

        if specVersion is not None:
            self.connectToSpec(specVersion)
        else:
            self.connection = None
        

    def connectToSpec(self, specVersion):
        self.connection = SpecConnectionsManager.SpecConnectionsManager().getConnection(specVersion)
        SpecEventsDispatcher.connect(self.connection, 'connected', self.connected)
        SpecEventsDispatcher.connect(self.connection, 'disconnected', self.__disconnected)

        self.connection.registerChannel('var/_SC_NEWSCAN', self.__newScan)
        self.connection.registerChannel('var/_SC_SCANDATALINE', self.__newScanPoint, dispatchMode=SpecEventsDispatcher.FIREEVENT)
                    
        if self.connection.isSpecConnected():
            self.connected()


    def isConnected(self):
        return self.connection and self.connection.isSpecConnected()

        
    def connected(self):
        pass


    def __disconnected(self):
        self.scanCounterMne = None
        self.__scanning = False
        self.scanParams = {}
        
        self.disconnected()

        
    def disconnected(self):
        pass
                            

    def __newScan(self, newscan):
        if not newscan:
            if self.__scanning:
                self.scanFinished()
                self.__scanning = False
            return

        self.__scanning = False
            
        self.scanParams = SpecWaitObject.waitReply(self.connection, 'send_msg_chan_read', ('var/_SC_SCANENV', ))

        if type(self.scanParams) != types.DictType:
            return

        self.newScan(self.scanParams)

        self.scanCounterMne = self.scanParams['counter']
        if len(self.scanCounterMne) == 0 or self.scanCounterMne == '?':
            logging.getLogger("SpecClient").error("No counter selected for scan.")
            self.scanCounterMne = None
            return
                
        self.__scanning = True
        self.scanStarted() # A.B
                

    def getScanType(self):
        try:
            return self.scanParams['scantype']
        except KeyError:
            return -1
        
                       
    def newScan(self, scanParameters):
        #print scanParameters
        pass


    def __newScanPoint(self, scanDataString):       
        if self.__scanning:
            scanData = {}

            for elt in scanDataString.split():
                key, value = elt.split('=')
                if key=="i":
                  i=float(value)
                elif key=="x":
                  x=float(value)
                elif key==self.scanCounterMne:
                  y=float(value)
                  scanData[key]=float(value)
                else:
                  scanData[key]=float(value)

            # hack to know if we should call newScanPoint with
            # scanData or not (for backward compatiblity)
            if len(self.newScanPoint.im_func.func_code.co_varnames) > 4:
              self.newScanPoint(i, x, y, scanData)
            else:
              self.newScanPoint(i, x, y)
    
    
    def newScanPoint(self, i, x, y, counters_value):
        #print i, x, y, counters_value
        pass


    def scanFinished(self):
        pass


    def scanStarted(self): # A.B
        pass # A.B


    def ascan(self, motorMne, startPos, endPos, nbPoints, countTime):
        if self.connection.isSpecConnected():
            self.connection.send_msg_cmd("ascan %s %f %f %d %f" % (motorMne, startPos, endPos, nbPoints, countTime))
            return True
        else:
            return False









