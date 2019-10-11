import numpy as np
from CSRBeamOptik.beamOptik.Constants import *

class ChargedParticle:

    def __init__(self, eKin, charge, mass):
        e0 = elementaryCharge()
        self.eKin   = eKin*e0*1e3
        self.charge = charge*e0
        self.mass   = mass
        self.speed  = 0.
        self.Brho   = 0.
        self.gamma  = 1.
        self.beta   = 0.
        self.setParticle()

    def setParticle(self):
        self.setSteifigkeit()
        self.setSpeed()
        self.setBeta()
        self.setGamma()
        self.setFrequency()
        
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
