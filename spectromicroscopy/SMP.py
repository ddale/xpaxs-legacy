# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SMP.ui'
#
# Created: Thu Jul 05 20:08:00 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(QtCore.QSize(QtCore.QRect(0,0,701,656).size()).expandedTo(Main.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(Main)
        self.centralwidget.setObjectName("centralwidget")

        self.Tabby = QtGui.QTabWidget(self.centralwidget)
        self.Tabby.setGeometry(QtCore.QRect(0,0,701,631))
        self.Tabby.setObjectName("Tabby")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.Tabby.addTab(self.tab,"")
        Main.setCentralWidget(self.centralwidget)

        self.Bar = QtGui.QMenuBar(Main)
        self.Bar.setGeometry(QtCore.QRect(0,0,701,28))
        self.Bar.setObjectName("Bar")
        Main.setMenuBar(self.Bar)

        self.retranslateUi(Main)
        self.Tabby.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        Main.setWindowTitle(QtGui.QApplication.translate("Main", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabby.setTabText(self.Tabby.indexOf(self.tab), QtGui.QApplication.translate("Main", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
