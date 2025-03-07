import socket

hostname = socket.gethostname()
local_ip = '172.20.10.4'
server_addr = '172.20.10.14'
local_addr = (local_ip, 4444)
print(local_addr)

def receive(local_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(local_addr)
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if data:
                print(str(data, "utf-8"))
               
def transmit(local_addr, server_addr):
    use = input("What do you want to send: ")
    if use:
        addr = (server_addr, local_addr[1])
        s = socket.socket()
        s.connect(addr)
        data = bytes(f"{use},\n {local_addr}", "utf-8")
        s.sendall(data)
        s.close()

while True:
    transmit(local_addr, server_addr)
    

        
        

