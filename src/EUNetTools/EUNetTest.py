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

    from EUNetGlobal import EUNetPlugin
    import time
    
    plugin = EUNetPlugin()
    sleepTime = 0.5

    #### CUP STROM READ #####
    werte = []
    print('Cup Strom Read:')
    for i in range(10):
        v = plugin.get('cupStrom', 'istWert')
        if v[0]:
            print(v[1])
            werte.append(v[1])
        else:
            print('NO READ!!!')
        time.sleep(sleepTime)
        
    import matplotlib.pyplot as plt
    plt.plot(werte,marker='.')
    plt.show()
    
    """
    for i in range(3):

        #### ROLFS SERVER #####
        
        print('Setting channel {} with {}'.format(i,1))
        plugin.set('outputcard', 'ch{}'.format(i), 1)
        # Should we force the sleep time directly on the implementation?
        # Answer: Maybe yes, optimal time for reading after setting values t = 0.5s
        time.sleep(sleepTime)

        print('Reads:')
        for i in range(16):
            v = plugin.get('inputcard', 'ch{}'.format(i))
            if v[0]:
                print('ch{}'.format(i), v[1])
            else:
                print('NO READ!!!')
    
    for i in range(10):
        plugin.set('outputcard', 'ch{}'.format(i), 0.0)
    print('Reads:')
    for i in range(16):
        v = plugin.get('inputcard', 'ch{}'.format(i))
        if v[0]:
            print('ch{}'.format(i), v[1])
        else:
            print('NO READ!!!')

    print('Cup Strom Read:')
    v = plugin.get('cupStromRead', 'ch15')
    if v[0]: print(v[1])
    else: print('NO READ!!!')
    time.sleep(sleepTime)
    """
    plugin.close()
    
crisTest()
