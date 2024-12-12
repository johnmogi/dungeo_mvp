import pygame
import os
from .base_screen import BaseScreen
from .screen_manager import ScreenManager

class WelcomeScreen(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.font = pygame.font.Font(None, 74)
        self.title_text = "Dungeon Quest"
        self.start_text = "Press ENTER to Start"
        
        # Load splash image
        splash_path = os.path.join('assets', 'splash.jpg')
        try:
            self.bg_image = pygame.image.load(splash_path)
            # Scale the image to fit the screen while maintaining aspect ratio
            img_ratio = self.bg_image.get_width() / self.bg_image.get_height()
            screen_ratio = self.screen.get_width() / self.screen.get_height()
            
            if screen_ratio > img_ratio:
                # Screen is wider than image
                new_height = self.screen.get_height()
                new_width = int(new_height * img_ratio)
            else:
                # Screen is taller than image
                new_width = self.screen.get_width()
                new_height = int(new_width / img_ratio)
            
            self.bg_image = pygame.transform.scale(self.bg_image, (new_width, new_height))
            # Calculate position to center the image
            self.bg_x = (self.screen.get_width() - new_width) // 2
            self.bg_y = (self.screen.get_height() - new_height) // 2
        except Exception as e:
            print(f"Could not load splash image: {splash_path}")
            print(f"Error: {e}")
            self.bg_image = None
            self.bg_x = 0
            self.bg_y = 0

    def draw(self):
        # Fill screen with dark color
        self.screen.fill((20, 20, 30))
        
        # Draw background image if available
        if self.bg_image:
            self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))
        
        # Create semi-transparent overlay for better text visibility
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)  # 50% transparency
        self.screen.blit(overlay, (0, 0))
        
        # Draw title with shadow
        title_shadow = self.font.render(self.title_text, True, (0, 0, 0))
        title_surface = self.font.render(self.title_text, True, (255, 215, 0))  # Gold color
        
        # Center the text
        title_x = self.screen.get_width() // 2
        title_y = self.screen.get_height() // 3
        
        # Draw shadow slightly offset
        shadow_rect = title_shadow.get_rect(center=(title_x + 2, title_y + 2))
        self.screen.blit(title_shadow, shadow_rect)
        
        # Draw main text
        title_rect = title_surface.get_rect(center=(title_x, title_y))
        self.screen.blit(title_surface, title_rect)
        
        # Draw "Press ENTER" text with pulsing effect
        alpha = int(abs(pygame.time.get_ticks() / 1000 % 2 - 1) * 255)
        start_surface = self.font.render(self.start_text, True, (255, 255, 255))
        start_surface.set_alpha(alpha)
        start_rect = start_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() * 2 // 3))
        self.screen.blit(start_surface, start_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return ScreenManager.get_screen('character_select', self.screen, self.game_state)
        return None