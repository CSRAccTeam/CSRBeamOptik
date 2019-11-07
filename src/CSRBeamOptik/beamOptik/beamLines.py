from CSRBeamOptik.beamOptik.Elements import (Quadrupole,
                                             QuadrupoleMagnetisch,
                                             Deflector,
                                             BendingMagnet)


class BeamLine:

    def __init__(self, BeamLineName, particle, EUNetManager):
        """
        Here we construct the list for MADX to read.
        BeamLineName must be the same as EUClientName to get 
        the device list
        """
        self.BLName     = BLName
        self.particle   = particle
        self.manager    = EUNetManager
        self.BLElements = self.getLineElements()
        self.madxParams = {}
        self.beamLine   = {}
        self.beamLine   = self.getBeamLine()

    def setLineElements(self):
        elementsInfo = self.manager.getDevicesInfo(self.BLName)
        for element in elementsInfo:
            el = self._buildElement(element)
        
    def setBeamLine(self):
        beamLine   = {}
        madxParams = {}
        for element in self.BLElements:
            madxParam = element['madxParam']
            
    def _buildElement(self, element):
        
        elClass = element['element']
        elType  = element['type']
        elGroup = element['group']
        elSpecs = element['specs']
        madxName  = element['madxName']
        madxParam = element['madxParam']
        
        if (elementKind == 'Dipole' and elementType == 'magnetisch'):
            bendRadius = elementSpecs['h']
            angle = elementSpecs['angle']
            lmad  = bendRadius * angle * (np.pi / 180.)
            # Effective length of magnetic bending dipoles has not yet been
            # measured, or no data is available
            newElement = BendingMagnet(particle, lmad, lmad, bendRadius)
        elif (elementKind == 'Quadrupole') or (elementKind == 'Quadrupole_kicker'):
            if elementType == 'magnetisch':
                lmad = elementSpecs['length']
                newElement = QuadrupoleMagnetisch(particle, lmad, lmad)
            elif elementType == 'elektrostatisch':
                lmad   = elementSpecs['lmad']
                leff   = elementSpecs['leff']
                radius = elementSpecs['radius']
                corr   = elementSpecs['correction']
                newElement = Quadrupole(particle, lmad, leff, radius, corr)
        self.elements.update({elementName : newElement})
