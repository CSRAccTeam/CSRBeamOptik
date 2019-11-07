import numpy as np
from CSRBeamOptik.beamOptik.Constants import *

class Element:

    def __init__(self, particle, lmad, leff):
        self.particle = particle
        self.lmad     = lmad
        self.leff     = leff

class Quadrupole(Element):

    def __init__(self, particle, lmad, leff, r0, corr=1):
        super().__init__(particle, lmad, leff)
        self.r0         = r0
        self.correction = corr

    def getkMad(self, Uquad):
        lmad = self.lmad
        leff = self.leff
        r02  = self.r0**2
        eKin = self.particle.eKin
        Q    = self.particle.charge
        corr = self.correction
        kMad = (leff * Q * corr * Uquad) / (lmad * r02 * eKin)
        return kMad

    def getkSoll(self):
        # TODO: Implement computation of k Value as
        # function of working point Q
        return 'Not implemented'

    def getUquad(self, kMad):
        lmad  = self.lmad
        leff  = self.leff
        r02   = self.r0**2
        eKin  = self.particle.eKin
        Q     = self.particle.charge
        corr  = self.correction
        Uquad = (lmad * r02 * eKin * kMad) / (leff * Q * corr)
        return kMad

class QuadrupoleMagnetisch(Element):

    def __init__(self, particle, lmad, leff, corr=1):
        super().__init__(particle, lmad, leff)
        self.correction = corr

    def getkMad(self, current):
        # TODO: Implement computation of k Value as
        # function of measured current
        return 'Not implemented'

    def getkSoll(self):
        # TODO: Implement computation of k Value as
        # function of working point Q
        return 'Not implemented'

    def getCurrent(self, kMad):
        # TODO: Implement computation of current as
        # function of wished k Value
        return 'Not implemented'

class Deflector(Element):

    def __init__(self, particle, radius, rIn, rOut, scalFactor):
        super().__init__(particle, 1., 1.)
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

class BendingMagnet(Element):

    def __init__(self, particle, lmad, leff, h):
        super().__init__(particle, lmad, leff)
        self.bendR = h

    def getBFeldSoll(self):
        return self.particle.getSteifigkeit() / self.bendR

    def getBFeld(self, current):
        # TODO: Implement BFeld as function of the current
        # We need calibration curves B(I)
        return 'Not implemented'
    
    def getCurrent(self, BFeld):
        # TODO: Implement current as function of BFeld
        # We need calibration curves B(I)
        pass
