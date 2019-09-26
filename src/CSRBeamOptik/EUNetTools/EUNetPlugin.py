from CSRBeamOptik.EUNetTools.EUNetClient import EUNetClient


class EUNetPlugin:

    def __init__(self):
        """
        This class simplifies the connection to the devices
        by offering the straight-forward functionability.
        The user only has to know the name of the devices.
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

    def close(self): self.manager.closeSession()

        
class EUNetManager:

    def __init__(self):
        """
        The EUNetManager connects to the user defined servers
        and controls the communication with the clients
        """
        self.configFolder   = '/home/blm/ccortes/MPIK/CSR/CSRBeamOptik/configFiles/'
        self.globalConfig   = self.setGlobalConfig()
        self.clientNameList = []
        self.clients        = {}
        self.clientDevices  = {}
        self.initClients()

    def setGlobalConfig(self):
        globalConfigFile = 'global.yaml'
        return self.configFolder + globalConfigFile

    def initClients(self):
        """
        Initializes the maps which then have access to
        the client and devices specified in the global config
        """
        from CSRBeamOptik.util.loadFiles import readYamlFile, readCsvFile
        clientList       = {}
        clientDeviceList = {}
        clientGlobalData = readYamlFile(self.globalConfig)
        
        for clientName in clientGlobalData:
            
            clientData = clientGlobalData[clientName]
            clientIP   = clientData['IP']
            clientPort = clientData['Port']
            clientDeviceListPath = self.configFolder + clientData['deviceList']

            newClient  = EUNetClient(clientIP, clientPort)
            clientDevices = readCsvFile(clientDeviceListPath)

            clientList.update({clientName : newClient} )
            clientDeviceList.update({clientName : clientDevices})
            
        self.clientNameList = list(clientList.keys())
        self.clients        = clientList
        c1 = self.clientNameList[0]

    def readDeviceList(self, deviceListPath):
        
        data = readYamlFile(deviceListPath)
        return data
        
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
        print('Closing session')
        for clientName in self.clientNameList:
            client = self.clients[clientName]
            client.close()
