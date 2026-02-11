import pygame
import os
import json

class SoundManager:
    def __init__(self):
        self.sounds = {}
        # Ustalanie ścieżek
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.sfx_path = os.path.join(base_dir, "assets", "sfx")
        self.music_path = os.path.join(base_dir, "assets", "music")
        self.crash_path = os.path.join(base_dir, "assets", "crash")
        
        # Folder DATA i plik ustawień
        self.data_dir = os.path.join(base_dir, "data")
        self.settings_file = os.path.join(self.data_dir, "sound_settings.json")

        # Wartości domyślne (używane, jeśli nie ma pliku)
        self.volume = 0.5           
        self.volume_music = 0.1     
        self.exit_volume_music = 0.1
        self.muted = False          
        self.previous_volume_music = 0.1
        self.last_music_played = "jazz_playlist.mp3"

        # Próba wczytania ustawień z pliku przy starcie
        self.load_settings()

    def _ensure_data_dir(self):
        """Upewnia się, że folder data istnieje."""
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
            except OSError as e:
                print(f"Nie udało się stworzyć folderu data: {e}")

    def save_settings(self):
        """Zapisuje ustawienia do data/settings.json"""
        self._ensure_data_dir()
        
        data = {
            "volume": self.volume,
            "volume_music": self.volume_music,
            "muted": self.muted,
            "previous_volume_music": self.previous_volume_music
        }
        
        try:
            with open(self.settings_file, "w") as f:
                json.dump(data, f, indent=4) # indent sprawia, że plik ładnie wygląda w notatniku
        except Exception as e:
            print(f"Błąd zapisu ustawień: {e}")

    def load_settings(self):
        """Wczytuje ustawienia z data/settings.json"""
        if not os.path.exists(self.settings_file):
            return # Brak pliku -> używamy domyślnych wartości z __init__

        try:
            with open(self.settings_file, "r") as f:
                data = json.load(f)
                
                # Pobieramy wartości, a jeśli ich nie ma, bierzemy obecne (domyślne)
                self.volume = data.get("volume", self.volume)
                self.volume_music = data.get("volume_music", self.volume_music)
                self.muted = data.get("muted", self.muted)
                self.previous_volume_music = data.get("previous_volume_music", self.previous_volume_music)

                # Logika po wczytaniu (np. ustawienie exit volume)
                if self.muted:
                    self.exit_volume_music = 0.0
                else:
                    self.exit_volume_music = self.volume_music
                    
        except Exception as e:
            print(f"Błąd odczytu ustawień (plik może być uszkodzony): {e}")

    def load_common_sounds(self): 
        common_sounds = {
            "click": "select_001.ogg",
            "hover": "hover.wav"
        }
        loaded = 0
        for name, filename in common_sounds.items():
            if self.load_sound(name, filename, self.sfx_path):
                loaded += 1
        print(f"Loaded {loaded}/{len(common_sounds)} common sounds")
        return loaded

    def load_blackjack_sounds(self): 
        blackjack_sounds = {
            "card_place1": "card_place1.ogg",
            "card_place2": "card_place2.ogg",
            "card_place3": "card_place3.ogg",
            "card_place4": "card_place4.ogg",
            "deal1": "deal1.ogg",
            "deal2": "deal2.ogg",
            "deal3": "deal3.ogg",
            "deal4": "deal4.ogg",

            "chip_stack": "chips_stack.ogg",
            "win": "chip_drop.wav",
            "lose": "chip_drop.wav"
        }
        loaded = 0
        for name, filename in blackjack_sounds.items():
            if self.load_sound(name, filename, self.sfx_path):
                loaded += 1
        print(f"Loaded {loaded}/{len(blackjack_sounds)} blackjack sounds")
        return loaded
    
    def load_crash_sounds(self): 
        crash_sounds = {
            "cashout": "cashout.mp3",
            "crash_cr": "crash_climb_riser.mp3",
            "crash_explosion": "crash_explosion.mp3",
            "crash_loop_ticking": "crash_loop_ticking.mp3"
        }
        loaded = 0
        for name, filename in crash_sounds.items():
            if self.load_sound(name, filename, self.crash_path):
                loaded += 1
        print(f"Loaded {loaded}/{len(crash_sounds)} crash sounds")
        return loaded
    
    def _ensure_mixer(self):
        if pygame.mixer.get_init():
            return True
        try:
            pygame.mixer.init()
            return True
        except Exception as e:
            return False

    def load_sound(self, name, filename, base_path=None): 
        if not self._ensure_mixer():
            print(f"Nie można załadować dźwięku '{filename}': mixer niedostępny.")
            return False

        if base_path is None:
            base_path = self.sfx_path
        path = os.path.join(base_path, filename)
        if not os.path.exists(path):
            print(f"Brak pliku dźwięku: {path}")
            return False
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
            return True
        except Exception as e:
            print(f"Blad przy wczytywaniu dźwięku {filename}: {e}")
            return False

    def play_sound(self, name): 
        if not self._ensure_mixer():
            print(f"Cannot play sound '{name}': mixer not initialized.")
            return

        if name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception as e:
                print(f"Blad przy odtwarzaniu dźwięku {name}: {e}")
        else:
            print(f"Dźwięk {name} nie został załadowany.")

    def play_music(self, name=None): 
        if name is None:
            name = self.last_music_played

        if not self._ensure_mixer():
            print(f"Cannot play music '{name}': mixer not initialized.")
            return False

        path = os.path.join(self.music_path, name)
        if not os.path.exists(path):
            path = os.path.join(self.crash_path, name)
        if not os.path.exists(path):
            print(f"Plik muzyki '{name}' nie istnieje w {self.music_path} ani {self.crash_path}.")
            return False
        try:
            pygame.mixer.music.load(path)
            
            # Ustawiamy głośność zgodnie z wczytanymi ustawieniami
            target_vol = 0.0 if self.muted else self.volume_music
            pygame.mixer.music.set_volume(target_vol)
            
            if name != "crash_climb_riser.mp3":
                self.last_music_played = name
            pygame.mixer.music.play(-1)
            return True
        except Exception as e:
            print(f"Blad przy odtwarzaniu muzyki {name}: {e}")
            return False
    
    def set_volume(self, value): 
        self.volume = max(0.0, min(1.0, value))
        self._apply_sound_volume()
        self.save_settings() # ZAPIS PRZY ZMIANIE

    def set_volume_music(self, value, crash=False): 
        self.volume_music = max(0.0, min(1.0, value))

        if not crash:
            self.exit_volume_music = self.volume_music
        else:
            if self.muted:
                self.exit_volume_music = 0.0
        
        # Jeśli ruszasz suwakiem - zdjęcie wyciszenia 
        if self.muted and self.volume_music > 0 and not crash:
            self.muted = False
            
        if self._ensure_mixer():
            target_vol = 0.0 if self.muted else self.volume_music
            pygame.mixer.music.set_volume(target_vol)
        else:
            print("Warning: mixer not initialized; cannot set music volume")
            
        if not crash:
            self.save_settings() # ZAPIS PRZY ZMIANIE

    def toggle_mute(self):  
        self.muted = not self.muted
        if self.muted:
            self.previous_volume_music = self.volume_music
            if self._ensure_mixer():
                pygame.mixer.music.set_volume(0.0)
        else:
            self.volume_music = self.previous_volume_music if self.previous_volume_music > 0 else 0.1
            if self._ensure_mixer():
                pygame.mixer.music.set_volume(self.volume_music)
        
        self.save_settings() # ZAPIS PRZY ZMIANIE

    def _apply_sound_volume(self):  
        for sound in self.sounds.values():
            sound.set_volume(self.volume)