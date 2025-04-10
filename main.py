import pygame
import subprocess
import sys
from pygame import Rect

# PyGame Initialisierung
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Programmauswahl")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)

# Buttons
server_button = Rect(100, 100, 200, 50)
ui_button = Rect(100, 180, 200, 50)

def run_script(script_name):
    """Startet ein Python-Skript im gleichen Verzeichnis"""
    try:
        pygame.quit()  # PyGame beenden vor Skriptstart
        subprocess.run([sys.executable, script_name], check=True)
        return True
    except Exception as e:
        print(f"Fehler beim Starten von {script_name}: {e}")
        return False
    finally:
        # PyGame neu starten falls wir zurückkommen
        pygame.init()
        global screen
        screen = pygame.display.set_mode((400, 300))

def draw_menu():
    screen.fill(WHITE)
    
    # Titel
    title = font.render("Wähle einen Modus", True, BLACK)
    screen.blit(title, (100, 50))
    
    # Server-Button
    pygame.draw.rect(screen, BLUE, server_button)
    server_text = font.render("Server", True, WHITE)
    screen.blit(server_text, (server_button.x + 70, server_button.y + 10))
    
    # UI-Button
    pygame.draw.rect(screen, BLUE, ui_button)
    ui_text = font.render("UI", True, WHITE)
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
                    if run_script("server.py"):
                        running = False
                
                elif ui_button.collidepoint(mouse_pos):
                    if run_script("MapUITest.py"):
                        running = False
        
        draw_menu()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()