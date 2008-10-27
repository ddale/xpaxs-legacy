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
# xpaxs imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_skipmode

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class SkipModeWidget(ui_skipmode.Ui_SkipModeWidget, QtGui.QWidget):

    """Dialog for setting spec scan options"""

    def __init__(self, specRunner, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.specRunner = specRunner

        settings = QtCore.QSettings()
        settings.beginGroup("SkipModeOptions")

        val = settings.value('threshold', QtCore.QVariant(0)).toInt()[0]
        self.thresholdSpinBox.setValue(val)

        val = settings.value('precount', QtCore.QVariant(0)).toDouble()[0]
        self.precountSpinBox.setValue(val)

        counters = [''] + self.specRunner.getCountersMne()
        self.counterComboBox.addItems(counters)
        try:
            i = counters.index(settings.value('counter').toString())
            self.counterComboBox.setCurrentIndex(i)
        except ValueError:
            pass

    @QtCore.pyqtSignature("QString")
    def on_counterComboBox_currentIndexChanged(self, val):
        isEnabled = bool(val)
        self.thresholdSpinBox.setEnabled(isEnabled)
        self.thresholdLabel.setEnabled(isEnabled)
        self.precountSpinBox.setEnabled(isEnabled)
        self.precountLabel.setEnabled(isEnabled)

        self.configure(channel=val)

    @QtCore.pyqtSignature("double")
    def on_precountSpinBox_valueChanged(self, val):
        self.configure(precount=val)

    @QtCore.pyqtSignature("double")
    def on_thresholdSpinBox_valueChanged(self, val):
        self.configure(threshold=val)

    def closeEvent(self, event):
        settings = QtCore.QSettings()
        settings.beginGroup("SkipModeOptions")
        settings.setValue(
            'counter',
            QtCore.QVariant( str(self.counterComboBox.currentText()) )
        )
        settings.setValue(
            'threshold',
            QtCore.QVariant(self.thresholdSpinBox.value())
        )
        settings.setValue(
            'precount',
            QtCore.QVariant(self.precountSpinBox.value())
        )

        event.accept()

    def configure(self, channel=None, precount=None, threshold=None):
        if channel is None:
            channel = str(self.counterComboBox.currentText())

        if threshold is None:
            threshold = self.thresholdSpinBox.value()

        if precount is None:
            precount = self.precountSpinBox.value()

        if bool(precount) and bool(channel):
            self.specRunner(
                str("skipmode %s %s %s"%(precount, channel, threshold))
            )

        else:
            self.specRunner('skipmode 0')

    def setBusy(self, busy):
        self.setDisabled(busy)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('XPaXS')
    myapp = ScanControls()
    myapp.show()
    sys.exit(app.exec_())
