from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QTableWidgetItem, QWidget, QGridLayout, QFormLayout,
                             QPushButton,  QTextEdit, QLineEdit, QLabel, QTableWidget)

class mainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        mainGrid = QGridLayout()
        self.setElementTables()
        self.setTableTitles()
        self.setLayout(mainGrid)
        
        mainGrid.addWidget(self.dipolesTitle,      0, 0)
        mainGrid.addWidget(self.dipoleTable,       1, 0)
        mainGrid.addWidget(self.quadDupletTitle,   2, 0)
        mainGrid.addWidget(self.quadDuplet1Table,  3, 0)
        mainGrid.addWidget(self.quadDuplet2Table,  4, 0)
        mainGrid.addWidget(self.quadTripletTitle,  5, 0)#, 1, 2)
        mainGrid.addWidget(self.quadTriplet1Table, 6, 0)
        mainGrid.addWidget(self.quadTriplet2Table, 7, 0)

    def setTableTitles(self):

        self.dipolesTitle     = self.createTableTitle('DIPOLES')
        self.quadDupletTitle  = self.createTableTitle('QUADRUPOLE DUPLETS')
        self.quadTripletTitle = self.createTableTitle('QUADRUPOLE TRIPLETS')
        
    def setElementTables(self):
        
        dipolesInfo      = [['Name', 'Current [A]', 'B_ist [mT]', 'B_soll [mT]'],
                            ['Dipole1', 1., 0., 0.],
                            ['Dipole2', 2., 0., 0.]]
        quadDuplet1Info   = [['Name', 'Voltage [V]', 'K_mad', 'K_ist'],
                            ['Quad11', 11., 0., 0.],
                            ['Quad12', 12., 0., 0.]]
        quadDuplet2Info   = [['Name', 'Voltage [V]', 'K_mad', 'K_ist'],
                            ['Quad21', 11., 0., 0.],
                            ['Quad22', 12., 0., 0.]]
        quadTriplet1Info = [['Name', 'Voltage [V]', 'K_mad', 'K_ist'],
                            ['Quad31', 31., 0., 0.],
                            ['Quad32', 32., 0., 0.],
                            ['Quad33', 33., 0., 0.]]
        quadTriplet2Info = [['Name', 'Voltage [V]', 'K_mad', 'K_ist'],
                            ['Quad41', 41., 0., 0.],
                            ['Quad42', 42., 0., 0.],
                            ['Quad43', 43., 0., 0.]]

        self.dipoleTable       = self.createTable(dipolesInfo)
        self.quadDuplet1Table  = self.createTable(quadDuplet1Info)
        self.quadDuplet2Table  = self.createTable(quadDuplet2Info)
        self.quadTriplet1Table = self.createTable(quadTriplet1Info)
        self.quadTriplet2Table = self.createTable(quadTriplet2Info)

    def createTableTitle(self, title):
        label = QLabel()
        titleFont = QtGui.QFont('Arial', 15)
        titleFont.setBold(True)
        label.setText(title)
        label.setFont(titleFont)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label
    
    def createTable(self, table):
        rows    = len(table)
        columns = len(table[0])
        newTable = QTableWidget()
        newTable.setFont(QtGui.QFont('Arial', 12))
        newTable.verticalHeader().hide()
        newTable.setRowCount(rows-1)
        newTable.setColumnCount(columns)
       
        for i in range(columns):
            titleItem = QTableWidgetItem('{}'.format(table[0][i]))
            newTable.setHorizontalHeaderItem(i, titleItem)

        for i in range(rows-1):
            for j in range(columns):
                tableItem = QTableWidgetItem('{}'.format(table[i+1][j]))
                tableItem.setTextAlignment(QtCore.Qt.AlignHCenter)
                newTable.setItem(i, j, tableItem)
                enableItem = self.getQTableWidgetItemFlags()
                tableItem.setFlags(enableItem)
        return newTable

    def getQTableWidgetItemFlags(self):
        """
        Just for documentation of how to make editable the table Items
        """
        selectable = QtCore.Qt.ItemIsSelectable
        enabled    = QtCore.Qt.ItemIsEnabled
        editable   = QtCore.Qt.ItemIsEditable
        return enabled
