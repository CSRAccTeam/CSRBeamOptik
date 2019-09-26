# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:36:24 2019
@author: Rolf Epking
"""
import socket

def CBSetValueDefault(iCrate,iCard,iCh,dValue):
    print("Received SetValue: Crate: " + str(iCrate) + " Card: " + str(iCard) + " Channel: " + str(iCh) + " Value: " + str(dValue))

def CBErrorDefault(Message):
    print("Error received: " + Message )
    
class EUNetClient:

    def __init__(self, IP, Port):
        print('Initializing client')
        self._IP   = IP
        self._Port = Port
        self._MySocket   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._CBSetValue = CBSetValueDefault
        self._CBError    = CBErrorDefault

    def __eq__(self, other):
        """
        Definiton (overload) of the equality operator for EUNetCLients
        """
        if(self._IP == other._IP and self._Port == other._Port):
            return True
        return False
    
    def connect(self):
        try:
            self._MySocket.connect((self._IP,self._Port))
            self._MySocket.settimeout(3); #3 sek timeout
            self._MySocket.send(b"TEXT\n")
            return True
        except socket.timeout:
            print("Timeout connecting " + self._IP)
            return False
        except OSError as err:
            print("Error connecting: " + err.strerror)
            return False
        
    def close(self):
        self._MySocket.shutdown(socket.SHUT_RDWR)
        self._MySocket.close()
    
    def SetValue(self,iCrate,iCard,iCh,dValue):
        try:
            self._MySocket.send(bytes("SET_WERT " + str(iCrate) + " " + str(iCard) + " " + str(iCh) + " " + str(dValue) + "\n", 'utf-8'))
            return True
        except socket.timeout:
            print("Timeout while sending Set_WERT " + self._IP)
            return False
        # Is this really an Operative System Error?
        except OSError as err:
            print("Error while sending Set_WERT: " + err.strerror)
            return False
        
    def SetBitfeld(self,iCrate,iCard,iCh,iBitfeld):
        try:
            self._MySocket.send(bytes("SET_BITFELD " + str(iCrate) + " " + str(iCard) + " " + str(iCh) + " " + str(iBitfeld) + "\n", 'utf-8'))
            return True
        except socket.timeout:
            print("Timeout while sending SET_BITFELD " + self._IP)
            return False
        # Is this really an Operative System Error?
        except OSError as err:
            print("Error while sending SET_BITFELD: " + err.strerror)
            return False
    
    def SetCBSetValue(self,SETValueCB):
        """ 
        Sets a CallBack-Function which will be called, when receiving a 'SET_WERT'
        (information for clients, that a set-value is set)
        """
        self._CBSetValue=SETValueCB  
        
    def SetCBError(self,ErrorCB):
        self._CBError=ErrorCB  
        
    def _GetLineFromSocket(self):
        SingleChar= b""
        Line= b""
        while SingleChar != b"\n":
            SingleChar = self._MySocket.recv(1)
            if SingleChar !=  b"\n":
                Line = Line + SingleChar
        
        return str(Line,'utf-8')
  
    def _CheckForMessage(self, InputString):
        """
        Check given String for PING and Error Messages - returns Tupel with Value and String
        If Value > 0 Then it is an error(1) or message(2) - on Ping the returned string is empty.
        If any Keyword found it returns 0 and the given String
        """
        if InputString[:5] == "PING": 
            return (0,"")
        elif InputString[:10] == "SET_FEHLER":
            return (1,InputString[11:])
        elif InputString[:11] == "SET_NACHRICHT":
            return (2,InputString[:14])
        else :
            return (0,InputString)
        
        
    def _CheckForSet_WERT(self,InputString):
        """
        Returns Tupel ErrNo and String
        ErrNo = -1 Parsing Error 
        ErrNo = 0 No SetWert - String forwarded
        ErrNo = 1 SetValue processed - empty string forwarded
        """
        if  InputString[:8] == "SET_WERT" :
            tokens = InputString.split(" ")
            tokens = list(filter(None,tokens))
            #https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
            if len(tokens) == 5:
                self._CBSetValue(int(tokens[1]),int(tokens[2]), int(tokens[3]), float(tokens[4]))
                return (1,"")
            else :
                return (-1,"Parsing Error from :\"" + InputString +  "\"")
        else :
            return (0, InputString)

    def GetValue(self,iCrate,iCard,iCh):
        """
        Returns tupel of boolean and Value
        """
        try:
            self._MySocket.send(bytes("GET_WERT " + str(iCrate) + " " + str(iCard) + " " + str(iCh)  + "\n", 'utf-8'))
            # Is the while loop really necessary ? 
            while True:
                (errNo,Line) = self._CheckForMessage(self._GetLineFromSocket())
                if errNo > 0:
                    self._CBError(Line)
                    return (False, 0.0)
                else:
                    (errNo,Line) = self._CheckForSet_WERT(Line)
                    if errNo < 0 :
                        print (Line)
                        return (False, 0.0)
                    elif errNo == 0:
                        tokens = Line.split(" ")
                        tokens = list(filter(None,tokens))
                        #https://stackoverflow.com/questions/3845423/
                        #remove-empty-strings-from-a-list-of-strings
                        if len(tokens) == 5:
                            if tokens[0] == "PUT_WERT" and \
                            int(tokens[1]) == int(iCrate) and \
                            int(tokens[2]) == int(iCard) and \
                            int(tokens[3]) == int(iCh) :
                                return (True, float(tokens[4]))
                            else:
                                print("Got Values I didn't Ask for: " + Line)
                                return (False, 0.0)
                    #errNo > 1  -> neue Zeile lesen
                
        except socket.timeout:
            print("Timeout while sending GET_WERT or waiting for answer " + self._IP)
            return (False, 0.0)
        except OSError as err:
            print("Timeout while sending GET_WERT or waiting for answer : " + err.strerror)
            return (False, 0.0)
                      
        

    def GetBitfeld(self,iCrate,iCard,iCh):
        """
        Returns tupel of boolean and Value
        """
        try:
            self._MySocket.send(bytes("GET_BITFELD " + str(iCrate) + " " + str(iCard) + " " + str(iCh)  + "\n", 'utf-8'))
    
            while True:
                (errNo,Line) = self._CheckForMessage(self._GetLineFromSocket())
                if errNo > 0:
                    self._CBError(Line)
                    return (False, 0)
                else:
                    (errNo,Line) = self._CheckForSet_WERT(Line)
                    if errNo < 0 :
                        print (Line)
                        return (False, 0)
                    elif errNo == 0:
                        tokens = Line.split(" ")
                         # For reference look at:
                         #https://stackoverflow.com/questions/3845423/
                         #remove-empty-strings-from-a-list-of-strings
                        tokens = list(filter(None,tokens))
                        if len(tokens) == 5:
                            if tokens[0] == "PUT_BITFELD" and \
                            int(tokens[1]) == int(iCrate) and \
                            int(tokens[2]) == int(iCard) and \
                            int(tokens[3]) == int(iCh) :
                                return (True, int(tokens[4]))
                            else:
                                print("Got Values I didn't Ask for: " + Line)
                                return (False,0)
                    #errNo > 1  -> neue Zeile lesen
                
        except socket.timeout:
            print("Timeout while sending GET_WERT or waiting for answer " + self._IP)
            return (False, 0)
        except OSError as err:
            print("Timeout while sending GET_WERT or waiting for answer : " + err.strerror)
            return (False, 0)
                      
