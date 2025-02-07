import socket
import json


#Use IP address of Socket server and non-privileged port >1023
addr=('192.168.0.100',4444)

s=socket.socket()
s.connect(addr)
x="Hallo"

#data = json.dumps(x).encode() 
data= bytes(f"{x}","utf-8")
s.sendall(data)
#data = s.recv(1024)

#print("Received "+str(data,"utf-8"))
s.close()
