import pygame
from .base_screen import BaseScreen
from .welcome_screen import WelcomeScreen

class VictoryScreen(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        
    def draw(self):
        self.screen.fill((20, 20, 30))
        
        # Draw victory message
        self.draw_text("Victory!", (255, 215, 0),  # Gold color
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
        
        # Draw achievements if any
        achieved = [name for name, unlocked in self.game_state.achievements.items() 
                   if unlocked]
        if achieved:
            self.draw_text("Achievements:", (255, 215, 0),
                          (self.screen.get_width() // 2, 400))
            for i, achievement in enumerate(achieved):
                self.draw_text(achievement, (200, 200, 200),
                              (self.screen.get_width() // 2, 440 + i * 30))
        
        # Draw restart prompt
        self.draw_text("Press ENTER or SPACE to return to menu", (150, 150, 150),
                      (self.screen.get_width() // 2, 550))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.game_state.reset()  # Reset game state
                return WelcomeScreen(self.screen, self.game_state)
        return None
