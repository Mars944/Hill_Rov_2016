import socket


# CLIENT

UDP_IP = "192.168.1.10"  # LAN Network address goes here
UDP_PORT = 5001

server = ('192.168.1.11', 5000)  # IP of server, port

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # (IPv4, UDP)
s.bind((UDP_IP, UDP_PORT))

data = "1"

count =0
while 1:
    if count != 0:
        data = data.decode('utf-8')
    else:
        count+=1
    s.sendto(data.encode('utf-8'), server)
    data, addr = s.recvfrom(1024)
    print(data.decode('utf-8')
