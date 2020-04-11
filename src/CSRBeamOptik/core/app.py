import sys
import requests

from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtWidgets import QApplication

from CSRBeamOptik.beamOptik.IonBeam import ChargedParticle
from CSRBeamOptik.util.loadFiles import readYamlFile

# TODO: Revisit this poor implementation

def initApp(particle, EUNetManager, argv=None, gui=True):
    from CSRBeamOptik.widgets.mainWindow import mainWindow
    if argv is None: argv = sys.argv
    if gui:
        app = QApplication(argv)
        mainW = mainWindow(particle, EUNetManager)
        mainW.show()
        sys.exit(app.exec_())
    return app

def getProton():
    eKin = 300.
    Q    = 1.
    mass = 1.
    proton300keV = ChargedParticle(eKin, Q, mass)
    return proton300keV

def _readIonData(ionData):
    lines = ionData.split('\n')
    ionData = {}
    for line in lines:
        data = line.split('=')
        if (len(data) == 2.): ionData.update({data[0] : float(data[1])})
    return ionData

def initIonBeam():
    """
    Loads the data from the web server. Note that the ion
    might not match with the ongoing experiment.
    """
    ionConfig   = readYamlFile('/home/cristopher/MPIK/CSRBeamOptik' + \
                               '/configFiles/ionDict.yaml')
    ionDataURL  = ionConfig['ionDataURL']
    ionDataKeys = ionConfig['ionDataKeys']
    ionData = requests.get(ionDataURL)
    ionData = ionData.text
    print(ionData)
    ionData = _readIonData(ionData)

    eKin = ionData['EkinIon']
    Q    = ionData['LadungIon']
    mass = ionData['MasseIon']
    ion  = ChargedParticle(eKin, Q, mass)

    #TODO: Implement user input definition of beam

    return ion

def main(argv=None, MainWindow=None):
    from CSRBeamOptik.EUNetTools.EUNetPlugin import EUNetManager

    EUNetManager = EUNetManager()
    particle     = initIonBeam()
    app = initApp(particle, EUNetManager)
