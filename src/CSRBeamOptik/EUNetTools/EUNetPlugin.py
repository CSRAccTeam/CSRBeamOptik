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
        # TODO: Implement in a more cleaner way
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

    def _readDeviceValue(self, devName, clientName):
        """
        Returns the device physical value. Takes into consideration
        if the channel is bipolar and its defined, max&min value.
        """
        clientDevs = self.clientsDevices[clientName]
        device     = clientDevs[devName]
        rawValue   = self._readRawValue(devName, clientName)

        if device['min'] < 0. :
            value = rawValue - 0.5
            value = 2*value*device['max']
        else:
            value = rawValue*device['max']
        return value

    specialElements = ['Quadrupole_elektro','Quadrupole_kicker']

    def _readRawValue(self, devName, clientName):
        """
        Returns the channel raw value from 0.0 to 1.0
        """
        client     = self.clients[clientName]
        clientDevs = self.clientsDevices[clientName]
        device     = clientDevs[devName]
        element    = device['element']
        elementType = device['type']

        isNotSpecial = not (element in self.specialElements)
        # User-defined element reading
        try:
            if isNotSpecial:
                devInfo = device['istWert']
            else:
                devInfo = device['horizontal']
                devInfo = devInfo['istWert']
        except KeyError:
            print(element)
            print(elementType)
        except RuntimeError:
            print(element)
            print(elementType)
            raise Exception('Element not yet implemented')

        crate   = devInfo['crate']
        card    = devInfo['card']
        channel = devInfo['channel']
        wasRead, rawValue = client.getValue(crate, card, channel)

        if wasRead:
            return rawValue

        return

    def setValue(self, devName, dValue):
        # TODO: Implement set function
        clientName = self._getClientName(devName)
        client     = self.clients[clientName]
        clientDevs = self.clientsDevices[clientName]

        device  = clientDevs[devName]
        element = device['element']

        isNotSpecial = not (element in self.specialElements)

        if isNotSpecial:
            devInfo = device['sollWert']
            crate   = devInfo['crate']
            card    = devInfo['card']
            channel = devInfo['channel']

            client.setValue(crate, card, channel, dValue)
        # Sadly this must be done by hand
        else:
            self.setSpecialValue(client, device, dValue)

    def setSpecialValue(self, client, device, dValue):

        elem = device['element']
        unit = device['unit']
        minVal = device['min']
        maxVal = device['max']

        if unit == 'kV':
            dValue /= 1e3

        if elem == 'Quadrupole_elektro':
            print()
            print('Elektrostatischer Quadrupol')
            print()
            info   = device['horizontal']
            setHor = info['sollWert']
            crate  = setHor['crate']
            card   = setHor['card']
            channel = setHor['channel']
            rawValue = self.computeRawValue(minVal, maxVal, dValue)
            #client.setValue(crate, card, channel, dValue)
            print('Set horizontal value: {} kV -> {}'.format(round(dValue,3),
                                                             rawValue))

            info    = device['vertical']
            setVer  = info['sollWert']
            crate   = setVer['crate']
            card    = setVer['card']
            channel = setVer['channel']
            rawValue = self.computeRawValue(minVal, maxVal, -dValue)
            #client.setValue(crate, card, channel, dValue)
            print('Set vertical value: {} kV -> {}'.format(round(-dValue,3),
                                                           rawValue))

        if elem == 'Quadrupole_kicker':
            print()
            print('Elektrostatischer Quadrupol mit Kicker')
            print()
            info   = device['horizontal']
            setHor = info['sollWert1']
            crate  = setHor['crate']
            card   = setHor['card']
            channel = setHor['channel']
            rawValue = self.computeRawValue(minVal, maxVal, dValue/2)
            #client.setValue(crate, card, channel, dValue)
            print('Set horizontal value: {} kV -> {}'.format(round(dValue/2,3),
                                                             rawValue))
            setHor = info['sollWert2']
            crate  = setHor['crate']
            card   = setHor['card']
            channel = setHor['channel']
            rawValue = self.computeRawValue(minVal, maxVal, dValue/2)
            #client.setValue(crate, card, channel, dValue)
            print('Set horizontal value: {} kV -> {}'.format(round(dValue/2,3),
                                                             rawValue))

            info    = device['vertical']
            setVer  = info['sollWert1']
            crate   = setVer['crate']
            card    = setVer['card']
            channel = setVer['channel']
            rawValue = self.computeRawValue(minVal, maxVal, -dValue/2)
            #client.setValue(crate, card, channel, dValue)
            print('Set vertical value: {} kV -> {}'.format(round(-dValue/2,3),
                                                           rawValue))
            setVer  = info['sollWert2']
            crate   = setVer['crate']
            card    = setVer['card']
            channel = setVer['channel']
            rawValue = self.computeRawValue(minVal, maxVal, -dValue/2)
            #client.setValue(crate, card, channel, dValue)
            print('Set vertical value: {} kV -> {}'.format(round(-dValue/2,3),
                                                           rawValue))


    def computeRawValue(self, minVal, maxVal, dVal):
        if minVal < 0.:
            rawVal = dVal/(2*maxVal) + 0.5
        else:
            rawVal = dVal/(2*maxVal)
        return rawVal


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
        Returns a list with ALL device names.
        Should we also build in a getter
        with the available input devices?
        or the output devices? or both?
        """
        return [devName
                for devName in self.clientsDevices[c]
                for c in self.clients]

    def close(self): self.closeSession()
