import pygame
from .base_screen import BaseScreen
from .game_board import GameBoard

class CharacterSelect(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.characters = ['Warrior', 'Archer', 'Mage']
        self.selected = 0
        self.char_stats = {
            'Warrior': {'hp': 120, 'atk': 15, 'def': 20},
            'Archer': {'hp': 100, 'atk': 20, 'def': 15},
            'Mage': {'hp': 80, 'atk': 25, 'def': 10}
        }

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        title_pos = (self.screen.get_width() // 2, 100)
        self.draw_text("Select Your Character", (255, 255, 255), title_pos)
        
        for i, char in enumerate(self.characters):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            pos = (200 + i * 200, 250)
            self.draw_text(char, color, pos)
            
            if i == self.selected:
                stats = self.char_stats[char]
                stat_y = 300
                for stat, value in stats.items():
                    self.draw_text(f"{stat.upper()}: {value}", (200, 200, 200), 
                                 (self.screen.get_width() // 2, stat_y))
                    stat_y += 30

        self.draw_text("Press ENTER to confirm", (255, 255, 255), 
                      (self.screen.get_width() // 2, 500))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected = (self.selected + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                char = self.characters[self.selected]
                stats = self.char_stats[char]
                self.game_state.selected_character = char
                self.game_state.hp = stats['hp']
                self.game_state.max_hp = stats['hp']
                self.game_state.attack = stats['atk']
                self.game_state.defense = stats['def']
                return GameBoard(self.screen, self.game_state)
        return None