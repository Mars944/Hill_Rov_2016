import socket

UDP_IP   = "localhost"
UDP_PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((UDP_IP, UDP_PORT))

while 1:
    data = int(s.recv(8).decode('utf-8')) #(bytes received)
    print(data+1)
