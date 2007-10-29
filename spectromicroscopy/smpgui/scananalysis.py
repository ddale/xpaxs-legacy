"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# SMP imports
#---------------------------------------------------------------------------

from spectromicroscopy.smpgui import elementsdata, mcaspectrum, mplwidgets, \
    elementsplot
from spectromicroscopy.smpcore import advancedfitanalysis

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------

class ScanAnalysis(QtGui.QWidget):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.specInterface = parent
        
        self.gridlayout = QtGui.QGridLayout(self)
        
        self.setEnabled(False)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        
        self.scanAnalysis = None

        self.mcaSpectrumPlot = mcaspectrum.McaSpectrum()
        self.gridlayout.addWidget(self.mcaSpectrumPlot, 0, 0, 1, 1)
        
        self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        self.gridlayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.splitter.addWidget(self.mcaSpectrumPlot)
        self.connect(self.specInterface.specRunner.scan,
                     QtCore.SIGNAL("scanFinished()"),
                     self.disconnectSignals)
        self.connect(self.specInterface.specRunner.scan,
                     QtCore.SIGNAL("scanAborted()"),
                     self.disconnectSignals)

    def connectSignals(self):
        self.connect(self.elementDataPlot.dataTypeBox,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.scanAnalysis.setCurrentDataType)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("elementDataChanged(PyQt_PyObject)"),
                     self.elementDataPlot.updateFigure)
        self.connect(self.elementDataPlot.saveDataPushButton,
                     QtCore.SIGNAL("clicked()"),
                     self.saveData)
        self.connect(self.specInterface.specRunner.scan, 
                     QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"),
                     self.scanAnalysis.newDataPoint)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("newMcaFit(PyQt_PyObject)"),
                     self.mcaSpectrumPlot.updateFigure)
        self.connect(self.scanAnalysis, 
                     QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                     self.elementDataPlot.xrfbandComboBox.addItems)
        self.connect(self.elementDataPlot.xrfbandComboBox,
                     QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.scanAnalysis.setCurrentElement)
        self.connect(self.scanAnalysis,
                     QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                     self.setEnabled)
        self.connect(self.specInterface.specRunner.scan,
                     QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                     self.scanAnalysis.setSuggestedFilename)
        self.connect(self.specInterface.specRunner.scan, 
                     QtCore.SIGNAL("xAxisLabel(PyQt_PyObject)"),
                     self.elementDataPlot.setXLabel)
        self.connect(self.specInterface.specRunner.scan, 
                     QtCore.SIGNAL("xAxisLims(PyQt_PyObject)"),
                     self.elementDataPlot.setXLims)
        self.connect(self.specInterface.specRunner.scan, 
                     QtCore.SIGNAL("yAxisLabel(PyQt_PyObject)"),
                     self.elementDataPlot.setYLabel)
        self.connect(self.specInterface.specRunner.scan, 
                     QtCore.SIGNAL("yAxisLims(PyQt_PyObject)"),
                     self.elementDataPlot.setYLims)
        self.connect(self.scanAnalysis,
                     QtCore.SIGNAL('viewConcentrations(PyQt_PyObject)'),
                     self.viewConcentrations)
    
    def disconnectSignals(self):
        # workaround to process last data point, reported after scanFinished 
        # signal is emitted:
        self.mcaSpectrumPlot.configPyMcaButton.setEnabled(True)
        self.disconnect(self.specInterface.specRunner.scan, 
                        QtCore.SIGNAL("newScanPoint(PyQt_PyObject)"),
                        self.scanAnalysis.newDataPoint)
        self.disconnect(self.scanAnalysis, 
                        QtCore.SIGNAL("availablePeaks(PyQt_PyObject)"),
                        self.elementDataPlot.xrfbandComboBox.addItems)
        self.disconnect(self.scanAnalysis,
                        QtCore.SIGNAL("enableDataInteraction(PyQt_PyObject)"),
                        self.setEnabled)
        self.disconnect(self.specInterface.specRunner.scan,
                        QtCore.SIGNAL("newScan(PyQt_PyObject)"),
                        self.scanAnalysis.setSuggestedFilename)
        self.disconnect(self.specInterface.specRunner.scan, 
                        QtCore.SIGNAL("xAxisLabel(PyQt_PyObject)"),
                        self.elementDataPlot.setXLabel)
        self.disconnect(self.specInterface.specRunner.scan, 
                        QtCore.SIGNAL("xAxisLims(PyQt_PyObject)"),
                        self.elementDataPlot.setXLims)
        self.disconnect(self.specInterface.specRunner.scan, 
                        QtCore.SIGNAL("yAxisLabel(PyQt_PyObject)"),
                        self.elementDataPlot.setYLabel)
        self.disconnect(self.specInterface.specRunner.scan, 
                        QtCore.SIGNAL("yAxisLims(PyQt_PyObject)"),
                        self.elementDataPlot.setYLims)

    def viewConcentrations(self, val):
        text = 'Mass Fraction'
        cbox = self.elementDataPlot.dataTypeBox
        cur = cbox.findText(text)
        if val and (cur < 0): cbox.addItem(text)
        if not val and (cur >= 0): cbox.removeItem(cur)

    def saveData(self):
        suggested = self.scanAnalysis.getSuggestedFilename()
        filename = QtGui.QFileDialog.getSaveFileName(self,
                        'Save Element Data File', suggested,
                        'EDF files (*.edf);;Plaintext files (*.dat *.txt *.*)')
        if filename:
            self.scanAnalysis.saveData(str(filename))


class ScanAnalysis1D(ScanAnalysis):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None, scanParams={}):
        ScanAnalysis.__init__(self, parent)

        self.scanAnalysis = \
            advancedfitanalysis.AdvancedFitAnalysis1D(scanParams)
        
        self.elementDataPlot = elementsplot.ElementsPlot()
        self.gridlayout.addWidget(self.elementDataPlot, 2, 0, 1, 1)
        self.splitter.addWidget(self.elementDataPlot)
        
        self.connectSignals()
        self.scanAnalysis.loadPymcaConfig(self.specInterface.pymcaConfig)
        
    def connectSignals(self):
        ScanAnalysis.connectSignals(self)


class ScanAnalysis2D(ScanAnalysis):
    """Establishes a Experimenbt controls    """
    def __init__(self, parent=None, scanParams={}):
        ScanAnalysis.__init__(self, parent)
        
        self.scanAnalysis = \
            advancedfitanalysis.AdvancedFitAnalysis2D(scanParams)
        
        self.elementDataPlot = elementsdata.ElementsData()
        self.gridlayout.addWidget(self.elementDataPlot, 2, 0, 1, 1)
        self.splitter.addWidget(self.elementDataPlot)

        self.connectSignals()
        self.scanAnalysis.loadPymcaConfig(self.specInterface.pymcaConfig)

    def connectSignals(self):
        ScanAnalysis.connectSignals(self)
        self.connect(self.elementDataPlot.aspectSpinBox,
                     QtCore.SIGNAL("valueChanged(double)"),
                     self.elementDataPlot.setImageAspect)
