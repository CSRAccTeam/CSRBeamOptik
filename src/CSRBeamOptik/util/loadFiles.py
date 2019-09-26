from yaml import safe_load
from csv  import reader as csvReader

def readCsvFile(theFile, comment='#'):
    """
    Reads the global config file and returns an array 
    with the IPs, Ports and configFiles
    GlobalConfig.csv has the format:
    IP  Port  DeviceConfigFileName
    """
    #TODO: Implement this method in a util.py class
    clients = []
    with open(theFile) as csvFile:
        csvBuffer = csvReader(csvFile, delimiter=',')
        for line in csvBuffer:
            if(len(line)>0):
                server = line[0]
                if comment in server: pass
                else: clients.append(line)
    return clients

def readYamlFile(theFile):
    with open(theFile, 'rb') as f:
        return safe_load(f)
