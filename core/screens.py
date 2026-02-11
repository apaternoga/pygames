import os
import pygame
from core.settings import WHITE, BLACK, GRAY, SCREEN_HEIGHT, SCREEN_WIDTH
WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT
# --- GŁÓWNE MENU ---
def draw_menu(screen, bg_image, btns, font, logo=None, logo_scale=1.0, wallet_balance=0, pyzeton_img=None, pyzeton_rect=None):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(WHITE)

    if logo:
        target_w = round(logo.get_width() * logo_scale)
        if target_w % 2 != 0: target_w += 1
        aspect_ratio = logo.get_height() / logo.get_width()
        target_h = round(target_w * aspect_ratio)
        if target_h % 2 != 0: target_h += 1

        # skalowanie -smoothscale
        scaled_logo = pygame.transform.smoothscale(logo, (target_w, target_h))
        
        # centrowanie
        logo_rect = scaled_logo.get_rect(center=(1280 // 2, 140))
        screen.blit(scaled_logo, logo_rect)
    
    btns['start'].draw(screen, font)
    btns['exit'].draw(screen, font)
    btns['settings'].draw(screen, font)

    # rysuj PyZeton
    if pyzeton_img and pyzeton_rect:
        screen.blit(pyzeton_img, pyzeton_rect)
        mouse_pos = pygame.mouse.get_pos()
        center = pyzeton_rect.center
        radius = min(pyzeton_rect.width, pyzeton_rect.height) / 2
        if (mouse_pos[0] - center[0]) ** 2 + (mouse_pos[1] - center[1]) ** 2 <= radius ** 2:
            font_small = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 20)
            text = font_small.render("click to reset chips", True, GRAY)
            screen.blit(text, text.get_rect(center=(center[0], center[1]+95)))

# --- USTAWIENIA ---
def draw_settings(screen, bg_image, btns, font, font_large):
    if bg_image: 
        screen.blit(bg_image, (0, 0))
    else: 
        screen.fill(GRAY)

    title_surf = font_large.render("SETTINGS", True, WHITE)
    screen.blit(title_surf, title_surf.get_rect(center=(1280 // 2, 100)))
    
    btns['instr'].draw(screen, font)
    btns['credits'].draw(screen, font)
    btns['music_m'].draw(screen, font)
    btns['back'].draw(screen, font)

# --- EKRAN INSTRUKCJI (SCROLLOWANY) ---
def draw_instructions(screen, bg_image, btns, font, font_smaller, scroll_y):
    # 1. TŁO I NAGŁÓWEK
    if bg_image:
        screen.blit(bg_image, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))
    else:
        screen.fill((30, 30, 35))

    title = font.render("HOW TO PLAY", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

    # 2. TREŚĆ
    full_text = [
        "HEADER:BLACKJACK",
        "Goal: Beat the dealer's score (max 21).",
        "Blackjack (Ace+10) pays 3:2.",
        "Dealer stands on 17. No Dealer Peek.",
        "",
        "HEADER:ACTIONS & CONTROLS",
        "HIT (H): Take another card.",
        "STAND (S): Hold your hand and end turn.",
        "DOUBLE (D): Double wager (1 card only).",
        "SPLIT (P): Split a pair into two hands.",
        "SURRENDER (U): Give up hand (get 50% back).",
        "", 
        "HEADER:CRASH",
        "Multiplier starts at 1.00x and increases.",
        "Goal: Cash out before the crash occurs.",
        "The longer you wait, the more you win.",
        "Risk: Multiplier can crash at any time!",
        "",
        "HEADER:CRASH CONTROLS",
        "SPACE: Place Bet / Cash Out.",
        "ARROWS: Adjust bet amount (if available)."
    ]

    # 3. OBSZAR WIDZENIA
    viewport_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 220)
    screen.set_clip(viewport_rect)

    start_y = viewport_rect.y + 35 - scroll_y 
    gap = 45 

    for i, line in enumerate(full_text):
        if line.startswith("HEADER:"):
            clean_line = line.replace("HEADER:", "")
            txt_surf = font_smaller.render(clean_line, True, (255, 200, 50))
        else:
            txt_surf = font_smaller.render(line, True, (230, 230, 230))
        
        rect = txt_surf.get_rect(center=(WIDTH // 2, start_y + i * gap))
        screen.blit(txt_surf, rect)

    screen.set_clip(None)

    # 4. PASEK PRZEWIJANIA
    scrollbar_x = viewport_rect.right + 10
    scrollbar_h = viewport_rect.height
    
    max_scroll = 480
    
    # Tło paska
    pygame.draw.rect(screen, (60, 60, 60), (scrollbar_x, viewport_rect.y, 8, scrollbar_h), border_radius=4)
    
    if max_scroll > 0:
        thumb_height = 60
        progress = scroll_y / max_scroll
        thumb_y = viewport_rect.y + progress * (scrollbar_h - thumb_height)
        
        # Zabezpieczenie wizualne
        if thumb_y > viewport_rect.bottom - thumb_height:
             thumb_y = viewport_rect.bottom - thumb_height
        
        # Kolor suwaka
        pygame.draw.rect(screen, (200, 200, 200), (scrollbar_x, thumb_y, 8, thumb_height), border_radius=4)

    # 5. PRZYCISK POWROTU
    if 'back_instr' in btns:
        btns['back_instr'].draw(screen, font)
    else:
        btns['back'].draw(screen, font)

# --- EKRAN CREDITS (SCROLLOWANY) ---
def draw_credits(screen, bg_image, btns, font, font_smaller, scroll_y):
    # 1. TŁO I NAGŁÓWEK
    if bg_image:
        screen.blit(bg_image, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))
    else:
        screen.fill((30, 30, 35))

    title = font.render("CREDITS", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

    # 2. TREŚĆ (Bez nazwisk autorów)
    full_text = [
        "HEADER:CRASH GAME MATH",
        "Algorithm: Inverse Probability Distribution.",
        "Based on: open-source reference implementation.",
        "", 
        "HEADER:AUDIO RESOURCES",
        "Background Music: Public Domain (CC0).",
        "Crash Riser: Generated via Suno AI.",
        "SFX: Kenney Assets & Pixabay.",
        "UI Sounds: Freesound (CC0 license).",
        "",
        "HEADER:GRAPHICS & TOOLS",
        "Menu Background: Pexels.com.",
        "Logos: Generated via Gemini AI.",
        "Code Assistant: LLM (Gemini/ChatGPT)."
    ]

    # 3. OBSZAR WIDZENIA (VIEWPORT)
    viewport_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 220)
    screen.set_clip(viewport_rect)

    start_y = viewport_rect.y + 35 - scroll_y 
    gap = 45 

    for i, line in enumerate(full_text):
        if line.startswith("HEADER:"):
            clean_line = line.replace("HEADER:", "")
            # Inny kolor dla nagłówków (np. złoty/zółty)
            txt_surf = font_smaller.render(clean_line, True, (255, 200, 50))
        else:
            # Biały/szary dla zwykłego tekstu
            txt_surf = font_smaller.render(line, True, (230, 230, 230))
        
        rect = txt_surf.get_rect(center=(WIDTH // 2, start_y + i * gap))
        screen.blit(txt_surf, rect)

    screen.set_clip(None)

    # 4. PASEK PRZEWIJANIA
    scrollbar_x = viewport_rect.right + 10
    scrollbar_h = viewport_rect.height
    
    # Długość scrolla - ZMNIEJSZONA DO 180
    max_scroll = 180 
    
    # Tło paska
    pygame.draw.rect(screen, (60, 60, 60), (scrollbar_x, viewport_rect.y, 8, scrollbar_h), border_radius=4)
    
    if max_scroll > 0:
        thumb_height = 60
        # Zabezpieczenie przed dzieleniem przez zero
        progress = scroll_y / max_scroll if max_scroll > 0 else 0
        if progress > 1: progress = 1
        
        thumb_y = viewport_rect.y + progress * (scrollbar_h - thumb_height)
        
        if thumb_y > viewport_rect.bottom - thumb_height:
             thumb_y = viewport_rect.bottom - thumb_height
        
        pygame.draw.rect(screen, (200, 200, 200), (scrollbar_x, thumb_y, 8, thumb_height), border_radius=4)

    # 5. PRZYCISK POWROTU
    if 'back_instr' in btns:
        btns['back_instr'].draw(screen, font)
    else:
        btns['back'].draw(screen, font)

# --- USTAWIENIA MUZYKI ---
def draw_settings_music(screen, bg_image, btns, font, font_smaller, volume, vol_slider, is_muted):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(BLACK)
    
    title = font.render("MUSIC", True, WHITE)
    screen.blit(title, title.get_rect(center=(1280 // 2, 80)))
    
    vol_label = f"VOLUME: {int(volume * 100)}%"
    vol_surf = font_smaller.render(vol_label, True, WHITE)

    total_width = vol_surf.get_width() + 20 + 30
    start_x = (1280 - total_width) // 2
    
    screen.blit(vol_surf, (start_x, 143))
    draw_speaker_icon(screen, start_x + vol_surf.get_width() + 20, 150, is_muted)

    vol_slider.draw(screen)
    btns['t1'].draw(screen, font)
    btns['t2'].draw(screen, font)
    btns['stop'].draw(screen, font_smaller)
    btns['back'].draw(screen, font)

# --- WYJŚCIE ---     
def draw_exit(screen, bg_image, btns, font, font_small):
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((147, 112, 219)) 

    rect_w, rect_h = 800, 300
    rect_x = (1280 - rect_w) // 2
    rect_y = (720 - rect_h) // 2
    
    pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_w, rect_h), border_radius=25)
    pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_w, rect_h), 5, border_radius=25) 
    
    text_surf = font_small.render("ARE YOU SURE YOU WANT TO EXIT?", True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(1280 // 2, rect_y + 90))
    screen.blit(text_surf, text_rect)
    
    btns['yes'].draw(screen, font)
    btns['no'].draw(screen, font)

# --- FULLSCREEN ---
def draw_fullscreen(screen, btns, font_smaller, is_fullscreen):
    overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(180); overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, WHITE, (100, 200, 600, 200), border_radius=15)
    pygame.draw.rect(screen, BLACK, (100, 200, 600, 200), 3, border_radius=15)
    mode_text = "PEŁNY EKRAN" if not is_fullscreen else "TRYB OKNA"
    text = font_smaller.render(f"CZY CHCESZ PRZEŁĄCZYĆ NA {mode_text}?", True, BLACK)
    screen.blit(text, text.get_rect(center=(400, 250)))
    btns['yes'].draw(screen, font_smaller)
    btns['no'].draw(screen, font_smaller)

# --- MINIGIERKI ---
def draw_game_placeholder(screen, bg_image, btns, font, logo, logo_scale=1.0, wallet_balance=0):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill((20, 20, 20))
    if logo:
        target_w = round(logo.get_width() * logo_scale)
        if target_w % 2 != 0: target_w += 1
        aspect_ratio = logo.get_height() / logo.get_width()
        target_h = round(target_w * aspect_ratio)
        if target_h % 2 != 0: target_h += 1

        # skalowanie -smoothscale
        scaled_logo = pygame.transform.smoothscale(logo, (target_w, target_h))
        
        # centrowanie
        logo_rect = scaled_logo.get_rect(center=(1280 // 2, 140))
        screen.blit(scaled_logo, logo_rect)
    else:
        title = font.render("MINIGIERKI", True, WHITE)
        screen.blit(title, title.get_rect(center=(1280 // 2, 80)))
    
    text_balance = font.render(f"${wallet_balance:.2f}", True, WHITE)
    screen.blit(text_balance, text_balance.get_rect(topleft=(50, 50)))

    btns['bj'].draw(screen, font)
    btns['cr'].draw(screen, font)
    btns['back'].draw(screen, font)

# --- IKONA GŁOŚNIKA ---
def draw_speaker_icon(screen, x, y, muted):
    try:
        icon_muted = pygame.image.load(os.path.join("assets", "images", "muted.png")).convert_alpha()
        icon_muted = pygame.transform.smoothscale(icon_muted, (58, 58))
    except:
        icon_muted = None
        print("Brak ikony wyciszenia w assets/images/muted.png")

    try:
        icon = pygame.image.load(os.path.join("assets", "images", "notmuted.png")).convert_alpha()
        icon = pygame.transform.smoothscale(icon, (60, 60))
    except:
        icon = None
        print("Brak ikony braku wyciszenia w assets/images/notmuted.png")
    if not icon_muted or not icon:
        pygame.draw.rect(screen, WHITE, (x, y + 5, 10, 10))
        pygame.draw.polygon(screen, WHITE, [
            (x + 10, y + 5), (x + 25, y - 5), 
            (x + 25, y + 25), (x + 10, y + 15)
        ])
        
        if muted:
            pygame.draw.line(screen, (255, 50, 50), (x - 5, y - 5), (x + 30, y + 25), 4)
            pygame.draw.line(screen, (255, 50, 50), (x + 30, y - 5), (x - 5, y + 25), 4)
        else:
            pygame.draw.arc(screen, WHITE, (x + 15, y - 5, 20, 30), -1.5, 1.5, 3)
            pygame.draw.arc(screen, WHITE, (x + 22, y - 10, 25, 40), -1.5, 1.5, 2)

    else:
        if muted:
            screen.blit(icon_muted, (x, y-18))
        else:
            screen.blit(icon, (x, y-20))