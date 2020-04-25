import numpy as np
from CSRBeamOptik.beamOptik.Constants import *

class Element:

    def __init__(self, madguiParamName,
                 particle, lmad, leff,
                 EUNetName):
        self.name     = madguiParamName
        self.particle = particle
        self.lmad     = lmad
        self.leff     = leff
        self.ui_unit  = 1.
        self.unit     = 1.
        self.readValue = 0.
        self.madxParam = 0.
        self.EUNetName = EUNetName

class Quadrupole(Element):

    def __init__(self, madguiParamName, particle,
                 lmad, leff, EUNetName, r0, corr=1):
        super().__init__(madguiParamName,
                         particle, lmad, leff, EUNetName)
        self.r0         = r0
        self.correction = corr

    def setReadValue(self, Uquad):
        self.readValue = Uquad
        self.setMadxParam(Uquad)

    def setMadxParam(self, Uquad):
        lmad = self.lmad
        leff = self.leff
        r02  = self.r0**2
        eKin = self.particle.eKin
        Q    = self.particle.charge
        corr = self.correction
        #Uquad *= 1.e3
        kMad = (leff * Q * corr * Uquad) / (lmad * r02 * eKin)
        self.madxParam = kMad

    def getkMad(self, Uquad):
        self.setMadxParam(Uquad)
        return self.madxParam

    def getkSoll(self):
        # TODO: Implement computation of k Value as
        # function of working point Q
        raise NotImplementedError

    def getUquad(self, kMad):
        lmad  = self.lmad
        leff  = self.leff
        r02   = self.r0**2
        eKin  = self.particle.eKin
        Q     = self.particle.charge
        corr  = self.correction
        Uquad = (lmad * r02 * eKin * kMad) / (leff * Q * corr)
        return Uquad


class QuadrupoleMagnetisch(Element):

    def __init__(self, madguiParamName, particle,
                 lmad, leff, EUNetName, corr=1):
        super().__init__(madguiParamName,
                         particle, lmad, leff, EUNetName)
        self.correction = corr

    def setReadValue(self, current):
        self.readValue = current
        self.setMadxParam(current)

    def setMadxParam(self, current):
        # TODO: Implement computation of k Value as
        # function of measured current
        self.madxParam = -9999.

    def getkSoll(self):
        # TODO: Implement computation of k Value as
        # function of working point Q
        raise NotImplementedError

    def getCurrent(self, kMad):
        # TODO: Implement computation of current as
        # function of wished k Value
        raise NotImplementedError

class Deflector(Element):

    def __init__(self, madguiParamName, particle,
                 EUNetName, radius, rIn, rOut, scalFactor):
        super().__init__(madguiParamName,
                         particle, 1., 1., EUNetName)
        self.radius     = radius
        self.rIn        = rIn
        self.rOut       = rOut
        self.scalFactor = scalFactor
        self.setVoltages()

    def getVoltage(self, rInOut):
        e0         = elementaryCharge()
        eKin       = self.particle.eKin
        scalFactor = self.scalFactor
        U = 2 * eKin * np.log(rInOut / self.radius) * scalFactor / Q
        return U

    def getVoltageIn(self):  return self.getVoltage(rIn)/1000.
    def getVoltageOut(self): return self.getVoltage(rOut)/1000.

    def setVoltages(self):
        self.voltageIn = self.getVoltageIn()
        self.voltageOut = self.getVoltageOut()

    def getBipolarValue(self, U, Umax):
        return (U + Umax)/ (2 * Umax)

    def setMadxParam(self, voltage):
        # TODO: Implement computation of kick
        self.madxParam = -9999.

class BendingMagnet(Element):

    def __init__(self, madguiParamName, particle,
                 lmad, leff, EUNetName, h):
        super().__init__(madguiParamName,
                         particle, lmad, leff, EUNetName)
        self.bendR = h

    def setReadValue(self, current):
        self.readValue = current
        self.setMadxParam(current)

    def getBFeldSoll(self):
        return self.particle.getSteifigkeit() / self.bendR

    def getBFeld(self, current):
        # TODO: Implement BFeld as function of the current
        # We need calibration curves B(I)
        return 'Not implemented'

    def getCurrent(self, BFeld):
        # TODO: Implement current as function of BFeld
        # We need calibration curves B(I)
        raise NotImplementedError

    def setMadxParam(self, current):
        # TODO: Implement computation of kick
        self.madxParam = -9999.
