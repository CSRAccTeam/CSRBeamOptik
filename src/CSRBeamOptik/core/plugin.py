"""
Madgui online control plugin.
"""

from __future__ import absolute_import

import os
import logging

from CSRBeamOptik.EUNetTools.EUNetPlugin import EUNetManager

import madgui.online.api as api
from madgui.util.misc import relpath as safe_relpath
from madgui.util.collections import Bool
from madgui.util.qt import SingleWindow

class _CSRBeamOptik(api.Backend):

    def __init__(self, session, settings):
         self.session   = session
         self.settings  = settings
         self.connected = Bool(False)

    # Backend API

    def connect(self):
        """Connect to online database (must be loaded)."""
        self.manager = EUNetManager()
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
        raise NotImplementedError

    def param_info(self, knob):
        """Get parameter info for backend key."""
        return self.manager.clientNameList
        
    def read_monitor(self, name):
        """
        Read out one monitor, return values as dict with keys
        posx/posy/envx/envy.
        """
        pass

    def read_params(self, param_names=None, warn=True):
        """Read all specified params (by default all). Return dict."""
        if param_names is None and self.connected:
            param_names = self.manager.clientNameList
            
        return {
            param: value
            for param in param_names
            for value in [self.read_param(param, warn=warn)]
            if value is not None
        }

    def read_param(self, param, warn=True):
        """Read parameter. Return numeric value."""
        paramName = param
        if paramName == 'none' or paramName == 'twiss_tol':
            return 0.
        try:
            return self.manager.getValue(paramName)
        except RuntimeError as e:
            if warn:
                logging.warning("{} for {!r}".format(e, param))

    def write_param(self, param, value):
        """Update parameter into control system."""
        pass

    def get_beam(self):
        pass

class CSR_ACS(_CSRBeamOptik):

    def __init__(self, session, settings):
        """Connect to online database."""
        super().__init__(session, settings)

