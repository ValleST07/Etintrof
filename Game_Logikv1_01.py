import socket
import random

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
map_data = generate_map()

player_position = [[100, 100], [100, 2300], [2300, 100], [2300, 2300]]
player_angle=[0,0,0,0]

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



def process_movement(player_num, direction, angle, mouse):
    """Verarbeitet die Eingabe des Spielers (Richtung, Winkel, Maus)."""
    global player_angle
    player_angle[player_num]=float(angle)
    if direction != "8":
        Bewegen(player_num, direction)

    if mouse != "0":
        Shot(player_num, player_position)

def Check_Collision(pos):
    #block size 48
    if pos[0]>2399 or pos[0]<0 or pos[1]>2399 or pos[1]<0:
        return False 
    try:
        if Map[int(pos[1]/48)] [int(pos[0]/48)] == 0:
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


def Shot(player_num, positions):
    """Prüfen ob ein spieler getroffen und die monition anzeigen"""
    
    return None

def senden(addr, daten=None):
    global player_position
    global player_angle

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    if daten:
        sock.sendto(bytes(daten,"utf-8"),(addr,4444))
        return
    data= bytes(f"{player_position}*{player_angle}","utf-8")
    sock.sendto(data,(addr,4444))
    #print(f"Gesendete Daten: {data}")


def start_server(local_ip, player_number, local_addr):
    player_addr = []
    
    # Server starten
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(local_addr)
        print(f"Server startet auf {local_ip}: {local_addr[1]} ...")
        print(f"Warte auf {player_number} Spieler...")

    
        while len(player_addr)<player_number:
            data, addr = s.recvfrom(1024)
            if addr[0] not in player_addr:
                player_addr.append(addr[0])
                print(f"{len(player_addr)}/{player_number} verbunden")
                senden(addr[0], f"F{len(player_addr)-1}")
                senden(addr[0], f"M{map_data}")
            
        print(f"\\n\rAlle {player_number} Spieler verbunden!")

        while True:
            handle_player(s)
            for addresse in player_addr:
                senden(addresse)




if __name__ == "__main__":
    # Server Setup

    local_ip = input("Server IP (default: 172.20.10.14): ") or "192.168.0.102"
    player_number = int(input("Anzahl der Spieler -> ") or "2")
    port = int(input("Port (default: 4444): ") or "4444")
    
    local_addr = (local_ip, port)
    
    start_server(local_ip, player_number, local_addr)
