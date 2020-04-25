"""
Madgui online control plugin.
"""

from __future__ import absolute_import
import requests
import os
import logging

from CSRBeamOptik.EUNetTools.EUNetPlugin import EUNetManager
from CSRBeamOptik.beamOptik.IonBeam import ChargedParticle
from CSRBeamOptik.util.loadFiles import readYamlFile
from CSRBeamOptik.beamOptik.beamLines import BeamLine

import madgui.online.api as api
from madgui.util.misc import relpath as safe_relpath
from madgui.util.collections import Bool
from madgui.util.qt import SingleWindow

class _CSRBeamOptik(api.Backend):

    def __init__(self, session, settings):
         self.session   = session
         self.settings  = settings
         self.connected = Bool(False)
         self.manager   = EUNetManager()
         self.particle  = self._getBeam()
         # For now we try just the IQ300
         self.beamLine  = BeamLine('IQ300', self.particle, self.manager)
         self.backendKnobs = self.getBackendKnobs()

    # Backend API

    def connect(self):
        """Connect to online database (must be loaded)."""
        isConnected  = self.manager.isConnected
        self.connected.set(isConnected)

    def disconnect(self):
        """Disconnect from online database."""
        logging.info('Disconnecting from EUNetClients')
        self.manager.closeSession()
        logging.info('Succesfully closed session')
        self.connected.set(False)

    def execute(self):
        """Execute changes (commits prior set_value operations)."""
        pass

    def getBackendKnobs(self):
        elements = self.beamLine.elements
        blElems  = [elements[e] for e in elements]
        backendKnobs = {e['madxParam']:e['beamOptikElement']
                        for e in blElems}
        return backendKnobs

    def param_info(self, knob):
        """Get parameter info for backend key."""
        try:
            return self.backendKnobs[knob]
        except KeyError as e:
            # Madgui asks for the globals in MADX which are not
            # always element attributes
            return
        except RuntimeError as e:
            if warn:
                logging.warning("{} for {!r}".format(e, param))

    def read_monitor(self, name):
        """
        Read out one monitor, return values as dict with keys
        posx/posy/envx/envy.
        """
        pass

    def read_params(self, param_names=None, warn=True):
        """Read all specified params (by default all). Return dict."""
        if param_names is None and self.connected:
            return {}

        return {
            param: value
            for param in param_names
            for value in [self.read_param(param, warn=warn)]
            if value is not None
        }

    def read_param(self, param, warn=True):
        """Read parameter. Return numeric value."""
        try:
            element = self.backendKnobs[param]
            return element.madxParam
        except KeyError as e:
            # Madgui asks for the globals in MADX which are not
            # always element attributes
            return
        except RuntimeError as e:
            if warn:
                logging.warning("{} for {!r}".format(e, param))

    def write_param(self, param, value):
        """Update parameter into control system."""
        if 'getUquad' in dir(self.backendKnobs[param]):
            element = self.backendKnobs[param]
            value   = element.getUquad(value)
            self.manager.setValue(element.EUNetName, value)

    def get_beam(self):
        return self._getBeam()

    def _getBeam(self):
        """
        Loads the data from the web server. Note that the ion
        might not match with the ongoing experiment.
        """
        configFile  = '/home/cristopher/MPIK/CSRBeamOptik/configFiles/ionDict.yaml'
        ionConfig   = readYamlFile(configFile)
        ionDataURL  = ionConfig['ionDataURL']
        ionDataKeys = ionConfig['ionDataKeys']
        ionData = requests.get(ionDataURL)
        ionData = ionData.text
        logging.info('Loading beam from online data')
        ionData = self._readIonData(ionData)
        #logging.info('{}'.format(ionData))
        eKin = ionData['EkinIon']
        Q    = ionData['LadungIon']
        mass = ionData['MasseIon']
        ion  = ChargedParticle(eKin, Q, mass)
        #TODO: Implement user input definition of beam
        return ion

    def _readIonData(self, ionData):
        lines = ionData.split('\n')
        lines = [line.split('=') for line in lines if len(line.split('='))==2]
        ionData = {l[0]:float(l[1]) for l in lines}
        return ionData

class CSR_ACS(_CSRBeamOptik):

    def __init__(self, session, settings):
        """Connect to online database."""
        super().__init__(session, settings)
