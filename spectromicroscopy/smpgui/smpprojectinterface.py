"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import sys
import time
import weakref

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy import smpConfig
from spectromicroscopy.smpgui.ui_smpspecinterface import Ui_SmpSpecInterface
from spectromicroscopy.smpgui import configuresmp, scananalysis, scancontrols
from spectromicroscopy.smpcore import specrunner, configutils, qtspecscan, \
    qtspecvariable
from SpecClient import SpecClientError

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SmpSpecInterface(Ui_SmpSpecInterface, QtGui.QWidget):
    """Establishes a Experimenbt controls 
    Generates Control and Feedback instances
   Addes Scan atributes to specRunner instance 
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self.parent = parent
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        
        self.connectToSpec()
        self.pymcaConfigFile = configutils.getDefaultPymcaConfigFile()

        self.scanControls = scancontrols.ScanControls(self)

        self.gridlayout.addWidget(self.scanControls,0,0,1,1)

        self.connect(self.specRunner.scan, 
                     QtCore.SIGNAL("newMesh(PyQt_PyObject)"),
                     self.newScanAnalysis2D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newTseries(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newAscan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newA2scan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newA3scan(PyQt_PyObject)"),
                     self.newScanAnalysis1D)
        self.connect(self.specRunner.scan,
                     QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                     self.setTabLabel)

    def close(self):
        self.specRunner.close()
        return QtGui.QWidget.close(self)

    def connectToSpec(self):
        specVersion = self.getSpecVersion()
        try:
            self.window().statusBar().showMessage('Connecting')
            QtGui.qApp.processEvents()
            self.specRunner = specrunner.SpecRunner(specVersion, timeout=500)
            self.specRunner.scan = \
                qtspecscan.QtSpecScanMcaA(self.specRunner.specVersion)
            self.window().statusBar().clearMessage()
        except SpecClientError.SpecClientTimeoutError:
            self.connectionError(specVersion)
            raise SpecClientError.SpecClientTimeoutError

    def connectionError(self, specVersion):
        error = QtGui.QErrorMessage()
        server, port = specVersion.split(':')
        error.showMessage('''\
        SMP was unabel to connect to the "%s" spec instance at "%s". Please \
        make sure you have started spec in server mode (for example "spec \
        -S").'''%(port, server))
        error.exec_()

    def getPymcaConfigFile(self):
        dialog = QtGui.QFileDialog(self, 'Load PyMca Config File')
        dialog.setFilter('PyMca config files (*.cfg)')
        self.pymcaConfigFile = str(dialog.getOpenFileName())

    def getSpecVersion(self):
        return ':'.join([smpConfig['session']['server'],
                         smpConfig['session']['port']])

    def newScanAnalysis(self, newAnalysis):
        self.parent.mainTab.addTab(newAnalysis, '')
        self.parent.mainTab.setCurrentWidget(newAnalysis)

    def newScanAnalysis1D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis1D(self, scanParams))

    def newScanAnalysis2D(self, scanParams):
        self.newScanAnalysis(scananalysis.ScanAnalysis2D(self, scanParams))

    def setTabLabel(self, scanParams):
        i = self.parent.mainTab.currentIndex()
        self.parent.mainTab.setTabText(i, scanParams['title'])


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = SmpProjectInterface()
    myapp.show()
    sys.exit(app.exec_())