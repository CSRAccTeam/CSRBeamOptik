"""Main Window of the application"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer


class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.mainWidget = self.getMainWidget()
        self.initUI()
        self.refreshCycle()
        
    def initUI(self):
        self.statusBar().showMessage('Online')
        self.setWindowTitle('CSR Beam Optik')
        self.setGeometry(0, 0, 450, 750)
        self.setCentralWidget(self.mainWidget)
        self.show()

    def getMainWidget(self):
        from CSRBeamOptik.widgets.windowWidgetIQ300 import mainWidget
        return mainWidget()

    def refreshCycle(self):
        timer = QTimer(self)
        timer.timeout.connect(self.refreshTable)
        timer.setInterval(1500)
        timer.start()

    def refreshTable(self): self.mainWidget.refreshTable()
