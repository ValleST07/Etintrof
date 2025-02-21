import socket
import json

def antwort():
    U=2#V
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.0.101',4444))
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




while True:
    use = input ("What to you want to send->")
    if use:
        #Use IP address of Socket server and non-privileged port >1023
        addr=('192.168.0.100',4444)

        s=socket.socket()
        s.connect(addr)

        #data = json.dumps(x).encode() 
        data= bytes(f"{use}","utf-8")
        s.sendall(data)
        #data = s.recv(1024)

        #print("Received "+str(data,"utf-8"))
        s.close()
        antwort()
        
        
