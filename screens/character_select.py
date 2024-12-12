import pygame
import random
from .base_screen import BaseScreen
from .screen_manager import ScreenManager
import os

class CharacterSelect(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        # Try different fonts
        fonts = ['segoe ui emoji', 'segoe ui symbol', 'arial']
        for font_name in fonts:
            try:
                self.font = pygame.font.SysFont(font_name, 24)
                test_surface = self.font.render('⚔️', True, (255, 255, 255))
                if test_surface.get_width() > 5:
                    break
            except:
                continue
        if not self.font:
            self.font = pygame.font.Font(None, 24)
        
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)  # Smaller font for stats
        
        # Load character portraits
        self.portraits = {}
        for char in ['warrior', 'archer', 'mage']:
            try:
                path = os.path.join('assets', f'{char}.png')
                img = pygame.image.load(path)
                self.portraits[char] = pygame.transform.scale(img, (100, 100))
            except:
                self.portraits[char] = None
        
        self.characters = {
            'Warrior': {
                'hp': 120,
                'attack': 15,
                'defense': 20,
                'icon': '⚔️',
                'desc': 'Tank specialist with high defense',
                'abilities': {
                    'shield_bash': {'uses': 3, 'icon': '🛡️', 'damage': 15, 'desc': 'Shield Bash'},
                    'battle_cry': {'uses': 2, 'icon': '⚔️', 'damage': 10, 'desc': 'Battle Cry'},
                    'defensive_stance': {'uses': 1, 'icon': '🛡️', 'defense': 30, 'desc': 'Defensive Stance'}
                }
            },
            'Archer': {
                'hp': 100,
                'attack': 20,
                'defense': 15,
                'icon': '🏹',
                'desc': 'Ranged expert with high damage',
                'abilities': {
                    'poison_arrow': {'uses': 3, 'icon': '🏹', 'damage': 20, 'desc': 'Poison Arrow'},
                    'ice_arrow': {'uses': 2, 'icon': '❄️', 'damage': 15, 'desc': 'Ice Arrow'},
                    'triple_shot': {'uses': 1, 'icon': '🏹', 'damage': 25, 'desc': 'Triple Shot'}
                }
            },
            'Mage': {
                'hp': 80,
                'attack': 25,
                'defense': 10,
                'icon': '✨',
                'desc': 'Spell master with powerful abilities',
                'abilities': {
                    'fireball': {'uses': 3, 'icon': '🔥', 'damage': 25, 'desc': 'Fireball'},
                    'ice_blast': {'uses': 2, 'icon': '❄️', 'damage': 20, 'desc': 'Ice Blast'},
                    'healing': {'uses': 1, 'icon': '✨', 'heal': 35, 'desc': 'Healing Word'}
                }
            }
        }
        self.char_list = list(self.characters.keys())
        self.selected = 0  # 0-2: characters, 3: gender, 4: name, 5: random, 6: start
        self.name = ""
        self.name_active = False
        self.gender = "Male"
        self.max_name_length = 12
        self.menu_state = 'character'  # 'character' or 'menu'

    def draw_text(self, text, color, pos):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title_surface = self.title_font.render("Choose Your Character", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width()//2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Draw character boxes in a row
        box_width = 200
        box_height = 280  # Make boxes taller
        spacing = 50
        start_x = (self.screen.get_width() - (box_width * 3 + spacing * 2)) // 2
        start_y = 100
        
        for i, char in enumerate(self.char_list):
            char_data = self.characters[char]
            x = start_x + i * (box_width + spacing)
            y = start_y
            
            # Draw box
            box_color = (255, 255, 0) if (self.menu_state == 'character' and i == self.selected) else (100, 100, 100)
            pygame.draw.rect(self.screen, box_color, (x, y, box_width, box_height), 2)
            
            # Draw character name and icon
            name_surface = self.font.render(f"{char} {char_data['icon']}", True, 
                                          (255, 255, 0) if (self.menu_state == 'character' and i == self.selected) else (255, 255, 255))
            name_rect = name_surface.get_rect(center=(x + box_width//2, y + 30))
            self.screen.blit(name_surface, name_rect)
            
            # Draw portrait or placeholder
            portrait = self.portraits.get(char.lower())
            if portrait:
                portrait_rect = portrait.get_rect(center=(x + box_width//2, y + 100))
                self.screen.blit(portrait, portrait_rect)
            else:
                # Draw placeholder circle
                pygame.draw.circle(self.screen, box_color, (x + box_width//2, y + 100), 40, 2)
                placeholder_text = self.font.render(char_data['icon'], True, box_color)
                placeholder_rect = placeholder_text.get_rect(center=(x + box_width//2, y + 100))
                self.screen.blit(placeholder_text, placeholder_rect)
            
            # Draw description
            desc_surface = self.small_font.render(char_data['desc'], True, (200, 200, 200))
            desc_rect = desc_surface.get_rect(center=(x + box_width//2, y + 160))
            self.screen.blit(desc_surface, desc_rect)
            
            # Draw stats with smaller font
            stats = [
                f"HP: {char_data['hp']} ❤️",
                f"ATK: {char_data['attack']} ⚔️",
                f"DEF: {char_data['defense']} 🛡️"
            ]
            for j, stat in enumerate(stats):
                stat_surface = self.small_font.render(stat, True, (150, 150, 150))
                stat_rect = stat_surface.get_rect(center=(x + box_width//2, y + 190 + j * 20))
                self.screen.blit(stat_surface, stat_rect)
            
            # Draw abilities
            ability_y = y + 250
            for ability in char_data['abilities'].values():
                ability_text = f"{ability['icon']} {ability['desc']}"
                ability_surface = self.small_font.render(ability_text, True, (150, 150, 150))
                ability_rect = ability_surface.get_rect(center=(x + box_width//2, ability_y))
                self.screen.blit(ability_surface, ability_rect)
                ability_y += 20
        
        menu_y = box_height + start_y + 50
        menu_spacing = 40
        menu_items = [
            (f"Gender: {self.gender} {'👨' if self.gender == 'Male' else '👩'}", 3),
            (f"Name: {self.name}{'_' if self.name_active else ''}", 4),
            ("🎲 Generate Random", 5)
        ]
        
        # Always show Start button if a character is selected
        if self.game_state.selected_character:
            menu_items.append(("⚔️ Start Adventure", 6))
        
        for i, (text, idx) in enumerate(menu_items):
            color = (255, 255, 0) if (self.menu_state == 'menu' and idx == self.selected) else (255, 255, 255)
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, menu_y + i * menu_spacing))
            self.screen.blit(text_surface, text_rect)
        
        # Draw controls at the bottom
        controls = [
            "← → to select character" if self.menu_state == 'character' else "↑ ↓ to select option",
            "TAB to switch between character/menu",
            "ENTER to confirm"
        ]
        for i, text in enumerate(controls):
            text_surface = self.font.render(text, True, (100, 100, 100))
            text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, self.screen.get_height() - 60 + i * 20))
            self.screen.blit(text_surface, text_rect)

    def randomize_character(self):
        # Select random character and update game state
        self.selected = random.randint(0, len(self.char_list) - 1)
        char = self.char_list[self.selected]
        stats = self.characters[char]
        self.gender = random.choice(['Male', 'Female'])
        
        prefixes = {
            'Male': ['Sir', 'Lord', 'King', 'Prince', 'Duke'],
            'Female': ['Lady', 'Queen', 'Princess', 'Duchess']
        }
        suffixes = ['Brave', 'Bold', 'Swift', 'Wise', 'Strong', 'Mighty']
        
        prefix = random.choice(prefixes[self.gender])
        suffix = random.choice(suffixes)
        self.name = f"{prefix} {suffix}"

        # Set character stats in game state
        self.game_state.selected_character = char
        self.game_state.character_name = self.name
        self.game_state.character_gender = self.gender
        self.game_state.hp = stats['hp']
        self.game_state.max_hp = stats['hp']
        self.game_state.attack = stats['attack']
        self.game_state.defense = stats['defense']

    def _set_character_stats(self, char_name):
        char_stats = self.characters[char_name]
        self.game_state.selected_character = char_name
        self.game_state.hp = char_stats['hp']
        self.game_state.max_hp = char_stats['hp']
        self.game_state.attack = char_stats['attack']
        self.game_state.defense = char_stats['defense']
        self.game_state.abilities = char_stats['abilities'].copy()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.name_active:
                if event.key == pygame.K_RETURN:
                    self.name_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.unicode.isprintable() and len(self.name) < self.max_name_length:
                    self.name += event.unicode
            else:
                if event.key == pygame.K_TAB:
                    self.menu_state = 'menu' if self.menu_state == 'character' else 'character'
                    if self.menu_state == 'character':
                        self.selected = min(self.selected, 2)
                    else:
                        self.selected = 3
                
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if self.menu_state == 'character':
                        # Set character stats
                        char = self.char_list[self.selected]
                        self.game_state.selected_character = self.characters[char].copy()
                        self.menu_state = 'menu'
                        self.selected = 3
                    else:
                        if self.selected == 3:  # Gender
                            self.gender = "Female" if self.gender == "Male" else "Male"
                        elif self.selected == 4:  # Name
                            self.name_active = True
                        elif self.selected == 5:  # Random
                            self.selected = random.randint(0, 2)
                            self.menu_state = 'character'
                            self.gender = random.choice(["Male", "Female"])
                            self.name = f"Hero_{random.randint(1, 999)}"
                        elif self.selected == 6 and self.name:  # Start game
                            if not self.game_state.selected_character:
                                char = self.char_list[0]
                                self.game_state.selected_character = self.characters[char].copy()
                            self.game_state.hp = self.game_state.selected_character['hp']
                            self.game_state.max_hp = self.game_state.selected_character['hp']
                            self.game_state.attack = self.game_state.selected_character['attack']
                            self.game_state.defense = self.game_state.selected_character['defense']
                            self.game_state.name = self.name
                            self.game_state.gender = self.gender
                            self.game_state.player_emoji = '👨' if self.gender == 'Male' else '👩'
                            from screens.game_board import GameBoard
                            return GameBoard(self.screen, self.game_state)
                
                elif self.menu_state == 'character':
                    if event.key == pygame.K_LEFT:
                        self.selected = (self.selected - 1) % 3
                    elif event.key == pygame.K_RIGHT:
                        self.selected = (self.selected + 1) % 3
                else:  # menu state
                    max_menu = 6 if self.name else 5
                    if event.key == pygame.K_UP:
                        self.selected = max(3, (self.selected - 1) if self.selected > 3 else max_menu)
                    elif event.key == pygame.K_DOWN:
                        self.selected = min(max_menu, (self.selected + 1) if self.selected < max_menu else 3)
        
        return None