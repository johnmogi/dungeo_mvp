# screens/game_over_screen.py
import pygame
from .base_screen import BaseScreen

class GameOverScreen(BaseScreen):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            self.game_state.reset()
            # Import here to avoid circular import
            from .welcome_screen import WelcomeScreen
            return WelcomeScreen(self.screen, self.game_state)
        return None