import socket
import sys
import math

from Quaternion import _AXES2TUPLE, relative, to_euler

import time
import serial

import numpy as np

from serial import Serial

import sys

import bluetooth

from TASKA import TASKA
from ActiveWrist import ActiveWrist
from Positional import Positional

# might need a user input for pronate/supinate
proorsup = str.lower(input('Enter Pronate or Supinate?: '))
if proorsup != 'pronate' and proorsup != 'supinate':
    print('Option Entered is not viable try again')

localIP = "127.0.0.1"
localPort = 20001
buffersize = 1024

msgFromServer = "Hello UDP Client"
bytestoSend = str.encode(msgFromServer)

# Create a socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server is booted and ready")

# Listen for incoming datagrams

hand = Positional()

## Get initial position 
bytesAddressPair = UDPServerSocket.recvfrom(buffersize)

message = bytesAddressPair[0]

#convert message bytes to a list format
message = message.decode("utf-8")
a_list = list(map(float,message.split(',')))

clientMsg = "Message from Client: {}".format(a_list)
print (clientMsg)

#first 4 elements are tracker, the last 4 are calibrator
tracker = a_list[0:4]
calibrator = a_list[4:8]

#calculate euler angles for relative AND source
quat_combine = relative(calibrator,tracker)
euler_angs = to_euler(quat_combine, axes='sxyz')
tracker_angs = to_euler(tracker, axes = 'sxyz')

# need a way to determine which of the 3 angles is the "roll" let's assume the x is roll

target_value = -1

#choose pronate or supinate here based on euler angle orientation
hand.test_command(proorsup) 
print('Initial error: ', abs(target_value - euler_angs[0]))

while(abs(target_value - euler_angs[0]) > 0.1): #change 0.01 radians error empirically
        print('Current error: ', abs(target_value - euler_angs[0]))

        bytesAddressPair = UDPServerSocket.recvfrom(buffersize)
        #prints the message received from Udpclient
        message = bytesAddressPair[0]

        #convert message bytes to a list format
        message = message.decode("utf-8")
        a_list = list(map(float,message.split(',')))

        clientMsg = "Message from Client: {}".format(a_list)
        print(clientMsg)

        #first 4 elements are tracker, the last 4 are calibrator
        tracker = a_list[0:4]
        calibrator = a_list[4:8]

        #calculate euler angles for relative AND source
        quat_combine = relative(calibrator,tracker)

        euler_angs = to_euler(quat_combine, axes='sxyz')
        print(euler_angs)
hand.test_command('rest')

UDPServerSocket.close()