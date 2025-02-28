import pygame


def show_start_screen():
    # Farben definieren
    WHITE = (240, 240, 240)
    BLACK = (30, 30, 30)
    GRAY = (180, 180, 180)
    BLUE = (70, 130, 180)
    LIGHT_BLUE = (100, 149, 237)
    HOVER_BLUE = (50, 100, 160)
    SHADOW = (200, 200, 200)

    # Pygame initialisieren
    pygame.init()

    # Fenstergröße
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Etintrof - Start Screen")

    # Schriftart
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 48)
    input_box = pygame.Rect(150, 150, 300, 50)
    button_box = pygame.Rect(225, 250, 150, 50)

    ip_address = ""
    running = True
    active = False
    hover = False
    placeholder = "192.168.1.1"

    # Begrüßungstext
    text_begruesung = large_font.render("Willkommen bei Etintrof", True, BLACK)
    textRect_begruesung = text_begruesung.get_rect(center=(WIDTH // 2, 60))

    while running:
        screen.fill(WHITE)

        # Schatten für den Text
        shadow_text = large_font.render("Willkommen bei Etintrof", True, SHADOW)
        screen.blit(shadow_text, (textRect_begruesung.x + 2, textRect_begruesung.y + 2))
        screen.blit(text_begruesung, textRect_begruesung)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = button_box.collidepoint(mouse_x, mouse_y)

        # Ereignisse verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
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
        text_color = BLACK if ip_address else (150, 150, 150)  # Grauer Text für Platzhalter
        text_surface = font.render(display_text, True, text_color)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 12))

        # Start-Button zeichnen
        pygame.draw.rect(screen, HOVER_BLUE if hover else BLUE, button_box, border_radius=10)
        button_text = font.render("Start", True, WHITE)
        screen.blit(button_text, (button_box.x + 50, button_box.y + 10))

        pygame.display.flip()


if __name__ == "__main__":
    address = show_start_screen()
    print("Eingegebene IP-Adresse:", address)