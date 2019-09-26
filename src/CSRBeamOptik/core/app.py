import sys
from PyQt5.QtCore import QTimer, QCoreApplication

def init_app(argv=None, gui=True):

    if argv is None: argv = sys.argv
    if gui:
        from PyQt5.QtWidgets import QApplication
        from importlib_resources import read_text
        app = QApplication(argv)
        # matplotlib must be imported *after* Qt;
        # must be selected before importing matplotlib.backends:
        import matplotlib
        matplotlib.use('Qt5Agg')

def main(argv=None, MainWindow=None):
    from CSRBeamOptik.widgets.mainWindow import mainWindow
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    mainW = mainWindow()
    sys.exit(app.exec_())
    
