import numpy as np

from CSRBeamOptik.beamOptik.Elements import (Quadrupole,
                                             QuadrupoleMagnetisch,
                                             Deflector,
                                             BendingMagnet)

class BeamLine:

    def __init__(self, bLName, particle, EUNetManager):
        """
        Here we construct the list for MADX to read.
        BeamLineName must be the same as EUClientName to get 
        the device list
        """
        self.bLName     = bLName
        self.particle   = particle
        self.manager    = EUNetManager
        self.elements   = {}
        self.bLElements = self.getLineElements()

    def getLineElements(self):
        elementsInfo = self.manager.getDevicesInfo(self.bLName)
        for element in elementsInfo:
            el = self._buildElement(element, elementsInfo[element])
        
    def setBeamLine(self):
        beamLine   = {}
        madxParams = {}
        for element in self.bLElements:
            madxParam = element['madxParam']
            
    def _buildElement(self, elName, element):
        
        elClass = element['element']
        elType  = element['type']
        elGroup = element['group']
        elSpecs = element['specs']
        madxName  = element['madxName']
        madxParam = element['madxParam']
        
        if (elClass == 'Dipole' and elType == 'magnetisch'):
            bendRadius = elSpecs['h']
            angle = elSpecs['angle']
            lmad  = bendRadius * angle * (np.pi / 180.)
            # Effective length of magnetic bending dipoles has not yet been
            # measured, or no data is available
            newElement = BendingMagnet(madxParam, self.particle,
                                       lmad, lmad, bendRadius)
        elif (elClass == 'Quadrupole') or (elClass == 'Quadrupole_kicker'):
            if elType == 'magnetisch':
                lmad = elSpecs['length']
                newElement = QuadrupoleMagnetisch(madxParam, self.particle,
                                                  lmad, lmad)
            elif elType == 'elektrostatisch':
                lmad   = elSpecs['lmad']
                leff   = elSpecs['leff']
                radius = elSpecs['radius']
                corr   = elSpecs['correction']
                newElement = Quadrupole(madxParam, self.particle,
                                        lmad, leff, radius, corr)
        newElement.setMadxParam(self.manager.getValue(elName))
        self.elements.update({elName : newElement})

    def showBeamElements(self):

        for el in self.elements:
            print(el)
            print(self.elements[el])
