import random
from core.settings import *

# importuje wartosci takie jak BLACK itd. z stworzonego juz pliku settings
import sys
import pygame

# definicje kolorow i rang kart
suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def draw(self, screen, x, y, hidden=False):
        # Rysujemy cień: daje on efekt głębi
        shadow_rect = pygame.Rect(x + 2, y + 2, 100, 150)
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=8)

        # Główny kształt karty
        rect = pygame.Rect(x, y, 100, 150)
        pygame.draw.rect(screen, WHITE, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        # Jeśli ukryta (karta dealera)
        if hidden:
            # Wzór na "plecach" karty
            inner_rect = pygame.Rect(x + 5, y + 5, 90, 140)
            pygame.draw.rect(screen, RED, inner_rect, border_radius=5)
            # Znak zapytania
            font_hidden = pygame.font.SysFont("Times New Roman", 60, bold=True)
            text_surf = font_hidden.render("?", True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            return

        # Konwersja nazw na symbole
        rank_conversion = {
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": "J",
            "Queen": "Q",
            "King": "K",
            "Ace": "A",
        }
        suits_symbols = {"Hearts": "♥", "Diamonds": "♦", "Spades": "♠", "Clubs": "♣"}

        suit_icon = suits_symbols[self.suit]
        rank_short = rank_conversion[self.rank]

        # Kolor czcionki
        color = RED if self.suit in ["Hearts", "Diamonds"] else BLACK

        rank_str = str(rank_short) 

        # Czcionki
        font_corner = pygame.font.SysFont("Arial", 18, bold=True)
        font_pip = pygame.font.SysFont("Segoe UI Symbol", 28) # Do małych symboli
        font_face = pygame.font.SysFont("Times New Roman", 60) # Do figur

        # --- RYSOWANIE ROGÓW ---

        # Lewy górny
        screen.blit(font_corner.render(rank_str, True, color), (x + 5, y + 5))
        screen.blit(font_corner.render(suit_icon, True, color), (x + 5, y + 25))
        
        # Prawy dolny
        corner_rank_surf = font_corner.render(rank_str, True, color)
        corner_rank_surf = pygame.transform.rotate(corner_rank_surf, 180)
        corner_suit_surf = font_corner.render(suit_icon, True, color)
        corner_suit_surf = pygame.transform.rotate(corner_suit_surf, 180)

        screen.blit(corner_rank_surf, (x + 95 - corner_rank_surf.get_width(), y + 145 - 20))
        screen.blit(corner_suit_surf, (x + 95 - corner_suit_surf.get_width(), y + 145 - 40))

        # Pozycje
        if isinstance(rank_short, int): # LICZBY 2-10
            # Pozycje X
            col_L = 28
            col_M = 50
            col_R = 72
            
            # Pozycje Y
            row_T = 35
            row_MT = 57
            row_C = 75
            row_MB = 93
            row_B = 115
            
            pips = []
            if rank_short == 2:
                pips = [(col_M, row_T), (col_M, row_B)]
            elif rank_short == 3:
                pips = [(col_M, row_T), (col_M, row_C), (col_M, row_B)]
            elif rank_short == 4:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_B), (col_R, row_B)]
            elif rank_short == 5:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_B), (col_R, row_B), (col_M, row_C)]
            elif rank_short == 6:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_C), (col_R, row_C), (col_L, row_B), (col_R, row_B)]
            elif rank_short == 7:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_C), (col_R, row_C), (col_L, row_B), (col_R, row_B), (col_M, row_MT)]
            elif rank_short == 8:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_C), (col_R, row_C), (col_L, row_B), (col_R, row_B), (col_M, row_MT), (col_M, row_MB)]
            elif rank_short == 9:
                 pips = [
                     (col_L, row_T), (col_L, row_MT+3), (col_L,  row_MB-3), (col_L, row_B), # Lewa
                     (col_R, row_T), (col_R, row_MT+3), (col_R,  row_MB-3), (col_R, row_B), # Prawa
                     (col_M, row_C) # Środek
                 ]
            elif rank_short == 10:
                 pips = [
                     (col_L, row_T), (col_L, row_MT+3), (col_L,  row_MB-3), (col_L, row_B), # Lewa
                     (col_R, row_T), (col_R, row_MT+3), (col_R,  row_MB-3), (col_R, row_B), # Prawa
                     (col_M, 48), (col_M, 102) # Dwa w środku
                 ]

            # Rysowanie małych symboli
            for (px, py) in pips:
                pip_surf = font_pip.render(suit_icon, True, color)

                if py > 75:
                    pip_surf = pygame.transform.rotate(pip_surf, 180)

                pip_rect = pip_surf.get_rect(center=(x + px, y + py))
                screen.blit(pip_surf, pip_rect)

        else: 
            # FIGURY (J, Q, K, A)
            if rank_short == "A":
                font_ace = pygame.font.SysFont("Segoe UI Symbol", 80)
                pip_surf = font_ace.render(suit_icon, True, color)
                pip_rect = pip_surf.get_rect(center=(x + 50, y + 75))
                screen.blit(pip_surf, pip_rect)
            else:
                # Dla figur (J, Q, K) ramka i litera
                pygame.draw.rect(screen, color, (x+20, y+30, 60, 90), 1)
                
                face_surf = font_face.render(rank_str, True, color)
                face_rect = face_surf.get_rect(center=(x + 50, y + 75))
                screen.blit(face_surf, face_rect)


