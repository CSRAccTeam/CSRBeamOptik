from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QTableWidgetItem, QWidget, QGridLayout, QFormLayout,
                             QTextEdit, QLineEdit, QLabel, QTableWidget,
                             QPushButton)

class mainWidget(QWidget):

    def __init__(self):

        super().__init__()
        
        from CSRBeamOptik.EUNetTools.EUNetPlugin import EUNetManager
        self.manager    = EUNetManager()
        self.clientName = 'IQ300'
        self.deviceList = self.manager.getDevicesInfo(self.clientName)
        self.initUI()
        
    def initUI(self):
        mainGrid = QGridLayout()
        self.setElementTables()
        self.setTableTitles()
        self.setLayout(mainGrid)

        for i in range(3):
            mainGrid.addWidget(self.titles[i], 2*i,   0)
            mainGrid.addWidget(self.tables[i], 2*i+1, 0)#, 1, 2)
        
    def setTableTitles(self):

        dipolesTitle     = self.createTableTitle('DIPOLES')
        quadDupletTitle  = self.createTableTitle('QUADRUPOLE DUPLETS')
        quadTripletTitle = self.createTableTitle('QUADRUPOLE TRIPLETS')
        self.titles = [dipolesTitle,
                       quadDupletTitle,
                       quadTripletTitle]
        
    def setElementTables(self):
        
        dipolesInfo     = [['Name', 'Current [A]',  'B_ist [mT]', 'B_soll [mT]']]
        quadDupletInfo  = [['Name', 'Current [A]',  'K_ist', 'K_mad']]
        quadTripletInfo = [['Name', 'Voltage [kV]', 'K_ist', 'K_mad']]

        for device in self.deviceList:
            devInfo = self.deviceList[device]
            element = devInfo['element']
            eleType = devInfo['type']
            elGroup = devInfo['group']
            readValue = round(self.manager.getValue(device), 3)
            if 'Dipoles' in elGroup:
                dipolesInfo.append([device, readValue ,0., 0.])
            elif 'Duplet' in elGroup:
                quadDupletInfo.append([device, readValue, 0., 0.])
            elif 'Triplet' in elGroup:
                quadTripletInfo.append([device, readValue, 0., 0.])
                
        dipoleTable      = self.createTable(dipolesInfo)
        quadDupletTable  = self.createTable(quadDupletInfo)
        quadTripletTable = self.createTable(quadTripletInfo)

        self.tables = [dipoleTable,
                       quadDupletTable,
                       quadTripletTable]

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

    def refreshTable(self):
        for table in self.tables:
            rows = table.rowCount()
            cols = table.columnCount()
            for i in range(rows):
                devNameItem = table.item(i, 0)
                devName = devNameItem.text()
                readValue = round(self.manager.getValue(devName), 3)
                devReadItem = table.item(i, 1)
                devReadItem.setText('{}'.format(readValue))
            
    def getQTableWidgetItemFlags(self):
        """
        Just for documentation of how to make editable the table Items
        """
        selectable = QtCore.Qt.ItemIsSelectable
        enabled    = QtCore.Qt.ItemIsEnabled
        editable   = QtCore.Qt.ItemIsEditable
        return enabled
