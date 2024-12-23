# screens/game_over_screen.py
import pygame
from .base_screen import BaseScreen
from .screen_manager import ScreenManager

class GameOverScreen(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        
    def draw(self):
        self.screen.fill((20, 20, 30))
        
        # Draw game over message
        self.draw_text("Game Over!", (255, 0, 0), 
                      (self.screen.get_width() // 2, 100))
        
        # Draw stats
        stats = [
            f"Character: {self.game_state.selected_character}",
            f"Final HP: {self.game_state.hp}/{self.game_state.max_hp}",
            f"Rooms Cleared: {self.game_state.rooms_cleared}/9",
            f"Monsters Defeated: {self.game_state.monsters_defeated}",
            f"Items Collected: {self.game_state.items_collected}"
        ]
        
        for i, stat in enumerate(stats):
            self.draw_text(stat, (255, 255, 255),
                          (self.screen.get_width() // 2, 200 + i * 40))
        
        # Draw restart prompt
        self.draw_text("Press ENTER or SPACE to return to menu", (150, 150, 150),
                      (self.screen.get_width() // 2, 500))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.game_state.reset()  # Reset game state
                return ScreenManager.get_screen('welcome', self.screen, self.game_state)
        return None