class Button:
    def __init__(self, text, x, y, w, h, color=GOLD, text_color=BLACK):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text_color = text_color
        # Kolor po najechaniu
        self.hover_color = (255, 240, 100)
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.is_hovered = False

    def draw(self, screen):
        # Efekt podswietlenia po najechaniu
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        current_color = self.hover_color if self.is_hovered else self.color

        # Rysowanie przycisku
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)

        # Wysrodkowanie tekstu na przycisku
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    # Funkcja ktora zwraca True tylko gdy klikniemy ja lewym przyciskiem myszki
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Deck:

    # ZMIANA: obsługa wielu talii
    def __init__(self, num_decks=6):
        self.deck = []
        self.num_decks = num_decks
        self.create_shoe()

    def create_shoe(self):
        self.deck = []
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit, rank))
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) == 0:
            self.create_shoe()
        return self.deck.pop()

    def needs_shuffle(self):
        return len(self.deck) < (52 * self.num_decks * 0.25)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    # dodajemy karte do reki gracza badz dealera, jesli to as dopasowywujemy najkorzystniejsza wartosc
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1
        self.adjust_for_ace()

    # As moze przyjmowac rozne wartosci, ta funkcja odpowiada za to zeby dopasowac najkorzystniejsza wartosc
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    # iterujac po decku, rysujemy obok siebie karty w przesunieciu o 10 pixeli od poprzedniej karty, (bo karta ma 100)
    def draw(self, screen, start_x, start_y, hide_first=False):
        for i, card in enumerate(self.cards):
            is_hidden = hide_first and i == 0
            card.draw(screen, start_x + (i * 110), start_y, hidden=is_hidden)


