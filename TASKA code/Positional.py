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
        self.ActiveWrist = ActiveWrist(mac = macA, elbow = elbow)

    def send_command(self, seconds = 69, cmd = "rest", move = None, prop = 1.0, angles = None, speed = 1.0 ):
        
        wristmoves = ['rest','pronate', 'supinate', 'elbow_flex', 'elbow_extend']
        taskamoves = [ 'interim', 'relaxed', 'open', 'keyboard', 'dondoff',
              'pointer', 'key', 'opposition', 'handshake', 'tripod',
              'mug_close', 'pincer', 'tablet', 'flex', 'precision',
              'grab_go', 'mouse', 'active_index_1', 'active_index_2',
              'custom_1', 'custom_2', 'custom_3', 'custom_4', 'custom_5' ]

        if cmd == "rest":

            seconds = int(seconds)
            self.TASKA.publish(move = move, prop = prop, angles = angles, speed = speed)
           
            self.ActiveWrist.publish( wristmoves[0] )
  
        elif cmd == "pronate":

            seconds = int(seconds)
            self.TASKA.publish(move = move, prop = prop, angles = angles, speed = speed)

            self.ActiveWrist.publish( wristmoves[1] )

            time.sleep(seconds)

            #self.ActiveWrist.publish( wristmoves[0] ) 

        elif cmd == "supinate":

            seconds = int(seconds)
            self.TASKA.publish(move = move, prop = prop, angles = angles, speed = speed) 

            self.ActiveWrist.publish( wristmoves[2] )

            time.sleep(seconds)

            #self.ActiveWrist.publish( wristmoves[0] ) 
        else:
            print("NO KNOWN POSITIONS TRY AGAIN")    

#run code at the bottom
#[1.0,1.0,1.0,1.0,1.0,1.0]
#[0,0,0,0,0,0]
#spider man
hand = Positional() #when calling a function from a class set class to an object to save the variable.

hand.send_command(cmd = "supinate", seconds = 2, move = None, prop = 1.0, angles = [0,1,1,0,0,1], speed = 1.0)

time.sleep(2)

#middle finger
hand.send_command(cmd = "pronate", seconds = 2,  move = None, prop = 1.0, angles = [1,0,1,1,1,1], speed = 1.0)

time.sleep(2)

#open fist stairway_slow
hand.send_command(cmd = "supinate", seconds = 2, move = None, prop = 1.0, angles = [0.7,0.6,0.5,0.4,1,1], speed = 0.5)

time.sleep(2)

#close fist_slow
hand.send_command(cmd = "pronate", seconds = 2, move = None, prop = 1.0, angles = [1,1,1,1,1,1], speed = 0.5)

time.sleep(2)

#open fist completely
hand.send_command(cmd = "rest", seconds = 2, move = None, prop = 1.0, angles = [0,0,0,0,0,0], speed = 1.0)