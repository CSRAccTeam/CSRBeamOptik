import numpy as np
from CSRBeamOptik.beamOptik.Constants import *

class ChargedParticle:

    def __init__(self, eKin, charge, mass):
        e0 = elementaryCharge()
        self.eKin   = eKin*1e3*e0
        self.charge = charge*e0
        self.mass   = mass
        self.speed  = 0.
        self.Brho   = 0.
        self.gamma  = 1.
        self.beta   = 0.
        self.setParticle()

    def getEkin(self, ISunits=False):
        e0 = elementaryCharge()
        if ISunits: return self.eKin
        return self.eKin/(e0*1e3)

    def getCharge(self, ISunits=False):
        e0 = elementaryCharge()
        if ISunits: return self.charge
        return round(self.charge/e0)

    def setParticle(self):
        self.setSteifigkeit()
        self.setSpeed()
        self.setBeta()
        self.setGamma()
        self.setFrequency()

    def resetParticle(self, eKin, charge, mass):
        e0 = elementaryCharge()
        self.eKin   = eKin*1e3*e0
        self.charge = charge*e0
        self.mass   = mass
        self.setParticle()

    def getSteifigkeit(self):
        eKin = self.eKin
        Q    = self.charge
        A    = self.mass
        amu  = atomicMassUnit()
        c    = speedOfLight()
        Brho = abs( np.sqrt( eKin * (eKin + 2 * A * amu * c * c) ) / (Q * c) )
        return Brho

    def getElekSteifigkeit(self):
        amu  = atomicMassUnit()
        Erho = self.gamma*(amu*self.mass)*self.speed**2/self.charge
        return Erho

    def setSteifigkeit(self):
        self.Brho = self.getSteifigkeit()

    def getSpeed(self):
        eKin = self.eKin
        c    = speedOfLight()
        amu  = atomicMassUnit()
        A    = self.mass
        v    = c*np.sqrt(1 - ( ( A* amu * c**2 ) / ( eKin + A * amu * c**2) )**2)
        return v

    def getBeta(self):
        c    = speedOfLight()
        return self.speed/c

    def getGamma(self):
        gamma = 1./(np.sqrt(1-self.beta**2))
        return gamma

    def getFrequency(self):
        return self.speed/CSRUmfang()

    def getRevolutionTime(self):
        return 1./self.frequency

    def setSpeed(self): self.speed = self.getSpeed()
    def setBeta(self):  self.beta  = self.getBeta()
    def setGamma(self): self.gamma = self.getGamma()
    def setFrequency(self): self.frequency = self.getFrequency()

class IonBeam:

    def __init__(self, particle):
        self.particle = particle
        self.emx = 30e-6
        self.emy = 30e-6
        self.emt = 30e-6

    def getBeamInfo(self):
        e0 = elementaryCharge()
        particleInfo = {
            'Ekin': {'Value': self.particle.getEkin(),
                     'Unit':  'keV'},
            'Charge':{'Value': self.particle.getCharge(),
                     'Unit':  'e'},
            'Mass':{'Value': self.particle.mass,
                     'Unit':  'u'},
            'emx':{'Value': self.emx*1e6,
                     'Unit':  'mm mrad'},
            'emy':{'Value': self.emy*1e6,
                     'Unit':  'mm mrad'}
        }
        return particleInfo
