import numpy as np

from CSRBeamOptik.beamOptik.Elements import (Quadrupole,
                                             QuadrupoleMagnetisch,
                                             Deflector,
                                             BendingMagnet)

class BeamLine:

    def __init__(self, bLName, particle, EUNetManager):
        self.bLName     = bLName
        self.particle   = particle
        self.manager    = EUNetManager
        self.elements   = {}
        self.setLineElements()

    def setLineElements(self):
        elementsInfo = self.manager.getDevicesInfo(self.bLName)
        for element in elementsInfo:
            el = self._buildElement(element, elementsInfo[element])
            elementsInfo[element].update({'beamOptikElement':el})
            self.elements.update({element:elementsInfo[element]})

    def _buildElement(self, elName, element):

        elClass = element['element']
        elType  = element['type']
        elGroup = element['group']
        elSpecs = element['specs']
        madxName  = element['madxName']
        madxParam = element['madxParam']

        if (elClass == 'Dipole'):
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
        newElement.setReadValue(self.manager.getValue(elName))
        return newElement

    def updateElementReads(self):
         for elName in self.elements:
             e = self.elements[elName]
             e['beamOptikElement'].setReadValue(self.manager.getValue(elName))
