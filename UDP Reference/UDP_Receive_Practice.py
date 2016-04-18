import socket


# SERVER

UDP_IP = "192.168.1.11"  # LAN Network address goes here
UDP_PORT = 5000           # May need to change

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # (IPv4, UDP)
s.bind((UDP_IP, UDP_PORT))

while 1:
    data, addr = s.recvfrom(1024)  # Receive data and address from client
    print(str(int(data.decode('utf-8'))+1))
    s.sendto(data, addr)
