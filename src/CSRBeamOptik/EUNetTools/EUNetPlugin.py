from CSRBeamOptik.EUNetTools.EUNetClient import EUNetClient


class EUNetPlugin:

    def __init__(self):
        """
        This class simplifies the connection to the devices
        by offering the straight-forward functionability.
        The user only has to know the name of the devices.
        """
        self.manager = EUNetManager()
        
    def set(self, devName, value):
        self.manager.setValue(devName, value)
    
    def get(self, devName, prop):
        return self.manager.getValue(devName)

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
        self.clientsDevices = {}
        self.initClients()
        self.test()
        self.closeSession()

    def setGlobalConfig(self):
        globalConfigFile = 'global.yaml'
        return self.configFolder + globalConfigFile

    def initClients(self):
        """
        Initializes the maps which then have access to
        the client and devices specified in the global config
        """
        from CSRBeamOptik.util.loadFiles import readYamlFile
        clientList       = {}
        clientDeviceList = {}
        clientGlobalData = readYamlFile(self.globalConfig)
        
        for clientName in clientGlobalData:
            clientData = clientGlobalData[clientName]
            clientIP   = clientData['IP']
            clientPort = clientData['Port']
            clientDeviceListPath = self.configFolder + clientData['deviceList']

            newClient     = EUNetClient(clientIP, clientPort)
            clientDevices = readYamlFile(clientDeviceListPath)

            clientList.update({clientName : newClient} )
            clientDeviceList.update({clientName : clientDevices})

        self.clientNameList = list(clientList.keys())
        self.clients        = clientList
        self.clientsDevices = clientDeviceList
        self.connectClients()

    def connectClients(self):
        print('   Connecting with clients')
        for clientName in self.clientNameList:
            client = self.clients[clientName]
            client.connect()

    def getValue(self, devName):
        clientName = self._getClientName(devName)
        client     = self.clients[clientName]
        devices    = self.clientsDevices[clientName]
        device     = devices[devName]
        readInfo   = device['istWert']
        crate      = readInfo['crate']
        card       = readInfo['card']
        channel    = readInfo['channel']
        return client.getValue(crate,card,channel)

    def _getClientName(self, devName):
        for clientName in self.clientNameList:
            devices = self.clientsDevices[clientName]
            if devName in devices: return clientName
        print('Warning: Device not found')
        
    def setValue(self, devName, prop, dValue):
        m = self.isInDeviceList(devName)
        if m[0]: m[1].setValue(devName, prop, dValue)
        else: raise Exception('Device not found')

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

    def closeSession(self):
        """
        Terminates all the connections to the servers. 
        """
        print('Closing session')
        for clientName in self.clientNameList:
            client = self.clients[clientName]
            client.close()

    def test(self):
        dipole1 = 'D1'
        dipole2 = 'D2'
        print('  Getting some values')
        print(self.getValue(dipole1))
        print(self.getValue(dipole2))
