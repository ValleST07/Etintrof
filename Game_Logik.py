import json
import socket

def senden(addr,player_addr):
    print(addr)
    while True:
        use = input ("What to you want to send->")
        if use:

            s=socket.socket()
            s.connect((addr[0],4444))
            
            data= bytes(f"{use}","utf-8")
            _1 = f"Player {player_addr[0]}"
            s.sendall(data)
            s.sendall(_1)
            s.close()
            break
        
        

hostname = socket.gethostname()
local_ip = input("Put here your IP ->")


local_addr = (local_ip,4444)
player_addr = [0]

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(local_addr)
        s.listen()
        conn, addr = s.accept()
        if addr not in player_addr:
            player_addr[0]+=1
            player_addr.append(player_addr[0])
            player_addr.append(addr)
        with conn:
            print(f"Connected by {addr}")
            while True:
                data=conn.recv(1024)
                if not data:
                    break
                data=str(data,"utf-8")
                print(data)
                senden(addr,player_addr)
          

              


