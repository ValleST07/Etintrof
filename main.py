import pygame
import subprocess
import sys

# Farben
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Fenstergröße
WIDTH, HEIGHT = 400, 300

# Buttons definieren
class Button:
    def __init__(self, text, rect, callback):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.callback = callback
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# Aktionen
def starte_server():
    pygame.quit()
    subprocess.run(["python", "server.py"])
    sys.exit()

def starte_client():
    pygame.quit()
    subprocess.run(["python", "MapUITest.py"])
    sys.exit()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Auswahlmenü")

font = pygame.font.SysFont(None, 40)
title_text = font.render("Was möchtest du starten?", True, BLACK)
title_rect = title_text.get_rect(center=(WIDTH // 2, 50))

# Buttons
buttons = [
    Button("Server starten", (100, 100, 200, 50), starte_server),
    Button("Client starten", (100, 170, 200, 50), starte_client)
]

# Hauptloop
running = True
while running:
    screen.fill(WHITE)
    screen.blit(title_text, title_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

pygame.quit()

