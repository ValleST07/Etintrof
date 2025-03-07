import socket

def antwort(local_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(local_addr)
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = str(data,"utf-8")
                print(data)
                



counter = 0

hostname = socket.gethostname()
local_ip = '192.168.0.100'
local_addr = (local_ip,4444)
print(local_addr)

while True:
    use = input ("What to you want to send->")
    if use:
        addr=('192.168.0.101',local_addr[1])

        s=socket.socket()
        s.connect(addr)

        data = bytes(f"{use},\n {local_addr}","utf-8")
        s.sendall(data)
        s.close()
        
        antwort(local_addr)
        
        