class BlackjackGame:
    def __init__(self, screen):
        self.screen = (
            screen  # referencja do glownego okna gry, tym sie zajmujemy juz w mainie
        )
        self.font = pygame.font.SysFont("Arial", 30)
        self.small_font = pygame.font.SysFont("Arial", 20)
        # "Brush Script MT" to standard na Windows/Mac, jak nie ma to wezmie domyslna
        self.logo_font = pygame.font.SysFont("Brush Script MT", 65, italic=True)

        # inicjujemy talie i rece
        self.deck = Deck(num_decks=6)
        # ZMIANA lista rak zamiast jednej reki
        self.player_hands = []
        self.current_hand_index = 0

        self.dealer_hand = Hand()

        # zaleznie od tego jaki jest stan gry, zachowuje sie ona inaczej
        self.state = "betting"
        # self.message="Postaw zaklad, aby zagrac!"
        self.message = "Ustaw stawke i kliknij ROZDAJ"
        self.chips = STARTING_MONEY
        self.current_bet = 10
        self.insurance_bet = 0

        # NOWE: Dynamiczne przyciski
        btn_y = SCREEN_HEIGHT - 65
        btn_w = 110  # Szerokosc przycisku
        spacing = 10  # Odstep miedzy przyciskami

        # Obliczamy pozycje startowa X zeby cala grupa przyciskow byla na srodku
        # Mamy 5 przyciskow akcji
        total_width_buttons = (5 * btn_w) + (4 * spacing)
        start_x = (SCREEN_WIDTH - total_width_buttons) // 2

        self.btn_hit = Button("DOBIERZ", start_x, btn_y, btn_w, 50)
        self.btn_stand = Button(
            "PAS", start_x + (btn_w + spacing) * 1, btn_y, btn_w, 50
        )
        self.btn_double = Button(
            "PODWÓJ",
            start_x + (btn_w + spacing) * 2,
            btn_y,
            btn_w,
            50,
            color=(200, 150, 50),
        )
        self.btn_split = Button(
            "SPLIT",
            start_x + (btn_w + spacing) * 3,
            btn_y,
            btn_w,
            50,
            color=(200, 150, 50),
        )
        self.btn_surrender = Button(
            "PODDAJ",
            start_x + (btn_w + spacing) * 4,
            btn_y,
            btn_w,
            50,
            color=(150, 50, 50),
            text_color=WHITE,
        )

        # Przycisk Rozdaj idealnie na srodku
        self.btn_deal = Button(
            "ROZDAJ KARTY",
            SCREEN_WIDTH // 2 - 100,
            btn_y,
            200,
            50,
            color=WHITE,
            text_color=BLACK,
        )

    def start_round(self):
        self.player_hands = [Hand()]
        self.current_hand_index = 0
        self.dealer_hand = Hand()
        self.player_hands[0].bet = self.current_bet

        # POPRAWKA: Odejmujemy pieniądze na starcie
        self.chips -= self.current_bet

        self.deck = Deck(num_decks=6)
        self.deck.shuffle()

        # Rozdajemy po 2 karty
        self.player_hands[0].add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hands[0].add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        self.state = "player_turn"
        self.message = "Twoj ruch!"

        if self.check_initial_blackjack():
            return

    def check_initial_blackjack(self):
        player_bj = self.player_hands[0].value == 21
        dealer_bj = self.dealer_hand.value == 21

        if player_bj and dealer_bj:
            # Remis: Oddajemy zabraną stawkę
            self.chips += self.current_bet
            self.message = "Remis (Push)! Obaj macie Blackjacka."
            self.state = "game_over"
            return True
        elif player_bj:
            # Wygrana: Oddajemy stawkę + 1.5 stawki wygranej
            win_amount = self.current_bet + int(self.current_bet * 1.5)
            self.chips += win_amount
            self.message = "Blackjack! Wygrywasz 3:2!"
            self.state = "game_over"
            return True
        elif dealer_bj:
            # Przegrana: Nic nie robimy, pieniądze już zabrane w start_round
            pass
        return False

    # funkcja odpowiadajaca za wcisniecia klawiszy ORAZ myszki
    def handle_input(self, event):
        # system obstawiania
        if self.state == "betting":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.chips >= self.current_bet:
                        self.start_round()
                    else:
                        self.message = "Brak srodkow na ten zaklad!"
                elif event.key == pygame.K_UP:
                    if self.chips >= self.current_bet + 10:
                        self.current_bet += 10
                elif event.key == pygame.K_DOWN:
                    if self.chips > 10:
                        self.current_bet -= 10

            # obsluga myszki dla przycisku rozdaj
            if self.btn_deal.is_clicked(event):
                if self.chips >= self.current_bet:
                    self.start_round()
                else:
                    self.message = "Brak srodkow na ten zaklad!"

        # ruch gracza dobiera (HIT) lub nie dobiera(STAY)
        elif self.state == "player_turn":
            current_hand = self.player_hands[self.current_hand_index]

            # zmienna pomocnicza zeby nie pisac kodu dwa razy dla klawiatury i myszki
            action = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    action = "hit"
                elif event.key == pygame.K_s:
                    action = "stand"
                elif event.key == pygame.K_d:
                    action = "double"
                elif event.key == pygame.K_p:
                    action = "split"
                elif event.key == pygame.K_u:
                    action = "surrender"

            # sprawdzamy klikniecia myszka
            if self.btn_hit.is_clicked(event):
                action = "hit"
            elif self.btn_stand.is_clicked(event):
                action = "stand"
            elif self.btn_double.is_clicked(event):
                if self.chips >= self.current_bet and len(current_hand.cards) == 2:
                    action = "double"
            elif self.btn_split.is_clicked(event):
                if (
                    len(current_hand.cards) == 2
                    and current_hand.cards[0].rank == current_hand.cards[1].rank
                    and self.chips >= self.current_bet
                ):
                    action = "split"
            elif self.btn_surrender.is_clicked(event):
                if len(self.player_hands) == 1 and len(current_hand.cards) == 2:
                    action = "surrender"

            # wykonanie akcji
            if (
                action == "hit"
            ):  # jesli gracz kliknie h dodajemy mu karte do reki i sprawdzamy czy przekroczyl wartosc 21
                current_hand.add_card(self.deck.deal())
                if current_hand.value > 21:
                    self.next_hand_or_dealer()

            elif action == "stand":  # jesli s dobieramy karte dealerowi
                self.next_hand_or_dealer()

            # NOWA LOGIKA "DOUBLE DOWN"
            elif action == "double":
                # podwajamy tylko dla aktualnej reki
                if self.chips >= self.current_bet and len(current_hand.cards) == 2:
                    self.chips -= self.current_bet
                    # w prawdziwej grze kazda reka po splicie ma wlasny zaklad
                    # dla uproszczenia przyjmujemy ze current bet to stawka na JEDNA reke
                    current_hand.add_card(self.deck.deal())
                    self.next_hand_or_dealer()
                else:
                    self.message = "Nie mozesz podwoic."

            # NOWA LOGIKA "SPLIT"
            elif action == "split":
                self.perform_split()

            elif action == "surrender":
                refund = self.current_bet // 2
                self.chips += refund
                self.message = f"Poddales sie. Zwrot {refund}."
                self.state = "game_over"

        # to odpowiada za "kliknij spacje zeby zaczac ponownie"
        elif self.state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()

    def perform_split(self):
        # Pobieramy aktualna reke
        current_hand = self.player_hands[self.current_hand_index]
        self.chips -= self.current_bet
        # Zabieramy jedna karte z obecnej reki, by stworzyc nowa
        card_to_move = current_hand.cards.pop()
        new_hand = Hand()
        new_hand.add_card(card_to_move)
        new_hand.bet = self.current_bet
        # Dobieramy po jednej karcie do obu rozdzielonych rąk
        current_hand.add_card(self.deck.deal())
        new_hand.add_card(self.deck.deal())

        # wstawiamy nowa reke zaraz po aktualnej rece w liscie,
        # dzieki czemu gra płynnie przejdzie do niej w nastepnym kroku petli
        self.player_hands.insert(self.current_hand_index + 1, new_hand)
        self.message = "Rozdzielono reke (Split)!"

    def next_hand_or_dealer(self):
        if self.current_hand_index < len(self.player_hands) - 1:
            self.current_hand_index += 1
            self.message = f"Reka {self.current_hand_index + 1} - Twoj ruch"
        else:
            self.state = "dealer_turn"
            self.dealer_logic()

    def dealer_logic(self):
        self.message = "Ruch krupiera..."
        self.draw()
        pygame.display.update()
        pygame.time.wait(500)
        # dealer dobiera karty dopoki ma mniej niz 17 pkt
        # NOWA LOGIKA "Soft 17"
        # Soft 17 czyli kiedy dealer ma 17 ale liczony z asem
        while self.dealer_hand.value < 17 or (
            self.dealer_hand.value == 17 and self.dealer_hand.aces > 0
        ):
            self.dealer_hand.add_card(self.deck.deal())
            self.draw()
            pygame.display.update()
            pygame.time.wait(1000)
        # sprawdzanie warunkow wygranej/przegranej
        final_message = ""
        for i, hand in enumerate(self.player_hands):
            if hand.value > 21:
                final_message += f"Reka {i+1}: Fura! "
            elif self.dealer_hand.value > 21:
                self.chips += hand.bet * 2
                final_message += f"Reka {i+1}: Wygrana! "
            elif hand.value > self.dealer_hand.value:
                self.chips += hand.bet * 2
                final_message += f"Reka {i+1}: Wygrana! "
            elif hand.value < self.dealer_hand.value:
                final_message += f"Reka {i+1}: Przegrana. "
            else:
                self.chips += hand.bet
                final_message += f"Reka {i+1}: Remis. "

        self.message = final_message
        self.state = "game_over"

    def reset_game(self):
        self.state = "betting"
        self.message = "Wcisnij SPACJE lub kliknij ROZDAJ"
        if self.chips < 10:
            self.chips = STARTING_MONEY
            self.message = "Reset srodkow!"

    # funkcja renderujaca - rysuje ona wszystko na ekranie w kazdej klatce
    def draw(self):
        self.screen.fill(GREEN_FELT)

        # NOWE: Kolo na srodku z napisem "Blackjack"
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        pygame.draw.circle(
            self.screen, (30, 120, 30), (center_x, center_y - 50), 120, 5
        )

        # Ozdobny napis w srodku kola
        logo_surf = self.logo_font.render(
            "Blackjack", True, (120, 215, 120)
        )  # bialawy napis
        logo_rect = logo_surf.get_rect(center=(center_x, center_y - 50))
        logo_rect = logo_surf.get_rect(center=(center_x, center_y - 50))
        self.screen.blit(logo_surf, logo_rect)

        panel_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, DARK_PANEL, panel_rect)
        pygame.draw.line(
            self.screen,
            GOLD,
            (0, SCREEN_HEIGHT - 80),
            (SCREEN_WIDTH, SCREEN_HEIGHT - 80),
            3,
        )

        # Wyswietlanie aktualnego zakladu w fazie betting
        bet_info = f"Stawka: {self.current_bet}"
        if self.state == "betting":
            bet_info += " (Gora/Dol)"

        chips_text = self.font.render(f"Zetony: {self.chips} | {bet_info} ", True, GOLD)

        # NOWE: Wiadomosc na samej gorze ekranu
        msg_text = self.font.render(self.message, True, MESSAGE_COLOR)

        # "naklejamy" napisy na ekran
        self.screen.blit(chips_text, (20, SCREEN_HEIGHT - 60))

        # Centrujemy wiadomosc na gorze (y=30)
        msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(msg_text, msg_rect)

        # jesli gra trwa, rysujemy karty (nie jestesmy w menu obstawienia)
        if self.state != "betting":
            hide_dealer = self.state == "player_turn" or self.state == "insurance"

            # Sztywne ustawienie po lewej
            dealer_x = 100

            # wywoluje tutaj narysowanie kart poprzez .draw() dla obiektow Hand()
            self.dealer_hand.draw(self.screen, dealer_x, 100, hide_first=hide_dealer)

            dealer_label = self.small_font.render("Krupier", True, (200, 255, 200))

            label_rect = dealer_label.get_rect(center=(dealer_x + 50, 80))

            self.screen.blit(dealer_label, label_rect)

            # rysowanie rak gracza
            for i, hand in enumerate(self.player_hands):
                # NOWE: Pozycjonowanie przy Splicie
                start_x = 100

                # ODSTĘP PRZY SPLICIE: każda kolejna ręka przesunięta o 600px
                gap = 600

                x_pos = start_x + (i * gap)

                # Strzałka aktywnej ręki
                if self.state == "player_turn" and i == self.current_hand_index:
                    arrow_points = [
                        (x_pos + 50, 360),
                        (x_pos + 40, 350),
                        (x_pos + 60, 350),
                    ]
                    pygame.draw.polygon(self.screen, GOLD, arrow_points)

                    label = self.small_font.render("Twój Ruch", True, GOLD)
                    label_rect = label.get_rect(center=(x_pos + 50, 330))
                    self.screen.blit(label, label_rect)

                hand.draw(self.screen, x_pos, 380)

        # Rysowanie przyciskow
        if self.state == "betting":
            self.btn_deal.draw(self.screen)
        elif self.state == "player_turn":
            current_hand = self.player_hands[self.current_hand_index]
            self.btn_hit.draw(self.screen)
            self.btn_stand.draw(self.screen)

            if len(current_hand.cards) == 2 and self.chips >= self.current_bet:
                self.btn_double.draw(self.screen)

            if (
                len(current_hand.cards) == 2
                and current_hand.cards[0].rank == current_hand.cards[1].rank
                and self.chips >= self.current_bet
            ):
                self.btn_split.draw(self.screen)

            if len(self.player_hands) == 1 and len(current_hand.cards) == 2:
                self.btn_surrender.draw(self.screen)
