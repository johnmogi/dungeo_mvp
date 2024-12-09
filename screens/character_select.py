import pygame
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
        self.selected = 0
        self.char_list = list(self.characters.keys())
        
    def draw(self):
        self.screen.fill((20, 20, 30))
        
        # Draw title
        self.draw_text("Select Your Character", (200, 200, 255), 
                      (self.screen.get_width()//2, 100))
        
        # Draw character options
        for i, char in enumerate(self.char_list):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            self.draw_text(char, color, 
                          (self.screen.get_width()//2, 200 + i * 50))
            
            # Draw stats if selected
            if i == self.selected:
                stats = self.characters[char]
                stat_text = [
                    f"HP: {stats['hp']}",
                    f"Attack: {stats['attack']}",
                    f"Defense: {stats['defense']}"
                ]
                for j, text in enumerate(stat_text):
                    self.draw_text(text, (150, 150, 150),
                                  (self.screen.get_width()//2, 350 + j * 30))
        
        # Draw controls
        self.draw_text("Press ENTER or SPACE to select", (150, 150, 150),
                      (self.screen.get_width()//2, 500))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.char_list)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.char_list)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                char = self.char_list[self.selected]
                stats = self.characters[char]
                
                # Set character stats in game state
                self.game_state.selected_character = char
                self.game_state.hp = stats['hp']
                self.game_state.max_hp = stats['hp']
                self.game_state.attack = stats['attack']
                self.game_state.defense = stats['defense']
                
                return ScreenManager.get_screen('game_board', self.screen, self.game_state)
        return None