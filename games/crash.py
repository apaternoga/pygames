import pygame

def run_crash_game(screen):
    """
    To jest główna funkcja gry Crash.
    """
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(None, 55)

    while running:
        screen.fill((20, 20, 20)) # Ciemne tło

        # Tekst tymczasowy
        text = font.render("Tu bedzie gra CRASH", True, (255, 0, 0))
        screen.blit(text, (100, 100))
        
        instruction = font.render("Nacisnij ESC aby wrocic", True, (200, 200, 200))
        screen.blit(instruction, (100, 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        clock.tick(60)