import subprocess
import sys
import os
import pygame
from pygame import Rect
import signal

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)

# Fenster-Setup
WIDTH, HEIGHT = 400, 300

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Branch Selector")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Buttons
server_button = Rect(100, 100, 200, 50)
ui_button = Rect(100, 180, 200, 50)

def cleanup():
    """Zurück zu main und Pygame schließen"""
    try:
        subprocess.run(["git", "checkout", "main"], stderr=subprocess.DEVNULL)
    except:
        pass
    pygame.quit()
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()

# Strg+C Signalhandler
signal.signal(signal.SIGINT, signal_handler)


def run_script(branch, script_name):
    project_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], check=True, cwd=project_dir)
        subprocess.run(["git", "checkout", branch], check=True, cwd=project_dir)
        print(f"[Info] Switched to branch '{branch}'")

        pygame.display.quit()

        process = subprocess.Popen([sys.executable, script_name], cwd=project_dir)

        process.wait()
        return True

    except subprocess.CalledProcessError as e:
        return False

    finally:
        subprocess.run(["git", "checkout", "main"], check=True, cwd=project_dir)


def draw_menu():
    screen.fill(WHITE)

    # Titel
    title = font.render("Wähle einen Modus", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    # Buttons
    pygame.draw.rect(screen, BLUE, server_button)
    pygame.draw.rect(screen, BLUE, ui_button)

    # Texte
    server_text = font.render("Server", True, WHITE)
    ui_text = font.render("UI", True, WHITE)

    screen.blit(server_text, server_text.get_rect(center=server_button.center))
    screen.blit(ui_text, ui_text.get_rect(center=ui_button.center))

    pygame.display.flip()

try:
    running = True
    while running:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if server_button.collidepoint(mouse_pos):
                    if run_script("server", "server.py"):
                        running = False

                elif ui_button.collidepoint(mouse_pos):
                    if run_script("UI", "MapUITest.py"):
                        running = False

        clock.tick(60)
finally:
    cleanup()

