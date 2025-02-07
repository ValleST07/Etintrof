import pygame

# Initialisierung
pygame.init()
WIDTH, HEIGHT = 800, 600  # Fenstergröße
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Map und Kamera
TILE_SIZE = 100  # Größe der Schachbrett-Kacheln
MAP_WIDTH, MAP_HEIGHT = 2000, 1500  # Große Map
map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))  # Ganze Map als Surface
player = pygame.Rect(500, 500, 50, 50)  # Spieler-Position

# Schachbrettmuster zeichnen
for y in range(0, MAP_HEIGHT, TILE_SIZE):
    for x in range(0, MAP_WIDTH, TILE_SIZE):
        color = (180, 180, 180) if (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0 else (100, 100, 100)
        pygame.draw.rect(map_surface, color, (x, y, TILE_SIZE, TILE_SIZE))

running = True
while running:
    screen.fill((0, 0, 0))  # Hintergrund

    # Spieler steuern
    keys = pygame.key.get_pressed()
    speed = 5
    if keys[pygame.K_LEFT]: player.x -= speed
    if keys[pygame.K_RIGHT]: player.x += speed
    if keys[pygame.K_UP]: player.y -= speed
    if keys[pygame.K_DOWN]: player.y += speed

    # Spieler auf die Map zeichnen
    pygame.draw.rect(map_surface, (255, 0, 0), player)

    # Kamera (Viewport) berechnen: Spieler zentrieren
    cam_x = max(0, min(player.x - WIDTH // 2, MAP_WIDTH - WIDTH))
    cam_y = max(0, min(player.y - HEIGHT // 2, MAP_HEIGHT - HEIGHT))
    camera_view = pygame.Rect(cam_x, cam_y, WIDTH, HEIGHT)

    # Nur den sichtbaren Bereich der Map anzeigen
    screen.blit(map_surface, (0, 0), camera_view)

    # Event-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
