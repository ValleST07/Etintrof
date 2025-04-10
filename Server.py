import socket
import random
import psutil
import time
import BulletObject
import math

def get_wlan_ip():
    for interface, addrs in psutil.net_if_addrs().items():
        if "wlan" in interface or "WLAN" in interface or "WI-FI" in interface:#WLAN
        #if "10"in interface:#HOTSPOT
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4 address
                    print(f"{interface}: {addr.address}")
                    return addr.address
    print("WLAN interface not found")

def generate_map(width=50, height=50):
    # Create empty map filled with floors (0)
    game_map = [[0 for _ in range(width)] for _ in range(height)]
    
    # Add border walls
    for x in range(width):
        game_map[0][x] = 1  # Top border
        game_map[height-1][x] = 1  # Bottom border
    for y in range(height):
        game_map[y][0] = 1  # Left border
        game_map[y][width-1] = 1  # Right border
    
    # Add random walls
    for _ in range(random.randint(50, 100)):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        game_map[y][x] = 1
        
        # Sometimes make wall clusters
        if random.random() > 0.7:
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < width-1 and 0 < ny < height-1:
                    game_map[ny][nx] = 1
    
    # Add water features
    for _ in range(random.randint(5, 10)):
        # Start a water feature
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        size = random.randint(3, 8)
        
        for _ in range(size):
            game_map[y][x] = 2
            # Random walk to expand water
            dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
            x = max(1, min(width-2, x + dx))
            y = max(1, min(height-2, y + dy))
    
    return game_map
Map=generate_map()

player_position = []
player_angle=[]
player_health=[]
player_readyToShoot=[]
OBullets=[]

def parse_input(data):
    """Parst die Eingabe des Clients und gibt sie als Dictionary zurück."""

    splited = data.split(";")
    # Beispiel: "player:1; dir:9; angle:0; mouse:False"
    player_num = int(splited[0])
    
    direction = splited[1]
    angle = splited[2]
    mouse = splited[3]
    mouse = mouse[0]

    #print(player_num,direction,angle,mouse)
    return (player_num,direction,angle,mouse)

def senden(addr, daten=None):
    global player_position
    global player_angle

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    if daten:
        sock.sendto(bytes(daten,"utf-8"),(addr,4444))
        return
    bullet_position=[]
    for i in OBullets:
        bullet_position.append(i.get_position())
    data= bytes(f"{player_position}*{player_angle}*{bullet_position}*{player_health}","utf-8")
    sock.sendto(data,(addr,4444))
    #print(f"Gesendete Daten: {data}")

def Check_Collision(pos, isPlayer=True):#True=keine Collision
    #block size 48
    #player size 19
    if pos[0]>2399 or pos[0]<0 or pos[1]>2399 or pos[1]<0:
        return False 
    try:
        if isPlayer==1: #Collision für Spieler
            if Map[int(pos[1]/48)] [int(pos[0]/48)] == 0:
                return True
            else:
                return False
        else: #Collision für Bullet
            if Map[int(pos[1]/48)] [int(pos[0]/48)] == 0 or Map[int(pos[1]/48)] [int(pos[0]/48)] == 2:
                #check for player
                for player_num,playerPos in enumerate(player_position):
                    if (pos[0]>playerPos[0]-19 and pos[0]<playerPos[0]+19 and pos[1]>playerPos[1]-19 and pos[1]<playerPos[1]+19): #Check for player collision
                        player_health[player_num]-=10
                        if player_health[player_num]==0: #STERBEN
                            player_position[player_num]=[100000000,100000000]
                        return False
                return True
            else:
                return False
    except:
        return False

