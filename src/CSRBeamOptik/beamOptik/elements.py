import numpy as np
from constants import *

class Quadrupole:

    def __init__(self, particle, lmad, leff, r0, corr=1):
        self.particle   = particle
        self.lmad       = lmad
        self.leff       = leff
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

    def getUquad(self, kMad):
        lmad  = self.lmad
        leff  = self.leff
        r02   = self.r0**2
        eKin  = self.particle.eKin
        Q     = self.particle.charge
        corr  = self.correction
        Uquad = (lmad * r02 * eKin * kMad) / (leff * Q * corr)
        return kMad

class Deflector:

    def __init__(self, particle, radius, rIn, rOut, scalFactor):
        self.particle   = particle
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

class BendingMagnet:

    def __init__(self, particle, lmad, leff):
        self.particle = particle
        self.lmad     = lmad
        self.leff     = leff

    def getBFeld(self):
        pass

    def getCurrent(self):
        pass
