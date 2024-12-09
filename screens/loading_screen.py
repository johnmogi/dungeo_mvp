import pygame
import time
from .base_screen import BaseScreen
from .welcome_screen import WelcomeScreen

class LoadingScreen(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.start_time = time.time()
        self.duration = 5
        self.bar_width = 400
        self.bar_height = 20
        self.bar_x = (screen.get_width() - self.bar_width) // 2
        self.bar_y = screen.get_height() - 100

    def update(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.duration:
            return WelcomeScreen(self.screen, self.game_state)
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        progress = min((time.time() - self.start_time) / self.duration, 1)
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (self.bar_x, self.bar_y, self.bar_width, self.bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (self.bar_x, self.bar_y, int(self.bar_width * progress), self.bar_height))
        self.draw_text("Loading...", (255, 255, 255), 
                      (self.screen.get_width() // 2, self.bar_y - 30))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return WelcomeScreen(self.screen, self.game_state)
        return None