import socket
from time import sleep

UDP_IP = "169.254.205.7"  # LAN Network address goes here
UDP_PORT = 5000           # May need to change

server = ("169.254.97.171", 5001)

# data = "1"  # Will be sent over cable

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # (IPv4, UDP)
s.bind((UDP_IP, UDP_PORT))

while 1:
    data, addr = s.recvfrom(1024)
    print("from: ") + str(addr)
    print("received: " + str(data))
    print("sending: " + str(data))
    s.sendto(data.encode('utf-8'), data, addr)
    print("sent")

