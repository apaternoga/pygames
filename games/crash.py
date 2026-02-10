import math
import os
import pygame.gfxdraw
import pygame
import random

# Colors
COLORS = {
    "bg_dark": (15, 23, 42),
    "bg_panel": (30, 41, 59),
    "accent_green": (16, 185, 129),
    "accent_red": (239, 68, 68),
    "accent_yellow": (245, 158, 11),
    "text_white": (248, 250, 252),
    "text_gray": (148, 163, 184),
    "input_bg": (51, 65, 85),
    "glow_green": (16, 185, 129, 50),
    "glow_red": (239, 68, 68, 50)
}

class CrashGame:
    def __init__(self, screen, sm, wallet):
        self.screen = screen
        self.W, self.H = screen.get_size()
        self.sm = sm
        self.wallet = wallet
        self.exit_requested = False
        
        # Audio setup
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Fonts
        self.font_main = pygame.font.SysFont("Arial Rounded MT Bold", 120, bold=True)
        self.font_ui = pygame.font.SysFont("Verdana", 24)
        self.font_mono = pygame.font.SysFont("Consolas", 28, bold=True)

        # Variables
        self.current_bet = 0
        self.game_history = [] 
        
        # Inputs
        self.bet_input_text = "10"
        self.auto_cashout_text = "2.00"
        self.active_input = "BET"
        self.auto_cashout_on = False
        
        # Game state
        self.state = "BETTING"
        self.current_multiplier = 1.00
        self.target_crash = 1.00
        self.cashout_point = 0.0
        self.growth_speed = 0.01
        self.history_points = [1.0]
        self.last_delta = 0.0
        
        # Rects
        center_x = self.W // 2
        self.rect_graph = pygame.Rect(50, 50, self.W - 100, self.H - 300)
        
        self.panel_y = self.H - 200
        self.rect_panel_bg = pygame.Rect(0, self.panel_y, self.W, 200)
        
        margin = 40
        input_w = 240
        btn_w = 110
        gap = 10

        bet_x = margin
        auto_x = self.W - margin - input_w - gap - btn_w

        base_center_y = self.panel_y + 105

        self.rect_input_bet = pygame.Rect(bet_x, base_center_y - 36, input_w, 72)
        self.rect_btn_double = pygame.Rect(self.rect_input_bet.right + gap, self.rect_input_bet.y, btn_w, 32)
        self.rect_btn_half = pygame.Rect(self.rect_input_bet.right + gap, self.rect_input_bet.y + 40, btn_w, 32)
        self.rect_input_auto = pygame.Rect(auto_x, base_center_y - 36, input_w, 72)
        self.rect_toggle_auto = pygame.Rect(self.rect_input_auto.right + gap, base_center_y - 30, btn_w, 60)
        self.rect_btn_action = pygame.Rect(center_x - 150, base_center_y - 40, 300, 80)
        self.rect_btn_exit = pygame.Rect(self.W - 120, 20, 100, 40)

        self.error_msg = ""
        self.error_timer = 0
        self.hover_states = {
            "half": False,
            "double": False,
            "toggle": False,
            "action": False,
        }
        
    def can_exit(self):
        # POPRAWKA: Można wyjść tylko gdy portfel nie jest zaangażowany w trwający lot
        return self.state == "BETTING" or self.state == "SUCCESS" or self.state == "CRASHED"

    def draw_rounded_rect(self, surface, color, rect, radius=10):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def draw_inner_glow(self, rect, color, alpha=70, radius=8):
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        glow_color = (color[0], color[1], color[2], alpha)
        pygame.draw.rect(overlay, glow_color, overlay.get_rect(), border_radius=radius)
        self.screen.blit(overlay, (rect.x, rect.y))

    def _handle_hover(self, key, hovered):
        if hovered != self.hover_states.get(key, False):
            if self.sm:
                self.sm.play_sound("hover")
        self.hover_states[key] = hovered

    def draw_gradient_bg(self):
        self.screen.fill(COLORS["bg_dark"])
        # Grid lines
        for x in range(0, self.W, 40):
            pygame.draw.line(self.screen, (20, 30, 50), (x, 0), (x, self.H))
        for y in range(0, self.H, 40):
            pygame.draw.line(self.screen, (20, 30, 50), (0, y), (self.W, y))

    def _generate_crash_point(self):
        # Crash-point algorithm
        r = random.random()
        house_edge = 0.01
        if r == 0: r = 0.0000001
        crash = (1 - house_edge) / r
        return max(1.00, int(crash * 100) / 100.0)

    def show_error(self, msg):
        self.error_msg = msg
        self.error_timer = 120

    def _parse_amount(self, text):
        try:
            return float(text)
        except:
            return 0.0

    def _format_amount(self, value):
        if value <= 0:
            return "0"
        if value.is_integer():
            return str(int(value))
        return f"{value:.2f}".rstrip("0").rstrip(".")

    def _display_balance(self):
        return math.floor(self.wallet.balance * 100) / 100

    def _apply_bet_multiplier(self, factor):
        if self.state == "RUNNING":
            return
        amount = self._parse_amount(self.bet_input_text)
        if amount <= 0:
            amount = 1.0
        amount *= factor
        max_bet = self._display_balance()
        if max_bet > 0:
            amount = min(amount, max_bet)
        self.bet_input_text = self._format_amount(amount)
        self.active_input = "BET"

    def start_round(self):
        if self.state == "RUNNING": return
        
        # Validation
        try:
            bet = float(self.bet_input_text)
        except:
            bet = 0.0
            
        max_bet = self._display_balance()
        if max_bet <= 0:
            self.current_bet = 0
            return self.show_error("No Funds")
        if bet <= 0:
            self.current_bet = 0
            return self.show_error("Invalid Bet")
        if bet > max_bet:
            self.current_bet = 0
            return self.show_error("No Funds")
        
        if self.auto_cashout_on:
            try:
                if float(self.auto_cashout_text) < 1.01: return self.show_error("Min Auto 1.01x")
            except:
                return self.show_error("Bad Input")

        # Start logic
        self.wallet.balance -= bet
        self.current_bet = bet
        self.target_crash = self._generate_crash_point()
        
        self.current_multiplier = 1.00
        self.history_points = [1.0]
        self.state = "RUNNING"
        self.growth_speed = 0.002
        self.last_delta = 0.0
        
        # Audio
        if self.sm:
            if (self.sm.volume_music == 0.0) or self.sm.muted:
                self.exit_music_volume = 0.0
            self.sm.set_volume_music(0.75, crash=True)
            self.sm.play_music("crash_climb_riser.mp3")

    def cash_out(self):
        if self.state == "RUNNING":
            self.sm.play_sound("cashout")
            
            self.state = "SUCCESS"
            self.cashout_point = self.current_multiplier
            win = self.current_bet * self.cashout_point
            self.wallet.balance += win
            self.last_delta = win
            self.game_history.append((self.cashout_point, True))
            if len(self.game_history) > 12: self.game_history.pop(0)

    def update(self):
        if self.error_timer > 0: self.error_timer -= 1
        else: self.error_msg = ""

        # Stop theme if ended
        if self.state != "RUNNING" and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        if self.state == "RUNNING":
            self.growth_speed *= 1.005
            self.current_multiplier += self.growth_speed
            
            # Graph points
            if self.current_multiplier > self.history_points[-1] + 0.02:
                self.history_points.append(self.current_multiplier)

            # Auto cashout
            if self.auto_cashout_on:
                try:
                    if self.current_multiplier >= float(self.auto_cashout_text):
                        self.cash_out()
                except: pass

            # Crash check
            if self.current_multiplier >= self.target_crash:
                self.current_multiplier = self.target_crash
                self.state = "CRASHED"
                
                self.sm.play_sound("crash_explosion")
                self.last_delta = -self.current_bet
                
                self.game_history.append((self.target_crash, False))
                if len(self.game_history) > 12: self.game_history.pop(0)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect_input_bet.collidepoint(event.pos): self.active_input = "BET"
                elif self.rect_input_auto.collidepoint(event.pos): self.active_input = "AUTO"
                else: self.active_input = None

                if self.rect_btn_half.collidepoint(event.pos):
                    self._apply_bet_multiplier(0.5)
                    if self.sm: self.sm.play_sound("click")
                if self.rect_btn_double.collidepoint(event.pos):
                    self._apply_bet_multiplier(2.0)
                    if self.sm: self.sm.play_sound("click")

                if self.rect_toggle_auto.collidepoint(event.pos):
                    self.auto_cashout_on = not self.auto_cashout_on
                    if self.sm: self.sm.play_sound("click")
                
                if self.rect_btn_action.collidepoint(event.pos):
                    if self.state == "RUNNING": self.cash_out()
                    else: self.start_round()

                # Poprawione sprawdzanie przycisku EXIT
                if self.can_exit() and self.rect_btn_exit.collidepoint(event.pos):
                    self.exit_requested = True

        if event.type == pygame.KEYDOWN:
            # ESCAPE Support
            if event.key == pygame.K_ESCAPE and self.can_exit():
                self.exit_requested = True
                
            if event.key == pygame.K_SPACE:
                if self.state == "RUNNING": self.cash_out()
                else: self.start_round()
            
            # Typing
            target_text = ""
            if self.active_input == "BET": target_text = self.bet_input_text
            elif self.active_input == "AUTO": target_text = self.auto_cashout_text
            
            if self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    target_text = target_text[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    if len(target_text) < 8:
                        target_text += event.unicode
                
                if self.active_input == "BET": self.bet_input_text = target_text
                else: self.auto_cashout_text = target_text

    def draw_graph(self):
        gx, gy = self.rect_graph.x, self.rect_graph.y
        gw, gh = self.rect_graph.width, self.rect_graph.height
        
        max_val = max(2.0, self.current_multiplier * 1.1)
        
        points = []
        if len(self.history_points) < 2: return

        for i, val in enumerate(self.history_points):
            px = gx + (i / len(self.history_points)) * gw
            norm_y = (val - 1.0) / (max_val - 1.0)
            py = (gy + gh) - (norm_y * gh)
            points.append((px, py))

        # Fill area
        if len(points) > 1:
            s = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            poly = points.copy()
            poly.append((points[-1][0], gy + gh))
            poly.append((points[0][0], gy + gh))
            
            f_col = COLORS["glow_green"] if self.state != "CRASHED" else COLORS["glow_red"]
            pygame.draw.polygon(s, f_col, poly)
            self.screen.blit(s, (0,0))

            # Line
            l_col = COLORS["accent_green"] if self.state != "CRASHED" else COLORS["accent_red"]
            pygame.draw.lines(self.screen, l_col, False, points, 4)

            # Head
            head = points[-1]
            pygame.draw.circle(self.screen, COLORS["text_white"], head, 6)

    def draw_ui(self):
        # Panel bg
        pygame.draw.rect(self.screen, COLORS["bg_panel"], self.rect_panel_bg)
        pygame.draw.line(self.screen, (60, 70, 90), (0, self.rect_panel_bg.y), (self.W, self.rect_panel_bg.y), 1)
        mouse_pos = pygame.mouse.get_pos()

        # Balance
        lbl = self.font_ui.render("BALANCE", True, COLORS["text_gray"])
        val = self.font_mono.render(f"${self._display_balance():.2f}", True, COLORS["text_white"])
        self.screen.blit(lbl, (20, 20))
        self.screen.blit(val, (20, 50))
        if self.last_delta != 0:
            delta_color = COLORS["accent_green"] if self.last_delta > 0 else COLORS["accent_red"]
            sign = "+" if self.last_delta > 0 else "-"
            delta_text = f"{sign}${abs(int(self.last_delta))}"
            delta = self.font_ui.render(delta_text, True, delta_color)
            self.screen.blit(delta, (20, 80))

        # History pills
        hx = 250
        for val, win in reversed(self.game_history[-8:]):
            c = COLORS["accent_green"] if win else COLORS["accent_red"]
            bg = (c[0]//5, c[1]//5, c[2]//5)
            
            txt = self.font_ui.render(f"{val:.2f}x", True, c)
            pr = pygame.Rect(hx, 25, txt.get_width() + 20, 30)
            
            self.draw_rounded_rect(self.screen, bg, pr, 15)
            self.screen.blit(txt, (hx + 10, 27))
            hx += pr.width + 10

        # Input: Bet
        lbl_bet = self.font_ui.render("BET AMOUNT", True, COLORS["text_gray"])
        self.screen.blit(lbl_bet, lbl_bet.get_rect(center=(self.rect_input_bet.centerx, self.rect_input_bet.y - 15)))
        
        col_border = COLORS["accent_green"] if self.active_input == "BET" else COLORS["input_bg"]
        self.draw_rounded_rect(self.screen, COLORS["input_bg"], self.rect_input_bet, 8)
        if self.active_input == "BET":
            pygame.draw.rect(self.screen, col_border, self.rect_input_bet, 2, border_radius=8)
        
        txt_bet = self.font_mono.render(f"{self.bet_input_text}", True, COLORS["text_white"])
        self.screen.blit(txt_bet, txt_bet.get_rect(center=self.rect_input_bet.center))

        # Bet quick buttons
        hover_half = self.rect_btn_half.collidepoint(mouse_pos)
        hover_double = self.rect_btn_double.collidepoint(mouse_pos)
        self._handle_hover("half", hover_half)
        self._handle_hover("double", hover_double)
        self.draw_rounded_rect(self.screen, COLORS["input_bg"], self.rect_btn_half, 6)
        self.draw_rounded_rect(self.screen, COLORS["input_bg"], self.rect_btn_double, 6)
        if hover_half:
            self.draw_inner_glow(self.rect_btn_half, COLORS["accent_green"], alpha=70, radius=6)
        if hover_double:
            self.draw_inner_glow(self.rect_btn_double, COLORS["accent_green"], alpha=70, radius=6)
        pygame.draw.rect(self.screen, COLORS["accent_green"], self.rect_btn_half, 1, border_radius=6)
        pygame.draw.rect(self.screen, COLORS["accent_green"], self.rect_btn_double, 1, border_radius=6)

        small_font = pygame.font.SysFont("Verdana", 12)
        t_half = small_font.render("0.5x", True, COLORS["text_white"])
        t_double = small_font.render("2x", True, COLORS["text_white"])
        self.screen.blit(t_half, t_half.get_rect(center=self.rect_btn_half.center))
        self.screen.blit(t_double, t_double.get_rect(center=self.rect_btn_double.center))

        # Input: Auto
        lbl_auto = self.font_ui.render("AUTO CASHOUT", True, COLORS["text_gray"])
        self.screen.blit(lbl_auto, lbl_auto.get_rect(center=(self.rect_input_auto.centerx, self.rect_input_auto.y - 15)))
        
        col_border = COLORS["accent_green"] if self.active_input == "AUTO" else COLORS["input_bg"]
        self.draw_rounded_rect(self.screen, COLORS["input_bg"], self.rect_input_auto, 8)
        if self.active_input == "AUTO":
            pygame.draw.rect(self.screen, col_border, self.rect_input_auto, 2, border_radius=8)
            
        txt_auto = self.font_mono.render(f"{self.auto_cashout_text} x", True, COLORS["text_white"])
        self.screen.blit(txt_auto, txt_auto.get_rect(center=self.rect_input_auto.center))

        # Toggle switch
        hover_toggle = self.rect_toggle_auto.collidepoint(mouse_pos)
        self._handle_hover("toggle", hover_toggle)
        t_col = COLORS["accent_green"] if self.auto_cashout_on else COLORS["bg_dark"]
        self.draw_rounded_rect(self.screen, t_col, self.rect_toggle_auto, 20)
        if hover_toggle:
            self.draw_inner_glow(self.rect_toggle_auto, COLORS["accent_green"], alpha=70, radius=20)
        knob_radius = 14
        if self.auto_cashout_on:
            kx = self.rect_toggle_auto.right - knob_radius - 6
        else:
            kx = self.rect_toggle_auto.x + knob_radius + 6
        cx, cy = kx, self.rect_toggle_auto.centery
        scale = 5
        size = knob_radius * 2 * scale
        knob = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(knob, size // 2, size // 2, knob_radius * scale, COLORS["text_white"])
        pygame.gfxdraw.aacircle(knob, size // 2, size // 2, knob_radius * scale, COLORS["text_white"])
        knob = pygame.transform.smoothscale(knob, (knob_radius * 2, knob_radius * 2))
        self.screen.blit(knob, (cx - knob_radius, cy - knob_radius))

        # Action Button
        b_col = COLORS["accent_green"]
        b_txt = "BET"
        
        if self.state == "RUNNING":
            b_col = COLORS["accent_yellow"]
            b_txt = "CASH OUT"
        elif self.state == "BETTING":
             b_col = COLORS["accent_green"]
             b_txt = "PLACE BET"
        else:
             b_col = COLORS["accent_green"]
             b_txt = "NEXT ROUND"

        hover_action = self.rect_btn_action.collidepoint(mouse_pos)
        self._handle_hover("action", hover_action)
        s_rect = self.rect_btn_action.copy()
        s_rect.y += 4
        self.draw_rounded_rect(self.screen, (20,20,20), s_rect, 15)
        self.draw_rounded_rect(self.screen, b_col, self.rect_btn_action, 15)
        if hover_action:
            self.draw_inner_glow(self.rect_btn_action, COLORS["text_white"], alpha=60, radius=15)
        
        t_btn = self.font_ui.render(b_txt, True, COLORS["bg_dark"])
        tr = t_btn.get_rect(center=self.rect_btn_action.center)
        self.screen.blit(t_btn, tr)
        


        # Center Text
        m_col = COLORS["text_white"]
        if self.state == "CRASHED": m_col = COLORS["accent_red"]
        if self.state == "SUCCESS": m_col = COLORS["accent_green"]
        
        d_val = f"{self.current_multiplier:.2f}x"
        if self.state == "CRASHED": d_val = f"CRASHED @ {self.target_crash:.2f}x"
        t_main = self.font_main.render(d_val, True, m_col)
        r_main = t_main.get_rect(center=(self.W // 2, self.H // 2 - 50))
        self.screen.blit(t_main, r_main)
        
        # Errors
        if self.error_msg:
            et = self.font_ui.render(f"⚠ {self.error_msg}", True, COLORS["accent_red"])
            er = et.get_rect(center=(self.W // 2, self.panel_y - 30))
            self.screen.blit(et, er)

        # Exit Button 
        if self.can_exit():
            hover_exit = self.rect_btn_exit.collidepoint(mouse_pos)
            exit_col = COLORS["accent_red"] if hover_exit else COLORS["bg_panel"]
            self.draw_rounded_rect(self.screen, exit_col, self.rect_btn_exit, 8)
            if hover_exit:
                self.draw_inner_glow(self.rect_btn_exit, COLORS["accent_red"], alpha=70, radius=8)
            t_exit = self.font_ui.render("EXIT", True, COLORS["text_white"])
            tr_exit = t_exit.get_rect(center=self.rect_btn_exit.center)
            self.screen.blit(t_exit, tr_exit)

    def draw(self):
        self.draw_gradient_bg()
        self.draw_graph()
        self.draw_ui()
