import pygame
import sys
from .base_screen import BaseScreen
from .character_select import CharacterSelect

class WelcomeScreen(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.menu_items = ['Start', 'Options', 'Exit']
        self.selected = 0
        self.options_visible = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_pos = (self.screen.get_width() // 2, 100)
        self.draw_text("DUNGEON QUEST", (255, 255, 255), title_pos)
        
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            pos = (self.screen.get_width() // 2, 250 + i * 50)
            self.draw_text(item, color, pos)
        
        if self.options_visible:
            sound_text = f"Sound: {'ON' if self.game_state.sound_enabled else 'OFF'}"
            cheat_text = f"Cheat Mode: {'ON' if self.game_state.cheat_mode else 'OFF'}"
            self.draw_text(sound_text, (255, 255, 255), 
                          (self.screen.get_width() // 2, 400))
            self.draw_text(cheat_text, (255, 255, 255), 
                          (self.screen.get_width() // 2, 450))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.menu_items[self.selected] == 'Start':
                    return CharacterSelect(self.screen, self.game_state)
                elif self.menu_items[self.selected] == 'Options':
                    self.options_visible = not self.options_visible
                elif self.menu_items[self.selected] == 'Exit':
                    pygame.quit()
                    sys.exit()
            
            if self.options_visible:
                if event.key == pygame.K_s:
                    self.game_state.toggle_sound()
                elif event.key == pygame.K_c:
                    self.game_state.toggle_cheat_mode()
        return None