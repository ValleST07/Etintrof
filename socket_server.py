# echo-server.py
import json
import socket

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
                #data = json.loads(data)
                print(data)
             #   elif data=="bereit":
              #      conn.sendall(bin(U))
