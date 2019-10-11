import sys
from PyQt5.QtCore import QTimer, QCoreApplication

def initApp(particle, argv=None, gui=True):
    from CSRBeamOptik.widgets.mainWindow import mainWindow
    from PyQt5.QtWidgets import QApplication
    if argv is None: argv = sys.argv
    if gui:
        from PyQt5.QtWidgets import QApplication
        from importlib_resources import read_text
        app = QApplication(argv)
        # matplotlib must be imported *after* Qt;
        # must be selected before importing matplotlib.backends:
        # import matplotlib
        # matplotlib.use('Qt5Agg')
        mainW = mainWindow(particle)
        sys.exit(app.exec_())

def initIonBeam():
    from CSRBeamOptik.beamOptik.IonBeam import ChargedParticle
    eKin = 200.
    Q    = 1.
    mass = 15.999 + 1.
    OHminus = ChargedParticle(eKin, Q, mass)
    return OHminus

def getProton():
    from CSRBeamOptik.beamOptik.IonBeam import ChargedParticle
    eKin = 300.
    Q    = 1.
    mass = 1.
    proton300keV = ChargedParticle(eKin, Q, mass)
    return proton300keV
    
def main(argv=None, MainWindow=None):
    particle = initIonBeam()
    initApp(particle)

    
