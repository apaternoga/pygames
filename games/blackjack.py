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
            "Two": "2",
            "Three": "3",
            "Four": "4",
            "Five": "5",
            "Six": "6",
            "Seven": "7",
            "Eight": "8",
            "Nine": "9",
            "Ten": "10",
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

        # Czcionki
        font_small = pygame.font.SysFont("Arial", 18, bold=True)
        font_large = pygame.font.SysFont("Segoe UI Symbol", 60)  # Duży symbol na środku

        # Lewy górny róg
        screen.blit(font_small.render(rank_short, True, color), (x + 8, y + 8))
        screen.blit(font_small.render(suit_icon, True, color), (x + 8, y + 28))

        # Duży symbol na środku karty
        icon_surf = font_large.render(suit_icon, True, color)
        icon_rect = icon_surf.get_rect(center=rect.center)
        screen.blit(icon_surf, icon_rect)


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

        # inicjujemy talie i rece
        self.deck = Deck(num_decks=6)
        # ZMIANA lista rak zamiast jednej reki
        self.player_hands = []
        self.current_hand_index = 0

        self.dealer_hand = Hand()

        # zaleznie od tego jaki jest stan gry, zachowuje sie ona inaczej
        self.state = "betting"
        self.message = "Postaw zaklad, aby zagrac!"
        self.chips = STARTING_MONEY
        self.current_bet = 10
        self.insurance_bet = 0
        self.message = "Ustaw stawke przy pomocy strzałek. Spacja = start."

    def start_round(self):
        if self.deck.needs_shuffle():
            self.deck.create_shoe()
            self.message = "Tasowanie kart..."
        self.chips -= self.current_bet
        self.insurance_bet = 0
        # ZMIANA
        self.player_hands = [Hand()]
        self.current_hand_index = 0
        self.dealer_hand = Hand()

        self.player_hands[0].add_card(self.deck.deal())
        self.player_hands[0].add_card(self.deck.deal())

        # rozdajemy po 2 karty dla dealera
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        dealer_up_card = self.dealer_hand.cards[1]

        if dealer_up_card == "Ace":
            self.state = "insurance"
            insurance_cost = self.current_bet // 2
            self.message = (
                f"Dealer ma Asa. Ubezpieczenie? Koszt: {insurance_cost} (T/N)"
            )
        else:
            self.check_initial_blackjack()

    # nowa funkcja
    def check_initial_blackjack(self):
        # sprawdzanie natural blackjacka
        if self.player_hands[0].value == 21:
            if self.dealer_hand.value == 21:
                self.message = "REMIS (Obaj maja Blackjacka). Zwrot."
                self.chips += self.current_bet
                self.state = "game_over"
            else:
                win_amount = int(self.current_bet * 2.5)
                self.message = f"BLACKJACK! Wygrywasz {win_amount- self.current_bet}$"
                self.chips += win_amount
                self.state = "game_over"
        else:
            # jesli nikt nie ma BJ or razu to gramy dalej
            # amerykanska wersja BJ tez sie konczy gdy dealer ma 21 a gracz nie
            if self.dealer_hand.value == 21:
                self.state = "game_over"
                self.message = "Dealer ma Blackjacka! Przegrales."
            else:
                self.state = "player_turn"
                self.message = (
                    "Ruch: H(Hit), S(Stand), D(Double), P(Split), U(Surrender)"
                )

    # funkcja odpowiadajaca za wcisniecia klawiszy
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

        # ruch gracza dobiera (HIT) lub nie dobiera(STAY)
        elif self.state == "player_turn":
            current_hand = self.player_hands[self.current_hand_index]
            if event.type == pygame.KEYDOWN:

                if (
                    event.key == pygame.K_h
                ):  # jesli gracz kliknie h dodajemy mu karte do reki i sprawdzamy czy przekroczyl wartosc 21
                    current_hand.add_card(self.deck.deal())
                    if current_hand.value > 21:
                        self.next_hand_or_dealer()

                elif event.key == pygame.K_s:  # jesli s dobieramy karte dealerowi
                    self.next_hand_or_dealer()

                # NOWA LOGIKA "DOUBLE DOWN"
                elif event.key == pygame.K_d:
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
                elif event.key == pygame.K_p:
                    if (
                        len(current_hand.cards) == 2
                        and current_hand.cards[0].rank == current_hand.cards[1].rank
                        and self.chips >= self.current_bet
                    ):
                        self.perform_split()
                elif event.key == pygame.K_u:
                    if len(self.player_hands) == 1 and len(current_hand.cards) == 2:
                        refund = self.current_bet // 2
                        self.chips += refund
                        self.message = f"Poddales sie. Zwrot {refund}."
                        self.state = "game_over"
                    else:
                        self.message = "Za pozno na poddanie!"

        # to odpowiada za "kliknij spacje zeby zaczac ponownie"
        elif self.state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "betting"
                self.message = "Wcisnij SPACJE"
                if self.chips < 10:
                    self.chips = STARTING_MONEY
                    self.message = "Reset srodkow!"

    def resolve_insurance(self):
        if self.dealer_hand.value == 21:
            self.message = "Dealer ma Blackjacka!"
            self.state = "game_over"

            # Wypłata ubezpieczenia 2:1
            if self.insurance_bet > 0:
                self.chips += self.insurance_bet * 3  # Zwrot stawiki ubezp + wygrana 2x
                self.message += "Wygrywasz ubezpieczenie."
            else:
                self.message += " Przegrales."
            # Gracz traci glowny zaklad
            # w pelnym kasynie jak gracz ma bj to jest 'even money' ale tu upraszczamy - dealer BJ wygrywa main bet
        else:
            self.message = "Dealer nie ma Blackjacka. Graj dalej."
            self.check_initial_blackjack()

    # nowa funkcja odpowiadajaca za split
    def perform_split(self):
        self.chips -= self.current_bet

        current_hand = self.player_hands[self.current_hand_index]

        split_card = current_hand.cards.pop()

        current_hand.value -= values[split_card.rank]
        if split_card.rank == "Ace":
            current_hand.aces -= 1

        new_hand = Hand()
        new_hand.add_card(split_card)

        current_hand.add_card(self.deck.deal())
        new_hand.add_card(self.deck.deal())

        self.player_hands.append(new_hand)

        self.message = "SPLIT! Grasz pierwsza reka."

    #
    def next_hand_or_dealer(self):
        if self.current_hand_index < len(self.player_hands) - 1:
            self.current_hand_index += 1
            self.message = f"Grasz reka numer {self.current_hand_index+1}"
        else:
            self.state = "dealer_turn"
            self.dealer_logic()

    # logika dealera
    def dealer_logic(self):
        # dealer dobiera karty dopoki ma mniej niz 17 pkt
        # NOWA LOGIKA "Soft 17"
        # Soft 17 czyli kiedy dealer ma 17 ale liczony z asem
        while self.dealer_hand.value < 17 or (
            self.dealer_hand.value == 17 and self.dealer_hand.aces > 0
        ):
            self.dealer_hand.add_card(self.deck.deal())
        self.state = "game_over"
        self.message = ""

        total_win = 0

        for i, hand in enumerate(self.player_hands):
            bet = self.current_bet

            result_msg = ""

            if hand.value > 21:
                result_msg = "Porażka (Fura)"
            elif self.dealer_hand.value > 21:
                result_msg = "Wygrana"
                self.chips += bet * 2
                total_win += bet
            elif self.dealer_hand.value > hand.value:
                result_msg = "Porażka"
            else:
                result_msg = "Remis"
                self.chips += bet
            if len(self.player_hands) > 1:
                self.message += f"R{i+1}: {result_msg} | "
            else:
                self.message = f"Dealer: {self.dealer_hand.value}. {result_msg}."
        if len(self.player_hands) > 1:
            self.message += "Spacja = Start"

    # funkcja renderujaca - rysuje ona wszystko na ekranie w kazdej klatce
    def draw(self):
        #  Tło i panel (bez zmian)
        self.screen.fill(GREEN_FELT)
        # Koło na środku
        pygame.draw.circle(
            self.screen,
            (30, 120, 30),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50),
            100,
            5,
        )

        panel_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, DARK_PANEL, panel_rect)
        pygame.draw.line(
            self.screen,
            GOLD,
            (0, SCREEN_HEIGHT - 80),
            (SCREEN_WIDTH, SCREEN_HEIGHT - 80),
            3,
        )

        # Wyświetlanie informacji (bez zmian)
        bet_info = f"STAWKA: {self.current_bet}$"
        if self.state == "betting":
            bet_info += " (↕ Zmień)"

        chips_surf = self.font.render(f"BANK: {self.chips}$", True, GOLD)
        bet_surf = self.font.render(bet_info, True, WHITE)
        self.screen.blit(chips_surf, (20, SCREEN_HEIGHT - 60))
        self.screen.blit(bet_surf, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 60))

        msg_font = self.font if len(self.message) < 30 else self.small_font
        msg_surf = msg_font.render(self.message, True, MESSAGE_COLOR)
        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(msg_surf, msg_rect)

        # Rysowanie kart
        if self.state != "betting":
            # Dealer (bez zmian)
            hide_dealer = self.state == "player_turn" or self.state == "insurance"
            dealer_label = self.small_font.render("Krupier", True, (200, 255, 200))
            self.screen.blit(dealer_label, (150, 70))
            self.dealer_hand.draw(self.screen, 150, 100, hide_first=hide_dealer)

            for i, hand in enumerate(self.player_hands):

                # Pozycja startowa: 150px od lewej krawędzi
                start_x = 150

                # ODSTĘP PRZY SPLICIE: każda kolejna ręka przesunięta o 750px
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
