import socket
import sys
import math
import Quaternion
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

s_val = True
hand = Positional()

while(s_val == True):
    bytesAddressPair = UDPServerSocket.recvfrom(buffersize)
    
    #prints the message received from Udpclient
    message = bytesAddressPair[0]
    #address = bytesAddressPair[1]

    #check if data is being received
    if not message:
        s_val = False

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

    euler_angs = to_euler(quat_combine, axes = 'sxyz')
    print(euler_angs)

    tracker_angs = to_euler(tracker, axes = 'sxyz')

    # need a way to determine which of the 3 angles is the "roll" let's assume the x is roll

    # need to check/switch the pronate and supinate based on which direction activewrist turns! try this 
    if sum(tracker[:]) > 0:
        #choose supinate
        s = 'supinate'
        while(abs(tracker_angs[0] - euler_angs[0]) < 0.01): #change 0.01 radians error empirically
            hand.send_command(cmd = "supinate", seconds = 1, move = None, prop = 1.0, angles = [0,0,0,0,0,0], speed = 0.5)
    else:
        #choose pronate
        p = 'pronate'
        while(abs(tracker_angs[0] - euler_angs[0]) < 0.01): #change 0.01 radians error empirically
            hand.send_command(cmd = "pronate", seconds = 1, move = None, prop = 1.0, angles = [0,0,0,0,0,0], speed = 0.5)
    #clientIP = "Client IP Address: {}".format(address)
    #calculate rotation matrix elements
    # Sending reply to client
    # UDPServerSocket.sendto(bytestoSend, address)

UDPServerSocket.close()