import json
import socket
import threading


## ------------------------------------------------------------------------
def handle_player(conn, addr, player_num, start_position):
    print(f"Verbunden mit {addr} als Spieler {player_num + 1}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                data = data.decode('utf-8').strip()
                print(f"Rohdaten von {addr}: {data}")
                
                parsed_data = parse_input(data)
                if parsed_data:
                    print(parsed_data['dir'])
                    print(parsed_data['angle'])
                    print(parsed_data['mouse'])
                    
                    process_movement(parsed_data['dir'], parsed_data['angle'], parsed_data['mouse'], player_num, start_position, conn)
                else:
                    print(f"Ungültige Eingabe von {addr}: {data} -> Ignoriert")
                    continue  # Ungültige Eingabe, warte auf die nächste Nachricht

            except Exception as e:
                print(f"Fehler bei der Verarbeitung der Daten von {addr}: {e}")
                continue

    except ConnectionResetError:
        print(f"Verbindung mit {addr} wurde unerwartet geschlossen.")
    except Exception as e:
        print(f"Fehler bei der Kommunikation mit {addr}: {e}")
    finally:
        print(f"Verbindung mit {addr} geschlossen")
        conn.close()


## ------------------------------------------------------------------------
def parse_input(data):
    """Parst die Eingabe des Clients und gibt sie als Dictionary zurück."""
    try:
        # Beispiel: dir:9, angle:0, mouse:False
        parts = data.split("; ")
        pritn(f"Parts -----------------{parts}")
        parsed_data = {}
        for part in parts:
            print(f"Part -----------------{part}")
            key, value = part.split(":")
            parsed_data[key.strip()] = value.strip()
        
        print(parsed_data)
        return parsed_data
    
    except Exception as e:
        print(f"Fehler beim Parsen der Eingabe: {e}")
        return None


## ------------------------------------------------------------------------
def process_movement(direction, angle, mouse, player_num, start_position, conn):
    """Verarbeitet die Eingabe des Spielers (Richtung, Winkel, Maus)."""
    try:
        if direction != "9":
            print(f"--Spieler {player_num} möchte in die Richtung {direction}.")
            start_position = Bewegen(player_num, start_position, conn, direction)
        
        if angle != "None":
            print(f"--Spieler {player_num} hat einen Winkel von {angle} angegeben.")
            Aim_Angle(player_num, conn, angle)

        
        if mouse != "False":
            print(f"--Spieler {player_num} hat Maus aktiviert: {mouse}")
            Shot(player_num, conn, start_position)
            
        senden(conn, start_position)

    except Exception as e:
        print(f"--Fehler bei der Verarbeitung der Bewegung von Spieler {player_num}: {e}")


## ------------------------------------------------------------------------
def Bewegen(player_num, start_position, conn, direction):
    """Bewege den Spieler basierend auf der Richtung"""
    current_position = start_position[player_num]
    movment_speed = 5

    if direction == "0" and current_position[1] > 0:                                         # Bewegung nach oben  
        current_position[1] -= movment_speed  

    elif direction == "7" and current_position[0] > 0 and current_position[1] > 0:           # Bewegung diagonal nach oben-links  
        current_position[0] -= movment_speed  
        current_position[1] -= movment_speed  

    elif direction == "6" and current_position[0] > 0:                                       # Bewegung nach links  
        current_position[0] -= movment_speed  

    elif direction == "5" and current_position[0] > 0 and current_position[1] < 2399:        # Bewegung diagonal nach unten-links  
        current_position[0] -= movment_speed  
        current_position[1] += movment_speed  

    elif direction == "4" and current_position[1] < 2399:                                    # Bewegung nach unten  
        current_position[1] += movment_speed  

    elif direction == "3" and current_position[0] < 2399 and current_position[1] < 2399:     # Bewegung diagonal nach unten-rechts  
        current_position[0] += movment_speed  
        current_position[1] += movment_speed  

    elif direction == "2" and current_position[0] < 2399:                                    # Bewegung nach rechts  
        current_position[0] += movment_speed  

    elif direction == "1" and current_position[0] < 2399 and current_position[1] > 0:        # Bewegung diagonal nach oben-rechts  
        current_position[0] += movment_speed  
        current_position[1] -= movment_speed  


    start_position[player_num] = current_position
    return start_position


## ------------------------------------------------------------------------
def Aim_Angle(player_num, conn, angle):
    """Ziele mit dem Spieler basierend auf den Winkel"""

    return None


## ------------------------------------------------------------------------
def Shot(player_num, conn, positions):
    """Prüfen ob ein spieler getroffen und die monition anzeigen"""

    return None


## ------------------------------------------------------------------------
def senden(conn, start_position):
    data = []
    #Spieler Positionen
    position_data = json.dumps(start_position)
    #Angle
    
    #Shot
    
    #Senden
    data.append(position_data)
    conn.sendall(data.encode('utf-8'))
    print(f"Neue Daten = = = {data}")


## ------------------------------------------------------------------------
def start_server(local_ip, player_number, local_addr):
    player_addr = []  
    start_position = [[10, 10], [10, 2390], [2390, 10], [2390, 2390]]  

    # Server starten
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(local_addr)
        s.listen()
        print("Server startet...")

        while len(player_addr) < player_number:
            conn, addr = s.accept()
            player_addr.append(addr)
            player_num = len(player_addr) - 1  
            threading.Thread(target=handle_player, args=(conn, addr, player_num, start_position)).start()

        print(f"\n\rAlle {player_number} Spieler verbunden!")

        while True:
            pass  # Endlos warten


# Server Setup-----------------------------------------------------------
local_ip = "192.168.188.129"  
player_number = int(input("Anzahl der Spieler -> "))  
local_addr = (local_ip, 4444)

start_server(local_ip, player_number, local_addr)

