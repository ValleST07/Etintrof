import json
import socket



def handle_player(conn, addr, player_num, player_position):
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
                    process_movement(parsed_data[0], parsed_data[1], parsed_data[2], player_num, addr, player_position, conn)
                else:
                    print(f"Keine Eingabe von {addr}: {data}")
                    continue  # Ungültige Eingabe, warte auf die nächste Nachricht

            except Exception as e:
                print(f"Fehler bei der Verarbeitung der Daten von {addr}: {e}")
                continue

    except ConnectionResetError:
        print(f"Verbindung mit {addr} wurde unerwartet geschlossen.")
    except Exception as e:
        print(f"Fehler bei der Kommunikation mit {addr}: {e}")


def parse_input(data):
    """Parst die Eingabe des Clients und gibt sie als Dictionary zurück."""
    try:
        splited = data.split(";")
        # Beispiel: "dir:9; angle:0; mouse:False"
        direction = splited[0]
        angle = splited[1]
        mouse = splited[2]
        mouse = mouse[0]

        print(direction,angle,mouse)
        return (direction,angle,mouse)

    except Exception as e:
        print(f"Fehler beim Parsen der Eingabe: {e}")
        return None
    

def process_movement(direction, angle, mouse, player_num, addr, player_position, conn):
    """Verarbeitet die Eingabe des Spielers (Richtung, Winkel, Maus)."""
    try:
        if direction != "8":
            print(f"--Spieler {player_num} möchte in die Richtung {direction}.")
            player_position = Bewegen(player_num, player_position, conn, direction)

        print(f"--Spieler {player_num} hat einen Winkel von {angle} angegeben.")
        Aim_Angle(player_num, conn, angle)

        if mouse != "0":
            print(f"--Spieler {player_num} hat Maus aktiviert: {mouse}")
            Shot(player_num, conn, player_position)
            
       

    except Exception as e:
        print(f"--Fehler bei der Verarbeitung der Bewegung von Spieler {player_num}: {e}")


def Bewegen(player_num, player_position, conn, direction):
    """Bewege den Spieler basierend auf der Richtung"""
    current_position = player_position[player_num]
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

    player_position[player_num] = current_position
    return player_position

def Aim_Angle(player_num, conn, angle):
    """Ziele mit dem Spieler basierend auf den Winkel"""
    # This function can be implemented later
    # For now, just acknowledge the angle
    return None

def Shot(player_num, conn, positions):
    """Prüfen ob ein spieler getroffen und die monition anzeigen"""
    # This function can be implemented later
    # For now, just acknowledge the shot
    return None

def senden(player_position, addr):
    """Sendet die aktuellen Spielerpositionen an den Client"""
    try:
        # Konvertiere die Positionen in JSON
        print(addr)
        s=socket.socket()
        s.connect((addr[0],4444))
            
        data= bytes(f"{player_position}","utf-8")
        # Senden
        s.sendall(data)
        print(f"Gesendete Daten: {data}")
        
    except Exception as e:
        print(f"Fehler beim Senden der Daten: {e}")

def start_server(local_ip, player_number, local_addr):
    player_addr = []
    player_position = [[10, 10], [10, 2390], [2390, 10], [2390, 2390]]

    # Server starten
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(local_addr)
        s.listen()
        print(f"Server startet auf {local_ip}: {local_addr[1]} ...")
        print(f"Warte auf {player_number} Spieler...")

        try:
            while len(player_addr)<player_number:
                conn, addr = s.accept()
                player_addr.append(addr)
                print(f"{len(player_addr)}/{player_number} verbunden")
            print(f"\\n\rAlle {player_number} Spieler verbunden!")
            
            while True:
                for player_num in range(len(player_addr)): 
                    handle_player(conn, player_addr[player_num], player_num, player_position)
                    print(player_num)
                for addr in player_addr:
                    senden(player_position, addr)

                
        except KeyboardInterrupt:
            print("\\nServer wird beendet...")
        except Exception as e:
            print(f"Fehler im Server: {e}")

if __name__ == "__main__":
    # Server Setup
    try:
        local_ip = input("Server IP (default: 172.20.10.14): ") or "172.20.10.14"
        player_number = int(input("Anzahl der Spieler -> ") or "2")
        port = int(input("Port (default: 4444): ") or "4444")
        
        local_addr = (local_ip, port)
        
        start_server(local_ip, player_number, local_addr)
    except KeyboardInterrupt:
        print("\\nServer-Start abgebrochen.")
    except ValueError:
        print("Bitte geben Sie eine gültige Zahl für die Spieleranzahl und den Port ein.")
    except Exception as e:
        print(f"Fehler beim Starten des Servers: {e}")