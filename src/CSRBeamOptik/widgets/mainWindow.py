"""Main Window of the application"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from CSRBeamOptik.EUNetTools.EUNetPlugin import EUNetManager

class mainWindow(QMainWindow):
    
    def __init__(self, particle):
        
        super().__init__()
        self.particle     = particle
        self.EUNetManager = EUNetManager()
        self.mainWidget   = self.getMainWidget()
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
        return mainWidget(self.EUNetManager, self.particle)

    def refreshCycle(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshTable)
        self.timer.setInterval(1500)
        self.timer.start()

    def stopRefreshCycle(self): self.timer.stop()
        
    def refreshTable(self): self.mainWidget.refreshTable()
