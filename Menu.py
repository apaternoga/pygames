import pygame
import sys

# 1. Inicjalizacja ekranu
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Nasza Gra - Menu")
font = pygame.font.SysFont("Arial", 40)

# Kolory 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150) # Dodatkowy kolor dla efektu najechania

# --- KLASA PRZYCISKU (Tu pracuje osoba od grafiki i logiki) ---
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        
    def draw(self, surface):
        # Pobierz pozycję myszki
        mouse_pos = pygame.mouse.get_pos()
        
        # LOGIKA GRAFIKA: Zmiana koloru jeśli myszka najeżdża na przycisk
        current_color = DARK_GRAY if self.rect.collidepoint(mouse_pos) else self.color
        
        # Rysowanie prostokąta
        pygame.draw.rect(surface, current_color, self.rect)
        
        # Rysowanie tekstu (wyśrodkowanego automatycznie!)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # LOGIKA PROGRAMISTY: Sprawdź, czy kliknięto w ten przycisk
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# --- TWORZENIE PRZYCISKÓW (Robimy to raz, przed pętlą) ---
btn_start = Button(300, 250, 200, 50, "START")
btn_exit = Button(300, 350, 200, 50, "WYJŚCIE")

state = "MENU"

def draw_menu():
    screen.fill(WHITE)
    title_text = font.render("MENU GŁÓWNE", True, BLACK)
    screen.blit(title_text, (275, 100))
    
    # ZOBACZ: Zamiast 10 linii kodu, mamy tylko to:
    btn_start.draw(screen)
    btn_exit.draw(screen)

def draw_game_placeholder():
    screen.fill((0, 255, 0)) # Zielony
    text = font.render("TU BĘDĄ MINIGIERKI", True, BLACK)
    back_text = font.render("Naciśnij M, aby wrócić", True, BLACK)
    screen.blit(text, (200, 250))
    screen.blit(back_text, (220, 350))

# 2. Główna pętla programu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if state == "MENU":
            # ZOBACZ: Nie musisz już wpisywać ręcznie liczb (300 <= mouse_pos[0]...)
            # Klasa sama wie, gdzie jest przycisk!
            if btn_start.is_clicked(event):
                state = "GRA"
            
            if btn_exit.is_clicked(event):
                running = False
        
        elif state == "GRA":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    state = "MENU"

    if state == "MENU":
        draw_menu()
    elif state == "GRA":
        draw_game_placeholder()

    pygame.display.flip()

pygame.quit()
sys.exit()