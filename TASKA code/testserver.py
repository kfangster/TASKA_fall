import socket
import sys
import math
import Quaternion
from Quaternion import _AXES2TUPLE, relative, to_euler

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
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(buffersize)
    
    #prints the message received from Udpclient
    message = bytesAddressPair[0]
    #address = bytesAddressPair[1]

    #check if data is being received
    if not message:
        break

    #convert message bytes to a list format
    message = message.decode("utf-8")
    a_list = list(map(float,message.split(',')))

    clientMsg = "Message from Client: {}".format(a_list)

    print(clientMsg)
    #first 4 elements are tracker, the last 4 are calibrator
    tracker = a_list[0:4]
    calibrator = a_list[4:8]

    quat_combine = relative(calibrator,tracker)
    print(quat_combine)

    euler_angs = to_euler(quat_combine, axes='sxyz')
    print(euler_angs)
    #clientIP = "Client IP Address: {}".format(address)

    #calculate the roll,pitch,yaw

    #calculate rotation matrix elements
    # Sending reply to client
    # UDPServerSocket.sendto(bytestoSend, address)

UDPServerSocket.close()