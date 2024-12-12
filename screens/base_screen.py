# screens/base_screen.py
import pygame

class BaseScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.parent_screen = None
        
        # Try different fonts that support emojis
        fonts = ['segoe ui emoji', 'segoe ui symbol', 'apple color emoji', 'noto color emoji', 'arial']
        self.font = None
        for font_name in fonts:
            try:
                self.font = pygame.font.SysFont(font_name, 24)
                # Test if font can render emojis
                test_surface = self.font.render('⚔️', True, (255, 255, 255))
                if test_surface.get_width() > 5:  # Successfully rendered
                    break
            except:
                continue
        
        if not self.font:
            self.font = pygame.font.Font(None, 24)

    def update(self):
        return None
        
    def draw(self):
        pass
        
    def handle_event(self, event):
        return None

    def draw_text(self, text, color, pos, centered=True):
        try:
            text_surface = self.font.render(text, True, color)
        except:
            # If rendering fails, try without combining characters
            text = ''.join(c for c in text if len(c.encode('utf-16', 'surrogatepass')) <= 2)
            text_surface = self.font.render(text, True, color)
            
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = pos
        else:
            text_rect.topleft = pos
        self.screen.blit(text_surface, text_rect)