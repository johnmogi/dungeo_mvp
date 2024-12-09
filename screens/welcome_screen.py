import pygame
from .base_screen import BaseScreen
from .screen_manager import ScreenManager

class WelcomeScreen(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.menu_items = ['Start', 'Options', 'Exit']
        self.selected_item = 0
        self.options_visible = False
        self.options = ['Sound: ON', 'Cheat Mode: OFF']
        self.selected_option = 0
        
    def draw(self):
        self.screen.fill((20, 20, 30))
        
        # Draw title
        self.draw_text("Dungeon Quest", (200, 200, 255), 
                      (self.screen.get_width()//2, 100))
        
        if not self.options_visible:
            # Draw menu items
            for i, item in enumerate(self.menu_items):
                color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
                self.draw_text(item, color, 
                             (self.screen.get_width()//2, 250 + i * 50))
        else:
            # Draw options
            self.options[0] = f"Sound: {'ON' if self.game_state.sound_enabled else 'OFF'}"
            self.options[1] = f"Cheat Mode: {'ON' if self.game_state.cheat_mode else 'OFF'}"
            
            for i, option in enumerate(self.options):
                color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
                self.draw_text(option, color, 
                             (self.screen.get_width()//2, 250 + i * 50))
            
            self.draw_text("Press ESC to return", (150, 150, 150),
                          (self.screen.get_width()//2, 400))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.options_visible:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if self.menu_items[self.selected_item] == 'Start':
                        return ScreenManager.get_screen('character_select', self.screen, self.game_state)
                    elif self.menu_items[self.selected_item] == 'Options':
                        self.options_visible = True
                    elif self.menu_items[self.selected_item] == 'Exit':
                        pygame.quit()
                        exit()
            else:
                if event.key == pygame.K_ESCAPE:
                    self.options_visible = False
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if self.selected_option == 0:  # Sound toggle
                        self.game_state.toggle_sound()
                    elif self.selected_option == 1:  # Cheat mode toggle
                        self.game_state.toggle_cheat_mode()
        
        return None