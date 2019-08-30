# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 15:21:00 2019
@author: C. Cortes
"""
from EUNetInterface import EUNetInterface

class EUNetMap:

    def __init__(self, IP, port, configFile):
        """
        This class intends to manage the distribution 
        of information to the devices in the servers.
        It deals with device Names and properties.
        """
        self.IP = IP
        self.port = int(port)
        self.configFile = configFile
        self.devList = self.setDevList()
        self.theInterface = EUNetInterface( [self.IP, self.port], self.configFile)
       
    def setDevList(self):
        """
        Reads the configFile and parses the values
        on the device list
        """
        devList = []
        try:
            devs = self.readCsvFile(self.configFile)
            for d in devs:
                for i in range(2,5): d[i] = int(d[i])
                for i in range(6,8): d[i] = float(d[i])
            return devs
        except:
            print('Could not read the ConfigFile: {}'.format(self.configFile))
        
    def devProperty_to_crCaCh(self, devName, prop):
        """
        Given a device and property it returns the Crate,
        Card and Channel
        """
        for d in self.devList:
            if (devName == d[0] and prop == d[1]):
                return d[2:6],d[6:]
        return False
        
    def crCaCh_to_devProperty(self, crCaCh):
        """
        Given a Crate, Card and Channel it returns a
        devProperty
        """
        cr = crCaCh[0]
        ca = crCaCh[1]
        ch = crCaCh[2]
        for d in self.devList:
            dCrCaCh = d[2:5]
            minMaxRange = d[5:]
            dCr = dCrCaCh[0]
            dCa = dCrCaCh[1] 
            dCh = dCrCaCh[2]
            if (cr == dCr and ca == dCa and ch == dCh):
                return d[:2]
        return False

    def setValue(self, devName, prop, dValue):
        """
        Cross checks that the device prop exits 
        and that the device is configured for input
        """
        # TODO: Implement a work around if the value is too high or too low
        crCaCh, minMaxRange = self.devProperty_to_crCaCh(devName, prop)
        inRange = dValue <= minMaxRange[1]*0.01 and dValue >= minMaxRange[0]*0.01
        if(crCaCh == False): raise Exception('Property not found!')
        if(crCaCh[3] == 'output' and inRange):
            self.theInterface.setValue(dValue, crCaCh[:-1])
        else:
            if(not(inRange)):
                raise Exception('Value not in range')
            raise Exception('Device is configured for input only')

    def getValue(self, devName, prop):
        """
        Returns the values read from the client.
        If an specific Crate, Card, Channel wants to be addressed
        it has to be given as argument
        """
        crCaCh, minMaxRange = self.devProperty_to_crCaCh(devName, prop)
        if(crCaCh == False): raise Exception('Property not found!')
        if(crCaCh[3] == 'input'):
            return self.theInterface.getCurrentValue(crCaCh[:-1])
        raise Exception('Device is configured for output only')

    def isInDeviceList(self, devName):
        """
        Returns true if the device was found in the config file.
        """
        # Is the double check necessary?
        for d in self.devList:
            if devName == d[0]: return True
        return False   

    def readCsvFile(self, theFile):
        """
        Reads the deviceConfigFile.csv with format:
        deviceName  Property  Crate  Card  Channel  I/0  Min  Max
        """
        import csv
        devProps = []
        with open( theFile ) as csvFile:
            csvBuffer = csv.reader( csvFile, delimiter=',' )
            for line in csvBuffer:
                if(len(line)>0):
                    server = line[0]
                    if '#' in server: pass
                    else: devProps.append(line)
        return devProps

    def close(self): self.theInterface.close()   
