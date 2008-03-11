"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import os
import sys

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore
import tables

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


class TreeItem:
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def itemActivated(self):
        pass


class H5EntryItem(TreeItem):

    def __init__(self, scanData, mutex, parent):
        self.scanData = scanData

        self.mutex = mutex

        self.parentItem = parent
        self.childItems = []

        scannum = '%s'%self.scanData._v_attrs.scanNumber
        cmd = self.scanData._v_attrs.scanCommand
        numpoints = '%d'%self.scanData._v_attrs.scanLines
        self.itemData = [scannum, cmd, numpoints]

    def itemActivated(self):
        return self.scanData, self.mutex


class FileItem(TreeItem):

    def __init__(self, filename, parent):
        self.parentItem = parent
        self.itemData = [os.path.split(filename)[-1], '', '']
        self.childItems = []

        mutex = QtCore.QMutex()
        datafile = tables.openFile(filename, 'r+')

        for scan in datafile.root:
            self.appendChild(H5EntryItem(scan, mutex, self))


class H5FileModel(QtCore.QAbstractItemModel):

    """
    """

    def __init__(self, filename=None, parent=None):
        super(H5FileModel, self).__init__(parent)

        rootData = []
        rootData.append(QtCore.QVariant('File/Entry #'))
        rootData.append(QtCore.QVariant('Command'))
        rootData.append(QtCore.QVariant('Points'))
        self.rootItem = TreeItem(rootData)
        if filename: self.appendFile(filename)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = index.internalPointer()

        return QtCore.QVariant(item.data(index.column()))

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and \
                role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) \
                or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def appendFile(self, filename):
        # TODO: check if file has already been opened
        self.rootItem.appendChild(FileItem(filename, self.rootItem))
        row = self.rowCount(QtCore.QModelIndex())-1
        index = self.index(row, 0, QtCore.QModelIndex())
        self.emit(QtCore.SIGNAL('fileAppended'), index)

    def itemActivated(self, index):
        scanData, mutex = index.internalPointer().itemActivated()
        self.emit(QtCore.SIGNAL('scanActivated'), scanData, mutex)


if __name__ == "__main__":
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)

    model = SpecFileModel('ause_Hg_Se_5.mca')

    view = QtGui.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.connect(view,
                 QtCore.SIGNAL('activated(QModelIndex)'),
                 model.itemActivated)
    view.show()
    sys.exit(app.exec_())