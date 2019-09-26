# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 11:27:13 2019
@author: Rolf
"""

def rolfsTest():

    from EUNetClient import EUNetClient
    import time
    MyEUC = EUNetClient("149.217.7.216", 20000)
    if MyEUC.connect():
        ui=0
        for i in range(10):
            if ui == 0 or ui == pow(2,16): ui = 1
            else: ui *= 2
            """
            Is it necessary to set a bit field on the crate
            in order to set a value?
            """
            MyEUC.SetBitfeld(1,8,0,ui)
            for value in range(0,10):
                MyEUC.SetValue(1,2,0,value/100.0)
                time.sleep(0.5)
                (Err, Value) = MyEUC.GetValue(1,7,0)
                if Err:
                    print(Value)
                else:
                    print("Error")
                    """
                    MyEUC.close()
                    print("Try to reconnect...")
                    while True:
                    if MyEUC.connect() == True: break
                    else: print("failed to connect")
                    """
            MyEUC.close()            
    
        else:
            print("Connect failed!")


def crisTest():

    from EUNetPlugin import EUNetPlugin
    import time
    
    plugin = EUNetPlugin()
    sleepTime = 0.5

    #### DIPOLE D1 READ #####
    werte = []
    print('Dipole Magnets Reads:')
    for i in range(10):
        v = plugin.get('D2', 'istWert')
        if v[0]:
            print(v[1])
            werte.append(v[1])
        else:
            print('NO READ!!!')
        time.sleep(sleepTime)
        
    import matplotlib.pyplot as plt
    plt.plot(werte,marker='.')
    plt.show()
    plugin.close()
    
crisTest()
