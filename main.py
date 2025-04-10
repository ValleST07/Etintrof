import subprocess
import sys
import pygame
from pygame import Rect


pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Game Selector")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)

# Buttons
server_button = Rect(100, 100, 200, 50)
ui_button = Rect(100, 180, 200, 50)

def run_script(branch, script_name):

    # Schließe PyGame, bevor wir den Branch wechseln
    pygame.quit()
    subprocess.run(["git", "rev-parse", "--git-dir"], check=True, capture_output=True)
    subprocess.run(["git", "checkout", branch], check=True)
    subprocess.run([sys.executable, script_name], check=True)


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
    ui_text = font.render("Client", True, WHITE)
    screen.blit(ui_text, (ui_button.x + 70, ui_button.y + 10))
    
    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if server_button.collidepoint(mouse_pos):
                run_script("server", "server.py")
                running = False
            
            elif ui_button.collidepoint(mouse_pos):
                run_script("UI", "MapUITest.py")
                running = False
    
    draw_menu()
    clock.tick(60)
