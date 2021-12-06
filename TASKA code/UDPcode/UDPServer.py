import socket
import sys
import math

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

    if a_list[0] == 0.0:
        # 0 = the tracker that is the main rotation 
        tracker_old = a_list[1-4]
        clientMsg = "Message from Client tracker info: {}".format(tracker_old)
        print(clientMsg)
    else:
        # 1 = tracker or calibrator/the one on the forearm
        calibrator_old = a_list[1-4]
        clientMsg = "Message from Client calibrator info: {}".format(calibrator_old)
        print(clientMsg)
    
    tracker = tracker_old
    calibrator = calibrator_old

    if tracker - tracker_old != 0 and calibrator - calibrator_old != 0:
        # do calculation of euler angles and do calculation
        print('poop')


        
    #clientIP = "Client IP Address: {}".format(address)

    #calculate the roll,pitch,yaw

    #calculate rotation matrix elements
    # Sending reply to client
    # UDPServerSocket.sendto(bytestoSend, address)

UDPServerSocket.close()