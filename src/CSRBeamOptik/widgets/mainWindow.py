"""Main Window of the application"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QTableWidgetItem, QWidget, QGridLayout, QFormLayout,
                             QTextEdit, QLineEdit, QLabel, QTableWidget,
                             QPushButton, QHeaderView)
from PyQt5 import QtGui, QtCore
from madgui.util.qt import load_ui
from CSRBeamOptik.beamOptik.beamLines import BeamLine
from CSRBeamOptik.beamOptik.IonBeam import IonBeam

import numpy as np

class mainWindow(QMainWindow):

    ui_file = 'mainWindow.ui'

    def __init__(self, particle, EUNetManager):

        super().__init__()
        load_ui(self, __package__, self.ui_file)
        self.ionBeam  = IonBeam(particle)
        self.bLName   = 'IQ300'
        self.beamLine = BeamLine(self.bLName, particle, EUNetManager)
        self.elements = self.beamLine.elements
        self.tables   = []
        self.initUI()
        self.refreshCycle()

    def initUI(self):
        self.initTables()
        self.initBeamWidgets()
        self.setWindowTitle('CSR Beam Optik')

    def refreshCycle(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshTable)
        self.timer.setInterval(500)
        self.timer.start()

    def stopRefreshCycle(self): self.timer.stop()

    def initBeamWidgets(self):
        self.beamTable  = self.findChild(QTableWidget, 'beamTable')
        beamInfo   = [['Beam', 'Value', 'Unit']]
        beamDict = self.ionBeam.getBeamInfo()

        for atr in beamDict:
            beamInfo.append([atr,
                             beamDict[atr]['Value'],
                             beamDict[atr]['Unit']])

        self.fillBeamTable(beamInfo,'beamTable')

        beamButton = self.findChild(QPushButton,'beamButton')
        beamButton.clicked.connect(self._on_clicked_beamButton)

    def _on_clicked_beamButton(self):
        print('You clicked it ;)')

        rows = self.beamTable.rowCount()
        newVals = {}
        for i in range(rows):
            atrName = self.beamTable.item(i, 0)
            name = atrName.text()
            atrVal  = self.beamTable.item(i, 1)
            value   = atrVal.text()
            newVals.update({name:float(value)})

        particle = self.ionBeam.particle.__dict__
        for i in particle: print(i, particle[i])
        self.ionBeam.particle.resetParticle(newVals['Ekin'],
                                            newVals['Charge'],
                                            newVals['Mass'])
        for i in particle: print(i, particle[i])


    def initTables(self):

        dipolesInfo     = [['Name', 'Current [A]',  'B_ist [mT]']]
        quadDupletInfo  = [['Name', 'Current [A]',  'K_ist [m^-2]']]
        quadTripletInfo = [['Name', 'Voltage [kV]', 'K_ist [m^-2]']]

        for elName in self.elements:
            devInfo = self.elements[elName]
            elGroup = devInfo['group']
            opticalElement  = devInfo['beamOptikElement']
            readValue = round(opticalElement.readValue, 3)
            madxParam = round(opticalElement.madxParam, 4)

            if 'Dipoles' in elGroup:
                dipolesInfo.append([elName, readValue, madxParam])
            elif 'Duplet' in elGroup:
                quadDupletInfo.append([elName, readValue, madxParam])
            elif 'Triplet' in elGroup:
                quadTripletInfo.append([elName, readValue, madxParam])

        self.fillTable(dipolesInfo,    'dipoleTable')
        self.fillTable(quadDupletInfo, 'magneticQuadsTable')
        self.fillTable(quadTripletInfo, 'electricQuadsTable')

    def fillTable(self, table, tableName):
        newTable = self.findChild(QTableWidget, tableName)
        rows     = len(table)
        columns  = len(table[0])
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
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                newTable.setItem(i, j, tableItem)
                enableItem = self.getQTableWidgetItemFlags()
                tableItem.setFlags(enableItem)

        headerH = newTable.horizontalHeader()
        headerH.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerH.setSectionResizeMode(QHeaderView.Stretch)
        headerV = newTable.verticalHeader()
        headerV.setSectionResizeMode(QHeaderView.Stretch)

        self.tables.append(newTable)

    def fillBeamTable(self, table, tableName):
        newTable = self.findChild(QTableWidget, tableName)
        rows     = len(table)
        columns  = len(table[0])
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
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                newTable.setItem(i, j, tableItem)
                if j != 1:
                    enableItem = self.getQTableWidgetItemFlags()
                    tableItem.setFlags(enableItem)

        headerH = newTable.horizontalHeader()
        headerH.setSectionResizeMode(QHeaderView.ResizeToContents)
        headerH.setSectionResizeMode(QHeaderView.Stretch)
        headerV = newTable.verticalHeader()
        headerV.setSectionResizeMode(QHeaderView.Stretch)

    def refreshTable(self):
        self.beamLine.updateElementReads()
        for table in self.tables:
            rows = table.rowCount()
            cols = table.columnCount()
            for i in range(rows):
                devNameItem = table.item(i, 0)
                devName     = devNameItem.text()
                devInfo = self.elements[devName]
                element = devInfo['beamOptikElement']
                readValue = round(element.readValue, 3)
                madxParam = round(element.madxParam, 4)
                devReadItem = table.item(i, 1)
                devIstVal   = table.item(i, 2)
                devReadItem.setText('{}'.format(readValue))
                devIstVal.setText('{}'.format(madxParam))

    def getQTableWidgetItemFlags(self):
        """
        Just for documentation of how to make editable the table Items
        """
        selectable = QtCore.Qt.ItemIsSelectable
        enabled    = QtCore.Qt.ItemIsEnabled
        editable   = QtCore.Qt.ItemIsEditable
        return enabled

    def getQEditableItem(self):
        selectable = QtCore.Qt.ItemIsSelectable
        enabled    = QtCore.Qt.ItemIsEnabled
        editable   = QtCore.Qt.ItemIsEditable
        return selectable, enabled, editable
