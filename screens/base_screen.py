# screens/base_screen.py
import pygame

class BaseScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        try:
            self.font = pygame.font.SysFont('segoe ui emoji', 36)  # Windows emoji font
        except:
            self.font = pygame.font.Font(None, 36)  # Fallback

    def update(self):
        return None
        
    def draw(self):
        pass
        
    def handle_event(self, event):
        return None

    def draw_text(self, text, color, center_pos):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        self.screen.blit(text_surface, text_rect)