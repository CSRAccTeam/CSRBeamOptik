from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QTableWidgetItem, QWidget, QGridLayout, QFormLayout,
                             QTextEdit, QLineEdit, QLabel, QTableWidget,
                             QPushButton)
import numpy as np

class mainWidget(QWidget):

    def __init__(self, manager, particle):
        super().__init__()

        self.particle   = particle
        self.manager    = manager
        self.clientName = 'IQ300'
        self.deviceList = self.manager.getDevicesInfo(self.clientName)
        self.titles     = self.initTableTitles()
        self.tables     = []
        self.elements   = {}
        self.initUI()
        
    def initUI(self):
        mainGrid = QGridLayout()
        self.initElementTables()
        self.setLayout(mainGrid)

        for i in range(3):
            mainGrid.addWidget(self.titles[i], 2*i,   0)
            mainGrid.addWidget(self.tables[i], 2*i+1, 0)#, 1, 2)
        
    def initTableTitles(self):
        dipolesTitle     = self.createTableTitle('DIPOLES')
        quadDupletTitle  = self.createTableTitle('QUADRUPOLE DUPLETS')
        quadTripletTitle = self.createTableTitle('QUADRUPOLE TRIPLETS')
        return [dipolesTitle, quadDupletTitle, quadTripletTitle]
        
    def initElementTables(self):
        dipolesInfo     = [['Name', 'Current [A]',  'B_ist [mT]', 'B_soll [mT]']]
        quadDupletInfo  = [['Name', 'Current [A]',  'K_ist [m^-2]', 'K_soll [m^-2]']]
        quadTripletInfo = [['Name', 'Voltage [kV]', 'K_ist [m^-2]', 'K_soll [m^-2]']]

        for devName in self.deviceList:
            devInfo = self.deviceList[devName]
            element = devInfo['element']
            eleType = devInfo['type']
            elGroup = devInfo['group']
            elSpecs = devInfo['specs']
            readValue  = round(self.manager.getValue(devName), 3)
            self.initElement(devName, element, eleType, elSpecs)
            opticalElem  = self.elements[devName]
            elOptics     = self.getElementOptics(opticalElem, element,
                                                 eleType, readValue)
            # TODO: Get rid of this if-else control structure
            if elOptics[0] == 'Not implemented':
                elOpticsIst  = '-'
            else:
                elOpticsIst  = round(elOptics[0], 3)
            if elOptics[1] == 'Not implemented':
                elOpticsSoll = '-'
            else:
                elOpticsSoll = round(elOptics[1], 3)
            #################################################
            if 'Dipoles' in elGroup:
                dipolesInfo.append([devName, readValue,
                                    elOpticsIst, elOpticsSoll])
            elif 'Duplet' in elGroup:
                quadDupletInfo.append([devName, readValue,
                                       elOpticsIst, elOpticsSoll])
            elif 'Triplet' in elGroup:
                quadTripletInfo.append([devName, readValue,
                                        elOpticsIst, elOpticsSoll])
                
        dipoleTable      = self.createTable(dipolesInfo)
        quadDupletTable  = self.createTable(quadDupletInfo)
        quadTripletTable = self.createTable(quadTripletInfo)

        #dipoleTable.resizeColumnsToContents()
        #quadDupletTable.resizeColumnsToContents()
        #quadTripletTable.resizeColumnsToContents()

        self.tables = [dipoleTable,
                       quadDupletTable,
                       quadTripletTable]

    # TODO: Migrate this to BeamLine Class and ensure compatibility    

    def initElement(self, elementName, elementKind,
                          elementType, elementSpecs):
        """
        @param elementName is the tag of the element
        @param elementKind is the kind of element e.g. Quadrupole, BendingMagnet, etc
        @param elementType is the type of element e.g. electrostatic or magnetic
        @param readValue   is the read value from the server
        @param elemtSpecs  are the element specifications needed to initialize 
                           the element
        """
        from CSRBeamOptik.beamOptik.Elements import (Quadrupole,
                                                     QuadrupoleMagnetisch,
                                                     Deflector,
                                                     BendingMagnet)
        particle = self.particle
        if (elementKind == 'Dipole' and elementType == 'magnetisch'):
            bendRadius = elementSpecs['h']
            angle = elementSpecs['angle']
            lmad  = bendRadius * angle * (np.pi / 180.)
            # Effective length of magnetic bending dipoles has not yet been
            # measured, or no data is available
            newElement = BendingMagnet(particle, lmad, lmad, bendRadius)
        elif (elementKind == 'Quadrupole') or (elementKind == 'Quadrupole_kicker'):
            if elementType == 'magnetisch':
                lmad = elementSpecs['length']
                newElement = QuadrupoleMagnetisch(particle, lmad, lmad)
            elif elementType == 'elektrostatisch':
                lmad   = elementSpecs['lmad']
                leff   = elementSpecs['leff']
                radius = elementSpecs['radius']
                corr   = elementSpecs['correction']
                newElement = Quadrupole(particle, lmad, leff, radius, corr)
        self.elements.update({elementName : newElement})

    def getElementOptics(self, element, elementKind, elementType, readValue):
        if (elementKind == 'Dipole' and elementType == 'magnetisch'):
            current = readValue
            bFeld_ist  = element.getBFeld(current)
            bFeld_soll = element.getBFeldSoll()*1e3 # [mT]
            return [bFeld_ist, bFeld_soll]
        elif (elementKind == 'Quadrupole') or (elementKind == 'Quadrupole_kicker'):
            if elementType == 'magnetisch':
                current = readValue
                k_ist  = element.getkMad(current)
                k_soll = element.getkSoll()
                return [k_ist, k_soll]
            elif elementType == 'elektrostatisch':
                voltage = readValue*1e3
                k_ist  = element.getkMad(voltage)
                k_soll = element.getkSoll()
                return [k_ist, k_soll]
        return [0., 0.]

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
                devName     = devNameItem.text()
                devInfo = self.deviceList[devName]
                element = devInfo['element']
                eleType = devInfo['type']
                readValue   = round(self.manager.getValue(devName), 3)
                opticalElem  = self.elements[devName]
                elOptics     = self.getElementOptics(opticalElem, element,
                                                     eleType, readValue)
                # TODO: Get rid of this if-else control structure
                if elOptics[0] == 'Not implemented':
                    elOpticsIst  = '-'
                else:
                    elOpticsIst  = round(elOptics[0], 3)
                if elOptics[1] == 'Not implemented':
                    elOpticsSoll = '-'
                else:
                    elOpticsSoll = round(elOptics[1], 3)
                #################################################
                devReadItem = table.item(i, 1)
                devIstVal   = table.item(i, 2)
                devSollVal  = table.item(i, 3)
                devReadItem.setText('{}'.format(readValue))
                devIstVal.setText('{}'.format(elOpticsIst))
                devSollVal.setText('{}'.format(elOpticsSoll))
                
    def getQTableWidgetItemFlags(self):
        """
        Just for documentation of how to make editable the table Items
        """
        selectable = QtCore.Qt.ItemIsSelectable
        enabled    = QtCore.Qt.ItemIsEnabled
        editable   = QtCore.Qt.ItemIsEditable
        return enabled
