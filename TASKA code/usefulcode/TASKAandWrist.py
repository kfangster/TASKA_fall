import time
import serial

import numpy as np

from serial import Serial

import sys

if sys.platform == 'win32': import bluetooth
elif sys.platform == 'linux': import socket
else: raise RuntimeError( 'Bluetooth not supported for this OS:' , sys.platform )

# from . import AbstractBaseOutput

from TASKA import TASKA
from ActiveWrist import ActiveWrist

#mac address for the TASKA 68:0a:e2:74:67:62 at COM3 through dongle
#mac address/things to know for the IBTCoreD8EA1 controller  ec:fe:7e:1d:8e:a1 COM 6

#To create and combine the two different classes from TASKA and Active Wrist a wrapping while loop was written
#The way how it works is an overall wrapping while loop gives the options to choose between TASKA, Wrist or Leave
#Choosing Leave will automatically break the entire loop and go into a print
#Choosing either TASKA or Wrist will go to the endings of the TASKACode and activewristkevin code basically
#The ends of each of those scripts are designed to run the classes. With them being imported into this .py we can easily call them
#In addition to the overall wrapping script, each of these TASKACode and activewristkevin has a built in done = False while loop
#Inside those done = False loops it's similar to the wrapping except the condition instead is q and not Leave.


if __name__ == '__main__':
    import utils

# Call classes outside loop to prevent double bluetooth connections(produces errors)
activewristmov = ActiveWrist( utils.args.mac, utils.args.elbow )
taska = TASKA( utils.args1.com )

# Start while loop for commands of active wrist and TASKA (nested while loops)
# Is there a more efficient way?
done = False
while not done:
    cmd = input('TASKA, Wrist or Leave?:  ')
    if cmd.lower() == 'leave':
        done = True
    elif cmd.lower() == 'taska':
        moves = [ 'interim', 'relaxed', 'open', 'keyboard', 'dondoff',
                'pointer', 'key', 'opposition', 'handshake', 'tripod',
                'mug_close', 'pincer', 'tablet', 'flex', 'precision',
                'grab_go', 'mouse', 'active_index_1', 'active_index_2',
                'custom_1', 'custom_2', 'custom_3', 'custom_4', 'custom_5' ]
        
        print( '------------ Movement Commands ------------' )
        print( '| 00  -----  INTERIM                      |' )
        print( '| 01  -----  RELAXED                      |' )
        print( '| 02  -----  OPEN PALM                    |' )
        print( '| 03  -----  KEYBOARD                     |' )
        print( '| 04  -----  DON DOFF                     |' )
        print( '| 05  -----  POINTER                      |' )
        print( '| 06  -----  KEY                          |' )
        print( '| 07  -----  OPPOSITION                   |' )
        print( '| 08  -----  HANDSHAKE                    |' )
        print( '| 09  -----  TRIPOD                       |' )
        print( '| 10  -----  MUG CLOSE ONLY               |' )
        print( '| 11  -----  PINCER                       |' )
        print( '| 12  -----  ADDUCTION TABLET             |' )
        print( '| 13  -----  FLEX TOOL                    |' )
        print( '| 14  -----  OPPOSITION PRECISION         |' )
        print( '| 15  -----  GRAB N GO                    |' )
        print( '| 16  -----  MOUSE                        |' )
        print( '| 17  -----  ACTIVE INDEX                 |' )
        print( '| 18  -----  ACTIVE INDEX 2               |' )
        print( '| 19  -----  CUSTOM 1                     |' )
        print( '| 20  -----  CUSTOM 2                     |' )
        print( '| 21  -----  CUSTOM 3                     |' )
        print( '| 22  -----  CUSTOM 4                     |' )
        print( '| 23  -----  CUSTOM 5                     |' )
        print( '-------------------------------------------' )
        print( '| Press [Q] to quit!                      |' )
        print( '-------------------------------------------' )

        done1 = False  
        while not done1:
            cmd = input( 'Command: ' )
            if cmd.lower() == 'q':
                done1 = True
            else:
                try:
                    idx = int( cmd )
                    if idx in range( 0, len( moves ) ):
                        taska.publish( moves[ idx ], prop = 1.0 )
                except ValueError:
                    pass
        print( 'Looping back to options' )

    elif cmd.lower() == 'wrist':
        moves = ['rest','pronate', 'supinate', 'elbow_flex', 'elbow_extend']
        
        print( '------------ Movement Commands ------------' )
        print( '| 00  -----  STOP                         |' )
        print( '| 01  -----  PRONATE                      |' )
        print( '| 02  -----  SUPINATE                     |' )
        print( '| 03  -----  ELBOW FLEXION                |' )
        print( '| 04  -----  ELBOW EXTENSION              |' )     
        print( '-------------------------------------------' )
        print( '| Press [Q] to quit!                      |' )
        print( '-------------------------------------------' )

        done2 = False  
        while not done2:
            cmd = input( 'Command: ' )
            if cmd.lower() == 'q':
                done2 = True
            else:
                try:
                    idx = int( cmd )
                    if idx in range( 0, len( moves ) ):
                        activewristmov.publish( moves[ idx ] )
                except ValueError:
                    pass
        print( 'Looping back to options' )
print('Farewell, travel safely')

