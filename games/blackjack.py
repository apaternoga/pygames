import random
from core.settings import *
#importuje wartosci takie jak BLACK itd. z stworzonego juz pliku settings
import sys
import pygame

# definicje kolorow i rang kart
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        pass
    
    #raczej niepotrzebna funkcja, sluzy do tego, ze jak napisze print(Card) to wypisze np Three of Hearts
    def __str__(self):
        return f'{self.rank} of {self.suit}'
        pass
    
    #funkcja odpowiedzialna za wyswietlanie karty na ekranie
    def draw(self,screen,x,y,hidden= False):
        
        #tutaj rysuje tlo karty z czarnym obrysem
        rect= pygame.Rect(x,y,100,150)
        pygame.draw.rect(screen,WHITE,rect,border_radius=5)
        pygame.draw.rect(screen,BLACK,rect,2,border_radius=5)
        
        #jesli karta jest ukryta (karta dealera) to wyswietlimy na karcie duzy znak zapytania
        if hidden:
            font_hidden= pygame.font.SysFont('Arial',80,bold=True)
            text_surf= font_hidden.render("?",True,BLACK)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf,text_rect)
            return
        
        #wyciagam pierwsza litere lub liczbe, aby wyswietlic ja na karcie na ekranie
        rank_conversion= {
            'Two':'2', 'Three':'3', 'Four':'4', 'Five':'5',
            'Six':'6', 'Seven':'7', 'Eight':'8', 'Nine':'9',
            'Ten':'10', 'Jack':'J', 'Queen':'Q', 'King':'K', 'Ace':'A'
        }

        suits_symbols={
            'Hearts': '♥',
            'Diamonds': '♦', 
            'Spades': '♠', 
            'Clubs': '♣'
        }
        
        suit_icon= suits_symbols[self.suit]
        rank_short=rank_conversion[self.rank]
        
        #dla Hearts i Diamonds jest kolor czerwony, dla reszty czarny
        color= RED if self.suit in ['Hearts','Diamonds'] else BLACK
        font= pygame.font.SysFont('Arial',20,bold=True)
        
        #4 linijki ponizej odpowiadaja za wyswietlenia tego co jest wewnatrz karty
        text_surf=font.render(f"{rank_short}",True,color)
        icon_surf=font.render(f"{suit_icon}",True,color)

        screen.blit(text_surf,(x+10,y+10))
        screen.blit(icon_surf,(x+10,y+40))



class Deck:

    #wypelniam deck wszystkimi mozliwymi kartami
    def __init__(self):
        self.deck = []  
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    #znowu, funkcja niepotrzebna, tylko na potrzeby wyprintowania decku
    def __str__(self):
        word = "The deck has: \n"
        for card in self.deck:
            word += card.__str__() + "\n"
        return word
        pass
    
    #tasowanie kart w decku
    def shuffle(self):
        random.shuffle(self.deck)

    #wyciagniecie pierwszej karty z decku
    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    #dodajemy karte do reki gracza badz dealera, jesli to as dopasowywujemy najkorzystniejsza wartosc
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
    
    #iterujac po decku, rysujemy obok siebie karty w przesunieciu o 10 pixeli od poprzedniej karty, (bo karta ma 100)
    def draw(self,screen,start_x,start_y, hide_first=False):
        for i,card in enumerate(self.cards):
            is_hidden=(hide_first and i==0)
            card.draw(screen,start_x+(i*110),start_y,hidden=is_hidden)

