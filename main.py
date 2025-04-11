import runpy
import pygame
from pygame import Rect

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)

# Fenster-Setup
WIDTH, HEIGHT = 400, 300

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Selector")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Buttons
server_button = Rect(100, 100, 200, 50)
ui_button = Rect(100, 180, 200, 50)

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
    ui_text = font.render("Client", True, WHITE)

    screen.blit(server_text, server_text.get_rect(center=server_button.center))
    screen.blit(ui_text, ui_text.get_rect(center=ui_button.center))

    pygame.display.flip()


running = True
while running:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if server_button.collidepoint(mouse_pos):
                runpy.run_path("Server.py")
                running = False
            elif ui_button.collidepoint(mouse_pos):
                runpy.run_path("MapUITest.py")
                running = False
    clock.tick(60)