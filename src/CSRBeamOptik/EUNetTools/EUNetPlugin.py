from CSRBeamOptik.EUNetTools.EUNetClient import EUNetClient


class EUNetManager:

    def __init__(self):
        """
        The EUNetManager connects to the user defined servers
        and controls the communication with the clients
        """
        self.configFolder   = '/home/cristopher/MPIK/CSRBeamOptik/configFiles/'
        self.globalConfig   = self.setGlobalConfig()
        self.clientNameList = []
        self.clients        = {}
        self.clientsDevices = {}
        self.isConnected    = False
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
        isConnected = False
        for clientName in self.clientNameList:
            client = self.clients[clientName]
            isConnected += client.connect()
        self.isConnected = isConnected

    def getValue(self, devName, raw=False):
        # Looks for the client who has the device
        clientName = self._getClientName(devName)
        if clientName:
            if not raw:
                return self._readDeviceValue(devName, clientName)
            else:
                return self._readRawValue(devName, clientName)
        else:
            raise Exception('Device not found')

    def _getClientName(self, devName):
        for clientName in self.clientNameList:
            devices = self.clientsDevices[clientName]
            if devName in devices: return clientName
        print('Warning: Device not found')
        return False

    def readDeviceList(self, deviceListPath):
        data = readYamlFile(deviceListPath)
        return data

    def getDevicesInfo(self, clientName):
        return self.clientsDevices[clientName]

    def closeSession(self):
        """
        Terminates all the connections to the servers.
        """
        for clientName in self.clientNameList:
            client = self.clients[clientName]
            client.close()

    def setValue(self, devName, dValue):
        # TODO: Implement set function
        clientName = self._getClientName(devName)

        client = self.clients[clientName]
        clientDevices = self.clientsDevices[clientName]
        device  = clientDevices[devName]
        element = device['element']
        elementType = device['type']

        if element == 'Deflektor':
            devInfo = device['sollWert']

            crate   = devInfo['crate']
            card    = devInfo['card']
            channel = devInfo['channel']

            client.setValue(crate, card, channel, dValue)

        else:
            pass

    def _readDeviceValue(self, devName, clientName):
        """
        Returns the device physical value. Takes into consideration
        if the channel is bipolar and its defined, max&min value.
        """
        clientDevices = self.clientsDevices[clientName]
        device  = clientDevices[devName]
        rawValue = self._readRawValue(devName, clientName)
        if device['min'] < 0. :
            value = rawValue - 0.5
            value = 2*value*device['max']
        else:
            value = rawValue*device['max']
        return value

    def _readRawValue(self, devName, clientName):
        """
        Returns the channel raw value from 0.0 to 1.0
        """
        client = self.clients[clientName]
        clientDevices = self.clientsDevices[clientName]
        device  = clientDevices[devName]
        element = device['element']
        elementType = device['type']
        # User-defined element reading
        if element == 'Dipole':
            devInfo = device['istWert']
        elif element == 'Quadrupole':
            if elementType == 'magnetisch':
                devInfo = device['istWert']
            elif elementType == 'elektroCSR':
                devInfo = device['istWert']
            else:
                devInfo = device['horizontal']
                devInfo = devInfo['istWert']
        elif element == 'Quadrupole_kicker':
            devInfo = device['horizontal']
            devInfo = devInfo['istWert1']
        elif element == 'Deflektor':
            if elementType == 'elektrostatisch':
                devInfo = device['istWert']
            elif elementType == 'elektrostatisch_kicker':
                devInfo = device['innen']
                devInfo = devInfo['istWert']
        elif element == 'Steerer':
            devInfo = device['istWert']
        else:
            print(element)
            print(elementType)
            raise Exception('Element not yet implemented')

        crate   = devInfo['crate']
        card    = devInfo['card']
        channel = devInfo['channel']

        client = self.clients[clientName]
        clientDevices = self.clientsDevices[clientName]
        device  = clientDevices[devName]
        crate   = devInfo['crate']
        card    = devInfo['card']
        channel = devInfo['channel']
        read, rawValue = client.getValue(crate, card, channel)
        return rawValue


class EUNetPlugin(EUNetManager):

    def __init__(self):
        """
        This class simplifies the connection to the devices
        by offering the straight-forward functionability.
        The user only has to know the name of the devices.
        The raw values are returned (0. to 1.).
        """
        super().__init__()

    def set(self, devName, value):
        # TODO: Implement setter
        self.setValue(devName, value)

    def get(self, devName):
        return self.getValue(devName, raw=True)

    def getDeviceList(self):
        """
        Returns a list with ALL devices name.
        Should we also build in a getter
        with the available input devices?
        or the output devices? or both?
        """
        allDevices = []
        for c in self.clients:
            for devName in self.clientsDevices[c]:
                allDevices.append(devName)
        return allDevices

    def close(self): self.closeSession()
