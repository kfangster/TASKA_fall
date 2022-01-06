import time
import serial

import numpy as np

from serial import Serial

import sys

import bluetooth

from TASKA import TASKA
from ActiveWrist import ActiveWrist

#Need to create a new class that has all these inits and these inits have self.TASKA
#Now when calling anything from TASKA or ActiveWrist you have to use things like self.Taska.publish() to do so
#Try to do everything that Becca wanted and place it into the Class now, no need for util

class Positional():

    def __init__(self,com = 'COM3', macT = '68:0a:e2:74:67:62', macA = 'ec:fe:7e:1d:8e:a1', elbow = False):
        #calling TASKA and ActiveWrist into class as objects
        self.TASKA = TASKA(com = com, mac = macT)
        #to do add a current limit 
        self.ActiveWrist = ActiveWrist(mac = macA, elbow = elbow)

    def test_command(self, cmd): 
        self.ActiveWrist.publish(cmd)
    def send_command(self, cmd = "rest", move = None, prop = 1.0, angles = None, speed = 1.0 ):
        
        wristmoves = ['rest','pronate', 'supinate', 'elbow_flex', 'elbow_extend']
        taskamoves = [ 'interim', 'relaxed', 'open', 'keyboard', 'dondoff',
              'pointer', 'key', 'opposition', 'handshake', 'tripod',
              'mug_close', 'pincer', 'tablet', 'flex', 'precision',
              'grab_go', 'mouse', 'active_index_1', 'active_index_2',
              'custom_1', 'custom_2', 'custom_3', 'custom_4', 'custom_5' ]
        # mapping of the angles to a degree format
        # 20 degrees = 0 fully extended
        # 80 degrees = 1 fully closed
        angles = [min(max(20, angle), 80) for angle in angles ]
        # convert back to percentage with respect to 20 being 0% and 80 being 100% (linear)
        angles = [(angles[0]-20)/60,(angles[1]-20)/60,(angles[2]-20)/60,(angles[3]-20)/60,(angles[4]-20)/60,(angles[5]-20)/60]

        if cmd == "rest":

            
            self.TASKA.publish(move = move, prop = prop, angles = angles, speed = speed)
           
            self.ActiveWrist.publish( wristmoves[0] )
  
        elif cmd == "pronate":

            
            self.TASKA.publish(move = move, prop = prop, angles = angles, speed = speed)

            self.ActiveWrist.publish( wristmoves[1] )

            
            #self.ActiveWrist.publish( wristmoves[0] ) 

        elif cmd == "supinate":

            
            self.TASKA.publish(move = move, prop = prop, angles = angles, speed = speed) 

            self.ActiveWrist.publish( wristmoves[2] )

            

            #self.ActiveWrist.publish( wristmoves[0] ) 
        else:
            print("NO KNOWN POSITIONS TRY AGAIN")    

