import sys
from PyQt5.QtCore import QTimer, QCoreApplication

def initApp(particle, EUNetManager, argv=None, gui=True):
    from CSRBeamOptik.widgets.mainWindow import mainWindow
    from PyQt5.QtWidgets import QApplication
    if argv is None: argv = sys.argv
    if gui:
        from PyQt5.QtWidgets import QApplication
        from importlib_resources import read_text
        app   = QApplication(argv)
        mainW = mainWindow(particle, EUNetManager)
        sys.exit(app.exec_())
    
def getProton():
    from CSRBeamOptik.beamOptik.IonBeam import ChargedParticle
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
        if (len(data) == 2.):
            ionData.update({data[0] : float(data[1])})
    return ionData

def initIonBeam():
    from CSRBeamOptik.beamOptik.IonBeam import ChargedParticle
    from CSRBeamOptik.util.loadFiles import readYamlFile
    import requests

    ionConfig = readYamlFile('/home/blm/ccortes/MPIK/CSR/CSRBeamOptik' + \
                             '/configFiles/ionDict.yaml')
    ionDataURL  = ionConfig['ionDataURL']
    ionDataKeys = ionConfig['ionDataKeys']
    ionData = requests.get(ionDataURL)
    ionData = ionData.text
    ionData = _readIonData(ionData)
    
    eKin = ionData['EkinIon']
    Q    = ionData['LadungIon']
    mass = ionData['MasseIon']
    ion  = ChargedParticle(eKin, Q, mass)
    
    return ion

def main(argv=None, MainWindow=None):
    from CSRBeamOptik.EUNetTools.EUNetPlugin import EUNetManager
    particle = initIonBeam()
    initApp(particle, EUNetManager())

    
