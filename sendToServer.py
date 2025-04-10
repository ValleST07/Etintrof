import socket
import psutil

def get_wlan_ip():
    for interface, addrs in psutil.net_if_addrs().items():
        if "wlan" in interface or "WLAN" in interface or "WI-FI" in interface:  # Adjust for your OS naming
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4 address
                    print(f"{interface}: {addr.address}")
                    return addr.address
    print("WLAN interface not found")

def receive(length:int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(local_addr)

        while True:
            data, addr = sock.recvfrom(length)
            if not data:
                break
            data=data.decode('utf-8').strip()
            #print(f"Rohdaten vom Server:{data}")
            return data


def transmit(server_addr, data):#localAddr=(local_ip,port) port=4444
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP
        data = bytes(f"{data},\n {local_addr}", "utf-8")
        sock.sendto(data,server_addr)
        sock.close()
    except:
        print("!!!!!!!!!!!!!!_KEINE VERBINDUNG ZUM SERVER_!!!!!!!!!!!!!!")

local_addr=(get_wlan_ip(), 4444)
print(local_addr)