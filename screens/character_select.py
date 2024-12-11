import pygame
import random
from .base_screen import BaseScreen
from .screen_manager import ScreenManager

class CharacterSelect(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.characters = {
            'Warrior': {'hp': 120, 'attack': 15, 'defense': 20},
            'Archer': {'hp': 100, 'attack': 20, 'defense': 15},
            'Mage': {'hp': 80, 'attack': 25, 'defense': 10}
        }
        self.selected = 0  # 0-2: characters, 3: gender, 4: name, 5: randomize, 6: start
        self.char_list = list(self.characters.keys())
        self.gender = 'Male'
        self.name = 'Hero'
        self.name_active = False
        self.max_name_length = 12

    def draw(self):
        self.screen.fill((20, 20, 30))
        
        # Draw title
        self.draw_text("Create Your Character", (200, 200, 255), 
                      (self.screen.get_width()//2, 80))
        
        # Draw character options with more spacing
        for i, char in enumerate(self.char_list):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            self.draw_text(f"{char} 👤", color, 
                          (self.screen.get_width()//2, 150 + i * 60))  # Increased spacing
        
        # Draw gender selection with adjusted position
        gender_color = (255, 255, 0) if self.selected == 3 else (255, 255, 255)
        gender_text = f"Gender: {self.gender} {'👨' if self.gender == 'Male' else '👩'}"
        self.draw_text(gender_text, gender_color,
                      (self.screen.get_width()//2, 350))  # Moved down
        
        # Draw name input with adjusted position
        name_color = (255, 255, 0) if self.selected == 4 else (255, 255, 255)
        cursor = '|' if self.name_active and pygame.time.get_ticks() % 1000 < 500 else ''
        self.draw_text(f"Name: {self.name}{cursor}", name_color,
                      (self.screen.get_width()//2, 410))  # Moved down
        
        # Draw randomize button with adjusted position
        random_color = (255, 255, 0) if self.selected == 5 else (255, 255, 255)
        self.draw_text("🎲 Generate Random Character 🎲", random_color,
                      (self.screen.get_width()//2, 470))  # Moved down

        # Draw start button with adjusted position
        if self.game_state.selected_character:
            start_color = (255, 255, 0) if self.selected == 6 else (255, 255, 255)
            self.draw_text("⚔️ Start Game ⚔️", start_color,
                          (self.screen.get_width()//2, 530))  # Moved down
            
        # Draw stats if a character is selected
        if self.selected < len(self.char_list):
            stats = self.characters[self.char_list[self.selected]]
            stat_text = [
                f"HP: {stats['hp']} ❤️",
                f"Attack: {stats['attack']} ⚔️",
                f"Defense: {stats['defense']} 🛡️"
            ]
            for j, text in enumerate(stat_text):
                self.draw_text(text, (150, 150, 150),
                              (self.screen.get_width()//2, 580 + j * 30))
        
        # Draw controls
        controls = []
        if self.selected == 4 and self.name_active:
            controls.append("Type to edit name")
            controls.append("Press ENTER to confirm")
        else:
            controls.append("↑↓ to navigate")
            controls.append("ENTER/SPACE to select")
        
        for i, text in enumerate(controls):
            self.draw_text(text, (150, 150, 150),
                          (self.screen.get_width()//2, 680 + i * 30))

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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.selected == 4 and self.name_active:
                if event.key == pygame.K_RETURN:
                    self.name_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.unicode.isprintable() and len(self.name) < self.max_name_length:
                    self.name += event.unicode
            else:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % 7
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % 7
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if self.selected < len(self.char_list):
                        char = self.char_list[self.selected]
                        stats = self.characters[char]
                        
                        # Set character stats in game state
                        self.game_state.selected_character = char
                        self.game_state.character_name = self.name
                        self.game_state.character_gender = self.gender
                        self.game_state.hp = stats['hp']
                        self.game_state.max_hp = stats['hp']
                        self.game_state.attack = stats['attack']
                        self.game_state.defense = stats['defense']
                        
                    elif self.selected == 3:  # Gender toggle
                        self.gender = 'Female' if self.gender == 'Male' else 'Male'
                    elif self.selected == 4:  # Name edit
                        self.name_active = True
                    elif self.selected == 5:  # Randomize
                        self.randomize_character()
                    elif self.selected == 6 and self.game_state.selected_character:  # Start game
                        return ScreenManager.get_screen('game_board', self.screen, self.game_state)
        return None