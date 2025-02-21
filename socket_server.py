# echo-server.py
import json
import socket

def senden(addr):
    while True:
        use = input ("What to you want to send->")
        if use:
            #Use IP address of Socket server and non-privileged port >1023

            s=socket.socket()
            s.connect((addr[0],4444))

            #data = json.dumps(x).encode() 
            data= bytes(f"{use}","utf-8")
            s.sendall(data)
            s.close()
            break
        
        

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
local_addr = (local_ip,4444)
player_addr = [0]

#empfangen
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(local_addr)
        s.listen()
        conn, addr = s.accept()
        if addr not in player_addr:
            player_addr[0]+=1
            player_addr.append(addr,player_addr[0])

        with conn:
            print(f"Connected by {addr}")
            while True:
                data=conn.recv(1024)
                if not data:
                    break
                data=str(data,"utf-8")
                print(data)
                senden(addr)
          

              

