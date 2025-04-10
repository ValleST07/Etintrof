import subprocess
import sys
import pygame
from pygame import Rect
import signal

# PyGame initialisieren
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Branch Selector")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)

# Buttons
server_button = Rect(100, 100, 200, 50)
ui_button = Rect(100, 180, 200, 50)

def cleanup():
    """Sicher zurück zum main-Branch wechseln und PyGame beenden"""
    try:
        subprocess.run(["git", "checkout", "main"], stderr=subprocess.DEVNULL)
    except:
        pass
    pygame.quit()
    sys.exit(0)

def signal_handler(sig, frame):
    """Handler für Strg+C"""
    cleanup()

# Signal-Handler registrieren
signal.signal(signal.SIGINT, signal_handler)

def run_script(branch, script_name):
    try:
        # Prüfen ob wir in einem Git-Repo sind
        try:
            subprocess.run(["git", "rev-parse", "--git-dir"], 
                         check=True, 
                         capture_output=True)
        except subprocess.CalledProcessError:
            print("Achtung: Kein Git-Repository erkannt!")
            return False
            
        # PyGame sauber beenden
        pygame.display.quit()
        
        # Branch wechseln und Skript starten
        subprocess.run(["git", "checkout", branch], check=True)
        subprocess.run([sys.executable, script_name], check=True)
        return True
        
    except Exception as e:
        print(f"Fehler: {str(e)}")
        return False
    finally:
        cleanup()

def draw_menu():
    screen.fill(WHITE)
    
    # Titel
    title = font.render("Wähle einen Modus", True, BLACK)
    screen.blit(title, (100, 50))
    
    # Buttons zeichnen
    pygame.draw.rect(screen, BLUE, server_button)
    pygame.draw.rect(screen, BLUE, ui_button)
    
    # Button Text
    server_text = font.render("Server", True, WHITE)
    ui_text = font.render("UI", True, WHITE)
    
    screen.blit(server_text, (server_button.x + 70, server_button.y + 10))
    screen.blit(ui_text, (ui_button.x + 85, ui_button.y + 10))
    
    pygame.display.flip()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if server_button.collidepoint(mouse_pos):
                    if run_script("server", "server.py"):
                        running = False
                    else:
                        # Bei Fehler neu initialisieren
                        pygame.init()
                        screen = pygame.display.set_mode((400, 300))
                        
                elif ui_button.collidepoint(mouse_pos):
                    if run_script("UI", "MapUITest.py"):
                        running = False
                    else:
                        pygame.init()
                        screen = pygame.display.set_mode((400, 300))
        
        try:
            draw_menu()
        except pygame.error:
            # Falls Display verloren, neu initialisieren
            pygame.init()
            screen = pygame.display.set_mode((400, 300))
            continue
            
        clock.tick(60)
    
    cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        print(f"Unerwarteter Fehler: {str(e)}")
        cleanup()