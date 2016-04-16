import socket
from time import sleep

UDP_IP   = "localhost" # LAN Network address goes here
UDP_PORT = 5000       # May need to change

data = "1" #Will be sent over cable

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #(IPv4, UDP)

while 1:
    s.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT)) #(data to send, (HOST, PORT))
    print("Data sent")
    sleep(1)
