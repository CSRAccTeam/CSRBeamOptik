# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:07:00 2019
@author: C. Cortes
"""
from EUNetTools.EUNetClient import EUNetClient
import numpy as np
import time

class EUNetInterface:

    def __init__(self, clientIP_Port, crCaChFile):
        """
        This class communicates directly to the server.
        It checks the integrity of the given input and
        handles the exceptions and errors
        """
        self.defaultIP   = clientIP_Port[0]
        self.defaultPort = clientIP_Port[1]
        self.client      = self.initializeClient()
        self.binSize     = 20
        self.sleepTime   = 0.05
        if (self.client.connect()):
            print('Connection stablished with client')
            print('IP: {}'.format(self.defaultIP))
            print('Port: {}'.format(self.defaultPort))
        else:
            raise Exception('Cannot stablish connection to client')
        
    def initializeClient(self):
        """
        Initializes a Default Client to get
        access to the server
        """
        return EUNetClient(self.defaultIP, self.defaultPort)

    def getEUNetClient(self, IP, Port):
        """
        Returns the EUNetClient instance
        """
        return self.client

    def setValue(self, dValue, crCaCh):
        """
        Here the client sets the values into the given 
        crate, card, channel.
        """
        self.client.SetValue(crCaCh[0], crCaCh[1], crCaCh[2], dValue)
        
    def getCurrentValue(self, crCaCh):
        """
        Returns the average value at the given crCaCh
        of binSize reads
        """
        dValbin = []
        iCrate = crCaCh[0]
        iCard  = crCaCh[1]
        iCh    = crCaCh[2]
        for i in range(self.binSize):
            read = self.client.GetValue(iCrate, iCard, iCh)
            if read[0]:
                dValbin.append(read[1])
                time.sleep(self.sleepTime)
            else:
                raise Exception('Error while reading the value')
        #np.savetxt('cupStromReads.txt',dValbin)
        return [True, np.mean(dValbin)]

    def close(self): self.client.close()
