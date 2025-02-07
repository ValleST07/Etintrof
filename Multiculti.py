import socket
import json
import multiprocessing
import time

# Use IP address of Socket server and non-privileged port >1023
addr = ('192.168.0.100', 4444)

def send_data(s, x):
    data = bytes(f"{x}", "utf-8")
    s.sendall(data)
    print(f"Sent: {x}")

def receive_data(s):
    data = s.recv(1024)
    print(f"Received: {str(data, 'utf-8')}")

def client():
    s = socket.socket()
    s.connect(addr)

    x = "Hallo"
    
    # Create two processes: one for sending data and one for receiving data
    send_process = multiprocessing.Process(target=send_data, args=(s, x))
    receive_process = multiprocessing.Process(target=receive_data, args=(s,))
    
    # Start both processes
    send_process.start()
    receive_process.start()

    # Wait for both processes to finish
    send_process.join()
    receive_process.join()

    s.close()

if __name__ == '__main__':
    client()
