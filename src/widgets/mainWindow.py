"""Main Window of the application"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.setWindowTitle('CSR Beam Optik')
        self.setGeometry(0, 0, 450, 750)
        from iq300WindowWidget import mainWidget
        self.setCentralWidget(mainWidget())
        self.show()

app = QApplication(sys.argv)
mainW = mainWindow()
sys.exit(app.exec_())
    
