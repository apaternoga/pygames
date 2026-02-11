import math
import os, pygame, sys
from games import blackjack
from core.settings import *
from core.ui_elements import Button, Button2, BlackjackIcon, CrashIcon, Slider 
from core import screens

WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT

class Menu:
    def __init__(self, screen, sound_manager, wallet):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # --- SOUND MANAGER ---
        self.sm = sound_manager
        if not pygame.mixer.music.get_busy():
            self.sm.play_music("jazz_playlist.mp3")

        # --- PORTFEL ---
        self.wallet = wallet

        self.state = "MENU"
        self.active_game = None
        
        # --- ZMIENNE SCROLLOWANIA ---
        self.instr_scroll = 0      # Pozycja tekstu
        self.credits_scroll = 0    # Pozycja tekstu credits
        self.is_dragging = False   # Czy trzymamy suwak myszką?
        
        # Suwak inicjujemy głośnością pobraną z Sound Managera
        current_vol = getattr(self.sm, 'volume_music', 0.1) 
        self.vol_slider = Slider(-1, 360, 600, current_vol)
        
        # --- GRAFIKA ---
        try:
            self.bg_image = pygame.image.load(os.path.join("assets", "images", "tlo_menu.jpg")).convert()
            self.bg_image = pygame.transform.smoothscale(self.bg_image, (self.width, self.height))
        except:
            self.bg_image = None

        try:
            self.logo = pygame.image.load(os.path.join("assets", "images", "PyVegas_napis.png")).convert_alpha()
            self.logo = pygame.transform.smoothscale(self.logo, (self.logo.get_width() //2, self.logo.get_height() //2))
        except:
            self.logo = None
        self.logo_scale=1.0

        self.pyzeton_img = None
        try:
            self.pyzeton_img = pygame.image.load(os.path.join("assets", "images", "PyZeton.png")).convert_alpha()
            self.pyzeton_img = pygame.transform.smoothscale(self.pyzeton_img, (150, 150))
            self.pyzeton_rect = self.pyzeton_img.get_rect(center=(145, 600))
        except: pass

        self.font = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 55)
        self.font_small = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 50)
        self.font_smaller = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 45)
        self.font_large = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 85) 

        # --- PRZYCISKI ---
        self.btns = {
            'start':    Button(-1, 320, 380, 90, "START"),
            'settings': Button(-1, 430, 380, 90, "SETTINGS"),
            'exit':     Button(1080, 630, 160, 65, "EXIT"),

            'instr':    Button(-1, 200, 400, 80, "INSTRUCTIONS"),
            'credits':  Button(-1, 300, 400, 80, "CREDITS"),
            'music_m':  Button(-1, 400, 400, 80, "MUSIC"),
            'back':     Button(-1, 580, 300, 60, "BACK"), 
            
            'back_instr': Button(-1, 620, 300, 60, "BACK"),

            'yes':      Button(460, 380, 180, 70, "YES"),
            'no':       Button(680, 380, 180, 70, "NO"),

            't1':       Button(330, 230, 300, 55, "JAZZ MIX"),
            't2':       Button(650, 230, 300, 55, "LOFI CHILL"),
            'stop':     Button(-1, 450, 400, 50, "SOUND ON / OFF"),

            'bj':       Button2(300, 300, 300, 200, "Blackjack", icon_renderer=BlackjackIcon()),
            'cr':       Button2(700, 300, 300, 200, "Crash", icon_renderer=CrashIcon()),
        }

    def update(self):
        # 1. Animacje (niezależne od zdarzeń)
        if self.state in ["MENU", "GRY"]:
            self.logo_scale = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() * 0.0035)

        # 2. Pętla zdarzeń - pobiera WSZYSTKIE zdarzenia z kolejki naraz
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return "EXIT_APP"

            # --- MENU ---
            if self.state == "MENU":
                if self.btns['start'].is_clicked(event): self.state = "GRY"
                if self.btns['settings'].is_clicked(event): self.state = "SETTINGS"
                if self.btns['exit'].is_clicked(event): self.state = "EXIT"

                # sprawdź PyZeton
                if self.pyzeton_img and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.pyzeton_rect.collidepoint(event.pos):
                        # Dokładniejsze sprawdzanie koła
                        center = self.pyzeton_rect.center
                        radius = min(self.pyzeton_rect.width, self.pyzeton_rect.height) / 2
                        if (event.pos[0] - center[0]) ** 2 + (event.pos[1] - center[1]) ** 2 <= radius ** 2:
                            self.wallet.balance = self.wallet.start_money
                            self.wallet.save()
                            if self.sm: self.sm.play_sound('click')
            
            elif self.state == "EXIT":
                if self.btns['yes'].is_clicked(event): return "EXIT_APP" 
                if self.btns['no'].is_clicked(event): self.state = "MENU"

            elif self.state == "GRY":
                if self.btns['bj'].is_clicked(event): return "BLACKJACK"
                if self.btns['cr'].is_clicked(event): return "CRASH"
                if self.btns['back'].is_clicked(event): self.state = "MENU"

            elif self.state == "SETTINGS":
                if self.btns['music_m'].is_clicked(event): self.state = "SETTINGS_MUSIC"
                
                if self.btns['instr'].is_clicked(event): 
                    self.state = "INSTRUCTIONS"
                    self.instr_scroll = 0 
                    self.is_dragging = False

                if self.btns['credits'].is_clicked(event):
                    self.state = "CREDITS"
                    self.credits_scroll = 0
                    self.is_dragging = False

                if self.btns['back'].is_clicked(event): self.state = "MENU"

            # --- INSTRUKCJE (LOGIKA MYSZKI) ---
            elif self.state == "INSTRUCTIONS":
                if self.btns['back_instr'].is_clicked(event):
                    self.state = "SETTINGS"
                
                viewport_y = 100            
                viewport_h = HEIGHT - 220   
                scrollbar_x = (WIDTH - 200) + 100 + 10 
                thumb_height = 60
                max_scroll = 480

                # 1. Obsługa kółka myszy (Scroll Wheel)
                if event.type == pygame.MOUSEWHEEL:
                    self.instr_scroll -= event.y * 30  # Zwiększyłem prędkość scrolla, bo działa płynniej

                # 2. Kliknięcie myszką (złapanie suwaka)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        progress = self.instr_scroll / max_scroll if max_scroll > 0 else 0
                        thumb_y = viewport_y + progress * (viewport_h - thumb_height)
                        thumb_rect = pygame.Rect(scrollbar_x - 5, thumb_y, 25, thumb_height) 
                        
                        if thumb_rect.collidepoint(event.pos):
                            self.is_dragging = True

                # 3. Puszczenie myszki
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_dragging = False

                # 4. Ruch myszką (gdy trzymamy suwak)
                elif event.type == pygame.MOUSEMOTION:
                    if self.is_dragging:
                        rel_y = event.rel[1]
                        track_len = viewport_h - thumb_height
                        if track_len > 0:
                            scroll_change = (rel_y / track_len) * max_scroll
                            self.instr_scroll += scroll_change

            # --- CREDITS (LOGIKA MYSZKI) ---
            elif self.state == "CREDITS":
                if self.btns['back_instr'].is_clicked(event):
                    self.state = "SETTINGS"
                
                viewport_y = 100            
                viewport_h = HEIGHT - 220   
                scrollbar_x = (WIDTH - 200) + 100 + 10 
                thumb_height = 60
                max_scroll = 180

                # 1. Scroll Wheel
                if event.type == pygame.MOUSEWHEEL:
                    self.credits_scroll -= event.y * 30

                # 2. Kliknięcie (złapanie suwaka)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        progress = self.credits_scroll / max_scroll if max_scroll > 0 else 0
                        thumb_y = viewport_y + progress * (viewport_h - thumb_height)
                        thumb_rect = pygame.Rect(scrollbar_x - 5, thumb_y, 25, thumb_height) 
                        
                        if thumb_rect.collidepoint(event.pos):
                            self.is_dragging = True

                # 3. Puszczenie myszki
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_dragging = False

                # 4. Ruch myszką
                elif event.type == pygame.MOUSEMOTION:
                    if self.is_dragging:
                        rel_y = event.rel[1]
                        track_len = viewport_h - thumb_height
                        if track_len > 0:
                            scroll_change = (rel_y / track_len) * max_scroll
                            self.credits_scroll += scroll_change

            elif self.state == "SETTINGS_MUSIC":
                if self.btns['back'].is_clicked(event): self.state = "SETTINGS"
                
                if self.vol_slider.handle_event(event):
                    self.sm.set_volume_music(self.vol_slider.value)

                if self.btns['t1'].is_clicked(event):
                    self.sm.play_music("jazz_playlist.mp3")
                
                if self.btns['t2'].is_clicked(event):
                    self.sm.play_music("lofi_playlist.mp3")

                if self.btns['stop'].is_clicked(event):
                    if hasattr(self.sm, 'toggle_mute'):
                        self.sm.toggle_mute()
                    else:
                        current = getattr(self.sm, 'is_muted', False)
                        self.sm.mute(not current)
        
        # 3. Logika poza pętlą zdarzeń (np. klampowanie wartości, żeby nie uciekły)
        # To zapobiega błędom przy bardzo szybkim scrollowaniu
        if self.state == "INSTRUCTIONS":
            max_scroll = 480
            if self.instr_scroll < 0: self.instr_scroll = 0
            if self.instr_scroll > max_scroll: self.instr_scroll = max_scroll

        if self.state == "CREDITS":
            max_scroll = 180
            if self.credits_scroll < 0: self.credits_scroll = 0
            if self.credits_scroll > max_scroll: self.credits_scroll = max_scroll

        return True

    def draw(self):
        if self.state == "GRA" and self.active_game:
            self.active_game.draw()
            return
        if self.sm.muted:
            current_vol = self.sm.previous_volume_music
        else:
            current_vol = self.sm.volume_music
        is_muted = getattr(self.sm, 'muted', False) or (current_vol == 0.0)
        

        if self.state == "MENU":
            screens.draw_menu(self.screen, self.bg_image, self.btns, self.font, self.logo, self.logo_scale, self.wallet.balance, self.pyzeton_img, self.pyzeton_rect)
        elif self.state == "EXIT":
            screens.draw_exit(self.screen, self.bg_image, self.btns, self.font, self.font_small)
        elif self.state == "SETTINGS":
            screens.draw_settings(self.screen, self.bg_image, self.btns, self.font, self.font_large)
        
        elif self.state == "INSTRUCTIONS":
            screens.draw_instructions(self.screen, self.bg_image, self.btns, self.font, self.font_smaller, self.instr_scroll)

        elif self.state == "CREDITS":
            screens.draw_credits(self.screen, self.bg_image, self.btns, self.font, self.font_smaller, self.credits_scroll)
            
        elif self.state == "SETTINGS_MUSIC":
            self.vol_slider.value = current_vol
            screens.draw_settings_music(
                self.screen, self.bg_image, self.btns, self.font, self.font_smaller, 
                current_vol, self.vol_slider, is_muted
            )
        elif self.state == "GRY":
            screens.draw_game_placeholder(self.screen, self.bg_image, self.btns, self.font, self.logo, self.logo_scale, self.wallet.balance)