def Bewegen(player_num, direction):
    #playersize 19
    global player_position
    current_position = player_position[player_num]
    movment_speed = 3

    if direction == "0" and Check_Collision((current_position[0],current_position[1] - movment_speed -19)):                                         # Bewegung nach oben  
        current_position[1] -= movment_speed  

    elif direction == "7" and Check_Collision(( current_position[0] - movment_speed-20  ,current_position[1] - movment_speed-20)):           # Bewegung diagonal nach oben-links  
        current_position[0] -= movment_speed-1  
        current_position[1] -= movment_speed-1  

    elif direction == "6" and Check_Collision(( current_position[0] - movment_speed -19 ,current_position[1])):                                       # Bewegung nach links  
        current_position[0] -= movment_speed  

    elif direction == "5" and Check_Collision(( current_position[0] - movment_speed-20  ,current_position[1] + movment_speed+18)):         # Bewegung diagonal nach unten-links  
        current_position[0] -= movment_speed-1  
        current_position[1] += movment_speed-1  

    elif direction == "4" and Check_Collision(( current_position[0] ,current_position[1] + movment_speed+18)):                                 # Bewegung nach unten  
        current_position[1] += movment_speed  

    elif direction == "3" and Check_Collision(( current_position[0] + movment_speed+18  ,current_position[1] + movment_speed+18)):  # Bewegung diagonal nach unten-rechts  
        current_position[0] += movment_speed-1  
        current_position[1] += movment_speed-1  

    elif direction == "2" and Check_Collision(( current_position[0] + movment_speed +19 ,current_position[1] )):                                     # Bewegung nach rechts  
        current_position[0] += movment_speed  

    elif direction == "1" and Check_Collision(( current_position[0] + movment_speed+18  ,current_position[1] - movment_speed-20)):      # Bewegung diagonal nach oben-rechts  
        current_position[0] += movment_speed-1  
        current_position[1] -= movment_speed-1  

    player_position[player_num] = current_position

def Shoot(player_num):
    global OBullets
    global player_angle
    global player_position
    x=player_position[player_num][0]+ math.cos(player_angle[player_num]) * 25
    y=player_position[player_num][1]+ math.sin(player_angle[player_num]) * 25
    OBullets.append(BulletObject.Bullet([x,y], player_angle[player_num]))

def process_movement(player_num, direction, angle, mouse):
    global player_readyToShoot
    global OBullets
    player_angle[player_num]=float(angle)
    if direction != "8":
        Bewegen(player_num, direction)

    if mouse != "0" and player_readyToShoot[player_num]:
        player_readyToShoot[player_num]=False
        Shoot(player_num)
    elif (mouse =="0"):
        player_readyToShoot[player_num]=True

    #move Bullets
    for i in OBullets:
        i.move()
    OBullets = [i for i in OBullets if Check_Collision(i.get_position(), False)] # Lösch Bullet wenn Kollison

def handle_player(s):
    global player_position

    while True:
        data, addr = s.recvfrom(1024)
        if not data:
            break
    
        data = data.decode('utf-8').strip()
        parsed_data = parse_input(data)
        if parsed_data:                    
            process_movement(parsed_data[0], parsed_data[1], parsed_data[2], parsed_data[3])
            return
        else:
            print(f"Keine Eingabe von {addr}: {data}")
            continue  # Ungültige Eingabe, warte auf die nächste Nachricht

def run_server(local_ip, player_number, local_addr):
    global player_position
    global player_angle
    global player_health
    global player_readyToShoot
    player_addr = []
    
    # Server starten
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(local_addr)
        print(f"Server startet auf {local_ip}: {local_addr[1]} ...")
        print(f"Warte auf {player_number} Spieler...")
        match(player_number):
            case 1:
                player_position=[[100,100]]
                player_angle=[0]
                player_health=[100]
                player_readyToShoot=[True]
            case 2:
                player_position=[[100,100],[100,2300]]
                player_angle=[0,0]
                player_health=[100,100]
                player_readyToShoot=[True,True]
            case 3:
                player_position=[[100,100],[100,2300],[2300,100]]
                player_angle=[0,0,0]
                player_health=[100,100,100]
                player_readyToShoot=[True,True,True]
            case 4:
                player_position=[[100,100],[100,2300],[2300,100],[2300,2300]]
                player_angle=[0,0,0,0]
                player_health=[100,100,100,100]
                player_readyToShoot=[True,True,True,True]
    
        while len(player_addr)<player_number:
            data, addr = s.recvfrom(1024)
            if addr[0] not in player_addr:
                player_addr.append(addr[0])
                print(f"{len(player_addr)}/{player_number} verbunden")
                senden(addr[0], f"M{Map}")
                time.sleep(0.1)
                senden(addr[0], f"P{len(player_addr)-1}")
            
        print(f"\\n\rAlle {player_number} Spieler verbunden!")

        while True:
            handle_player(s)
            for addresse in player_addr:
                senden(addresse)

if __name__ == "__main__":
    # Server Setup
    local_ip = get_wlan_ip()
    player_number = int(input("Anzahl der Spieler -> ") or "2")
    #port = int(input("Port (default: 4444): ") or "4444")
    port=4444
    local_addr = (local_ip, port)
    
    run_server(local_ip, player_number, local_addr)
