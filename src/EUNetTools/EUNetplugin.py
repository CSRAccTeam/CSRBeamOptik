# -*- coding: utf-8 -*-
"""
Created on Thu Jul 04 12:50:00 2019
@author: C. Cortes
"""
from EUNetMap import EUNetMap


class EUNetPlugin:

    def __init__(self):
        """
        This class simplifies the connection to the devices
        by offering the functionability asked for
        """
        self.manager = EUNetManager()
        
    def set(self, devName, prop, value):
        self.manager.setValue(devName, prop, value)
    
    def get(self, devName, prop):
        return self.manager.getValue(devName, prop)

    def getDeviceList(self):
        """
        Returns a list of tuples with device 
        list and properties. Should we return a list 
        with the available input devices? or the output
        devices? or both?
        """
        pass

    def close(self):
        self.manager.closeSession()

        
class EUNetManager:

    def __init__(self):
        #TODO: Implement a generic way for finding this path
        self.configFolder = '../configFiles/'
        self.globalConfig = self.setGlobalConfig()
        self.theMaps = self.setTheMaps()

    def setGlobalConfig(self):
        # TODO: Implement correct packaging for user convenience
        globalConfigFile = 'global.csv'
        return self.configFolder + globalConfigFile

    def setTheMaps(self):
        """
        Initializes the maps which then have access to
        the client and devices specified in the global config
        """
        theMaps = []
        clients = self.readCsvFile(self.globalConfig)
        for c in clients: c[2] = self.configFolder + c[2]
        for c in clients: theMaps.append(EUNetMap(*c))
        return theMaps
        
    def isInDeviceList(self, devName):
        """
        Returns the map which contains the device
        """
        for m in self.theMaps:
            if m.isInDeviceList(devName): return [True, m]
        print('Warning: Device not found')
        return [False]
    
    def getValue(self, devName, prop):
        m = self.isInDeviceList(devName)
        if m[0]: return m[1].getValue(devName, prop)
        else: raise Exception('Device not found')

    def setValue(self, devName, prop, dValue):
        m = self.isInDeviceList(devName)
        if m[0]: m[1].setValue(devName, prop, dValue)
        else: raise Exception('Device not found')

    def closeSession(self):
        """
        Terminates all the connections to the servers. 
        """
        for m in self.theMaps: m.close()

    def readCsvFile(self, theFile):
        """
        Reads the global config file and returns an array 
        with the IPs, Ports and configFiles
        GlobalConfig.csv has the format:
        IP  Port  DeviceConfigFileName
        """
        #TODO: Implement this method in a util.py class
        import csv
        clients = []
        with open( theFile ) as csvFile:
            csvBuffer = csv.reader( csvFile, delimiter=',' )
            for line in csvBuffer:
                if(len(line)>0):
                    server = line[0]
                    if '#' in server: pass
                    else: clients.append(line)
        return clients        
