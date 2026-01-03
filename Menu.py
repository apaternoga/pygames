import pygame
import sys
from games import blackjack

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

#TWORZENIE PRZYCISKÓW
btn_start = Button(300, 250, 200, 50, "START")
btn_exit = Button(300, 350, 200, 50, "WYJŚCIE")
btn_autorzy = Button(300, 450, 200, 50, "AUTORZY") 

btn_bj = Button(250, 150, 300, 60, "Blackjack")
btn_g2 = Button(250, 250, 300, 60, "Gra 2")
btn_g3 = Button(250, 350, 300, 60, "Gra 3")
btn_back = Button(250, 470, 300, 60, "Powrót")

state = "MENU"

active_game= None

def draw_menu():
    screen.fill(WHITE)
    title_text = font.render("MENU GŁÓWNE", True, BLACK)
    screen.blit(title_text, (275, 100))
    
    btn_start.draw(screen)
    btn_exit.draw(screen)
    btn_autorzy.draw(screen)

def draw_game_placeholder():
    screen.fill((0, 255, 0)) # Zielony
    text = font.render("MINIGIERKI", True, BLACK)
    #back_text = font.render("Naciśnij M, aby wrócić", True, BLACK)
    btn_bj.draw(screen)
    btn_g2.draw(screen)
    btn_g3.draw(screen)
    btn_back.draw(screen)
    screen.blit(text, (300, 75))
    #screen.blit(back_text, (220, 350))

# 2. Główna pętla programu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if state == "MENU":
            
            if btn_start.is_clicked(event):
                state = "GRY"
            
            if btn_autorzy.is_clicked(event):
                print("Tu wyświetlimy autorów!")
            
            if btn_exit.is_clicked(event):
                running = False
        
        elif state == "GRY":
            if btn_bj.is_clicked(event):
                active_game = blackjack.BlackjackGame(screen)
                state = "GRA"
            if btn_g2.is_clicked(event):
                print("Wybrano Grę 2")
                state = "GRA"
            if btn_g3.is_clicked(event):
                print("Wybrano Grę 3")
                state = "GRA"
            if btn_back.is_clicked(event):
                state = "MENU"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
        
        elif state == "GRA":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "GRY"
                    active_game = None

                if active_game:
                    active_game.handle_input(event)

    if state == "MENU":
        draw_menu()
    elif state == "GRY":
        draw_game_placeholder()
    elif state == "GRA":
        if active_game:
            active_game.draw()
        else:
            draw_game_placeholder()

    pygame.display.flip()

pygame.quit()
sys.exit()