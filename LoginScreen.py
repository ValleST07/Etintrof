import pygame


def get_IP():
    # Farben definieren
    WHITE = (240, 240, 240)
    BLACK = (30, 30, 30)
    GRAY = (180, 180, 180)
    BLUE = (70, 130, 180)
    LIGHT_BLUE = (100, 149, 237)
    HOVER_BLUE = (50, 100, 160)

    # Pygame initialisieren
    pygame.init()

    # Fenstergröße und Modus
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Etintrof - Start Screen")
    fullscreen = False

    # Schriftart
    def get_fonts(height):
        return pygame.font.Font(None, height // 20), pygame.font.Font(None, height // 15)

    font, large_font = get_fonts(HEIGHT)

    def get_rects(width, height):
        return (
            pygame.Rect(width // 4, height // 3, width // 2, height // 12),
            pygame.Rect(width // 3, height // 1.5, width // 3, height // 12)
        )

    input_box, button_box = get_rects(WIDTH, HEIGHT)

    ip_address = ""
    running = True
    active = False
    placeholder = "192.168.1.1"

    while running:
        screen.fill(WHITE)

        # Begrüßungstext aktualisieren
        text_begruesung = large_font.render("Willkommen bei Etintrof", True, BLACK)
        textRect_begruesung = text_begruesung.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        screen.blit(text_begruesung, textRect_begruesung)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = button_box.collidepoint(mouse_x, mouse_y)

        # Ereignisse verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    WIDTH, HEIGHT = screen.get_size()
                    font, large_font = get_fonts(HEIGHT)
                    input_box, button_box = get_rects(WIDTH, HEIGHT)
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                font, large_font = get_fonts(HEIGHT)
                input_box, button_box = get_rects(WIDTH, HEIGHT)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if button_box.collidepoint(event.pos):
                    return ip_address if ip_address else placeholder
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    return ip_address if ip_address else placeholder
                elif event.key == pygame.K_BACKSPACE:
                    ip_address = ip_address[:-1]
                else:
                    ip_address += event.unicode

        # Input-Feld zeichnen
        pygame.draw.rect(screen, LIGHT_BLUE if active else GRAY, input_box, border_radius=10)
        display_text = ip_address if ip_address else placeholder
        text_color = BLACK if ip_address else (150, 150, 150)
        text_surface = font.render(display_text, True, text_color)
        text_rect = text_surface.get_rect(center=input_box.center)
        screen.blit(text_surface, text_rect.topleft)

        # Start-Button zeichnen
        pygame.draw.rect(screen, HOVER_BLUE if hover else BLUE, button_box, border_radius=10)
        button_text = font.render("Start", True, WHITE)
        text_rect = button_text.get_rect(center=button_box.center)
        screen.blit(button_text, text_rect.topleft)

        pygame.display.flip()