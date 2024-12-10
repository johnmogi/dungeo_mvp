# screens/base_screen.py
import pygame

class BaseScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.parent_screen = None
        try:
            self.font = pygame.font.SysFont('segoeuiemoji', 32)
        except pygame.error:
            try:
                # Fallback to Arial which usually supports basic emojis on Windows
                self.font = pygame.font.SysFont('arial', 32)
            except pygame.error:
                # Last resort - use default font
                self.font = pygame.font.Font(None, 32)

    def update(self):
        return None
        
    def draw(self):
        pass
        
    def handle_event(self, event):
        return None

    def draw_text(self, text, color, pos, centered=True):
        try:
            text_surface = self.font.render(text, True, color)
        except pygame.error:
            # If rendering fails with emojis, try to render without them
            text = ''.join(c for c in text if ord(c) < 0x10000)
            text_surface = self.font.render(text, True, color)
            
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = pos
        else:
            text_rect.topleft = pos
        self.screen.blit(text_surface, text_rect)