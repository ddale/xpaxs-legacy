#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# GUI imports
#---------------------------------------------------------------------------

from xpaxs.instrumentation.spec.ui import ui_gamepad
from xpaxs.instrumentation.spec import TEST_SPEC
from xpaxs.instrumentation.spec.motorwidget import MotorWidget

#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class ScanBounds(object):

    @property
    def test(self):
        return 1

sb = ScanBounds()

print sb.test