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
    
    def get(self, devName):
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
        
    def setGlobalConfig(self):
        globalConfigFile = 'global.yaml'
        return self.configFolder + globalConfigFile

    def initClients(self):
        """
        Initializes the clients data
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
        self._connectClients()

    def _connectClients(self):
        """
        Initializes the connection
        """
        for clientName in self.clientNameList:
            client = self.clients[clientName]
            client.connect()

    def getValue(self, devName):
        # Looks for the client who has the device
        clientName = self._getClientName(devName)
        if clientName:
            return self._readDeviceInfo(devName, clientName)
        else:
            raise Exception('Device not found')

    def _getClientName(self, devName):
        for clientName in self.clientNameList:
            devices = self.clientsDevices[clientName]
            if devName in devices: return clientName
        print('Warning: Device not found')
        return False

    def _readDeviceInfo(self, devName, clientName):
        client = self.clients[clientName]
        clientDevices = self.clientsDevices[clientName]
        
        device  = clientDevices[devName]
        element = device['element']
        elementType = device['type']
        
        if element == 'Dipole':
            devInfo = device['istWert']
        elif element == 'Quadrupole':
            if elementType == 'magnetisch':
                devInfo = device['istWert']
            else:
                devInfo = device['horizontal']
                devInfo = devInfo['istWert']
        elif element == 'Quadrupole_kicker':
            devInfo = device['horizontal']
            devInfo = devInfo['istWert1']
        else:
            raise Exception('Element not yet implemented')

        crate   = devInfo['crate']
        card    = devInfo['card']
        channel = devInfo['channel']
        read, rawValue = client.getValue(crate, card, channel)
        if device['min'] < 0. :
            value = rawValue - 0.5
            value = 2*value*device['max']
        else:
            value = rawValue*device['max']
        return value
        
    def readDeviceList(self, deviceListPath):
        data = readYamlFile(deviceListPath)
        return data

    def getDevicesInfo(self, clientName):
        return self.clientsDevices[clientName]

    def closeSession(self):
        """
        Terminates all the connections to the servers. 
        """
        print('Closing session')
        for clientName in self.clientNameList:
            client = self.clients[clientName]
            client.close()

    def setValue(self, devName, dValue):
        # TODO: Implement set function
        pass
