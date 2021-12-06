import socket
import sys

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

print(socket.gethostname())

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(buffersize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client: {}".format(message)
    cleintIP = "Client IP Address: {}".format(address)

    print(clientMsg)
    print(cleintIP)

    # Sending reply to client
    UDPServerSocket.sendto(bytestoSend, address)
    