class BlackjackGame:
    def __init__(self,screen):
        self.screen=screen #referencja do glownego okna gry, tym sie zajmujemy juz w mainie
        self.font=pygame.font.SysFont('Arial',30)
        self.small_font=pygame.font.SysFont('Arial',20)
        
        #inicjujemy talie i rece
        self.deck=Deck()
        self.deck.shuffle()
        self.player_hand=Hand()
        self.dealer_hand= Hand()

        #zaleznie od tego jaki jest stan gry, zachowuje sie ona inaczej
        self.state='betting'
        self.message="Postaw zaklad, aby zagrac!"
        self.chips=STARTING_MONEY
        self.current_bet=0

    def start_round(self):
        #jesli brakuje srodkow konczymy gre
        if self.chips<10:
            self.message="Brak srodkow! Koniec gry."
            return
        #jesli sa srodki pobieramy 10 , resetujemy talie i rece
        self.current_bet=10
        self.chips -=10
        self.deck=Deck()
        self.deck.shuffle()
        self.player_hand= Hand()
        self.dealer_hand= Hand()

        #rozdajemy po 2 karty dla gracza i dealera
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        
        #zmian stanu gry na ruch gracza
        self.state='player_turn'
        self.message="Twoj ruch: HIT(H) lub STAND(S)"

        #NOWA LOGIKA "Natural Blackjack"
        #Sprawdzam czy gracz ma 21 z rozdania
        if self.player_hand.value==21:
            if self.dealer_hand.value==21:
                self.message= "REMIS (Obaj maja Blackjacka). Zwrot stawki."
                self.chips+=self.current_bet
            else:
                #wygrana 3:2
                win_amount=int(self.current_bet*2.5)
                self.message=f"BLACKJACK! Wygrywasz {win_amount-self.current_bet}$!" 
                self.chips+=win_amount
            self.state='game_over'
    #funkcja odpowiadajaca za wcisniecia klawiszy
    def handle_input(self,event):
        #poczatek gry, gracz zaklada sie wciskac dowolny klawisz
        if self.state== 'betting':
            if event.type == pygame.KEYDOWN:
                self.start_round()

        #ruch gracza dobiera (HIT) lub nie dobiera(STAY)
        elif self.state == 'player_turn':
            if event.type == pygame.KEYDOWN:

                if event.key==pygame.K_h:#jesli gracz kliknie h dodajemy mu karte do reki i sprawdzamy czy przekroczyl wartosc 21
                    self.player_hand.add_card(self.deck.deal())
                    if self.player_hand.value >21:
                        self.state= 'game_over'
                        self.message= "Przegrales! Spacja = nowa gra"

                elif event.key== pygame.K_s:#jesli s dobieramy karte dealerowi
                    self.state= 'dealer_turn'
                    self.dealer_logic()
                
                #NOWA LOGIKA "DOUBLE DOWN"
                elif event.key==pygame.K_d:
                    #Podwoic moznatylko wtedy kiedy masz wystarczajaco srodkow i tylko przy dwoch pierwszych kartach
                    if self.chips>= self.current_bet and len(self.player_hand.cards)==2:
                        self.chips -= self.current_bet
                        self.current_bet*=2
                        self.player_hand.add_card(self.deck.deal())

                        if self.player_hand.value>21:
                            self.state= 'game_over'
                            self.message= f"Double Down nieudany! Strata {self.current_bet}."
                        else:
                            self.state='dealer_turn'
                            self.dealer_logic()
                    else:
                        self.message= "Nie mozesz podwoic (brak srodkow lub zly moment)"
        
        #to odpowiada za "kliknij spacje zeby zaczac ponownie"
        elif self.state == 'game_over':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state= 'betting'
                self.message= "Wcisnij SPACJE zeby zagrac za 10 monet"
                if self.chips<10:
                    self.chips= STARTING_MONEY
                    self.message= "Reset konta! Wcisnij SPACJE."

    #logika dealera
    def dealer_logic(self):
        #dealer dobiera karty dopoki ma mniej niz 17 pkt
        #NOWA LOGIKA "Soft 17"
        #Soft 17 czyli kiedy dealer ma 17 ale liczony z asem
        while self.dealer_hand.value<17 or (self.dealer_hand.value==17 and self.dealer_hand.aces>0):
            self.dealer_hand.add_card(self.deck.deal())

        #sprawdzanie warunkow wygranej
        if self.dealer_hand.value>21:
            win=self.current_bet*2
            self.message= f"Dealer ma FURE! Wygrales {win-self.current_bet}$!"
            self.chips+=win
        elif self.dealer_hand.value<self.player_hand.value:
            win=self.current_bet*2
            self.message= f"Wygrales {win-self.current_bet}$."
            self.chips+=win
        elif self.dealer_hand.value>self.player_hand.value:
            self.message="Dealer wygrywa. Tracisz stawke."
        else:
            self.message= "REMIS. Zwrot stawki"
            self.chips+=self.current_bet
        self.state= "game_over"

    #funkcja renderujaca - rysuje ona wszystko na ekranie w kazdej klatce
    def draw(self):
        self.screen.fill(TABLE_COLOR)

        chips_text=self.font.render(f"Zetony: {self.chips} monet",True, WHITE)
        msg_text= self.small_font.render(self.message,True, WHITE)
        
        #"naklejamy" napisy na ekran
        self.screen.blit(chips_text,(20,20))
        self.screen.blit(msg_text,(20,60))

        #jesli gra trwa, rysujemy karty (nie jestesmy w menu obstawienia)
        if self.state != 'betting':
            #ukrywamy pierwsza karte dealera w turze gracza
            hide_dealer= (self.state=='player_turn')
            
            #wywoluje tutaj narysowanie kart poprzez .draw() dla obiektow Hand(), ktore wywoluja funkcje .draw() dla obiektow Card
            self.dealer_hand.draw(self.screen,150,100, hide_first=hide_dealer)
            self.player_hand.draw(self.screen,150,400)


