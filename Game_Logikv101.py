import json
import socket
import threading

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
                    print(f"Direction: {parsed_data['dir']}")
                    print(f"Angle: {parsed_data['angle']}")
                    print(f"Mouse: {parsed_data['mouse']}")
                    
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

def parse_input(data):
    """Parst die Eingabe des Clients und gibt sie als Dictionary zurück."""
    try:
        # Beispiel: dir:9; angle:0; mouse:False
        parts = data.split("; ")
        print(f"Parts: {parts}")
        parsed_data = {}
        for part in parts:
            print(f"Part: {part}")
            key, value = part.split(":")
            parsed_data[key.strip()] = value.strip()

        print(parsed_data)
        return parsed_data

    except Exception as e:
        print(f"Fehler beim Parsen der Eingabe: {e}")
        return None

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

def senden(conn, start_position):
    """Sendet die aktuellen Spielerpositionen an den Client"""
    try:
        # Konvertiere die Positionen in JSON
        position_data = json.dumps(start_position)
        
        # Senden
        conn.sendall(position_data.encode('utf-8'))
        print(f"Gesendete Daten: {position_data}")
    except Exception as e:
        print(f"Fehler beim Senden der Daten: {e}")

def start_server(local_ip, player_number, local_addr):
    player_addr = []
    start_position = [[10, 10], [10, 2390], [2390, 10], [2390, 2390]]

    # Server starten
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(local_addr)
        s.listen()
        print(f"Server startet auf {local_ip}:{local_addr[1]}...")
        print(f"Warte auf {player_number} Spieler...")

        try:
            while len(player_addr) < player_number:
                conn, addr = s.accept()
                player_addr.append(addr)
                player_num = len(player_addr) - 1  
                threading.Thread(target=handle_player, args=(conn, addr, player_num, start_position)).start()
                print(f"Spieler {player_num + 1} verbunden! ({len(player_addr)}/{player_number})")

            print(f"\\n\rAlle {player_number} Spieler verbunden!")

            # Keep the server running
            while True:
                pass  # Endlos warten
                
        except KeyboardInterrupt:
            print("\\nServer wird beendet...")
        except Exception as e:
            print(f"Fehler im Server: {e}")

if __name__ == "__main__":
    # Server Setup
    try:
        local_ip = input("Server IP (default: 0.0.0.0): ") or "0.0.0.0"
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