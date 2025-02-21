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
            x="10909.90809809.1980, Fertig"

            #data = json.dumps(x).encode() 
            data= bytes(f"{use}","utf-8")
            s.sendall(data)
            #data = s.recv(1024)

            #print("Received "+str(data,"utf-8"))
            s.close()
            break
        
        

HOST = "192.168.0.100"  # Standard loopback interface address (localhost)
PORT = 4444  # Port to listen on (non-privileged ports are > 1023)



while True:
    U=2#V
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
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
                senden(addr)
          

              

