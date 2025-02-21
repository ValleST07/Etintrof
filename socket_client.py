import socket
import json

def antwort():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(addr)
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data=conn.recv(1024)
                if not data:
                    break
                data=str(data,"utf-8")
                print(data)



counter = 0

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
addr = (local_ip,4444)


while True:
    use = input ("What to you want to send->")
    if use:
        addr=('192.168.0.100',addr[1])

        s=socket.socket()
        s.connect(addr)

        data = bytes(f"{use}","utf-8")

        s.sendall(data)
        s.close()
        
        antwort()
        
        
