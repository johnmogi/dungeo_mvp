import pygame
import os
from screens.character_select import CharacterSelectScreen

class WelcomeScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Load background image
        self.background = pygame.image.load(os.path.join("assets", "dungeo.jpg"))
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        
        # Button dimensions and positions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 200
        button_height = 40
        
        # Center positions
        center_x = screen_width // 2 - button_width // 2
        
        # Create buttons
        self.start_button = pygame.Rect(center_x, 200, button_width, button_height)
        self.sound_button = pygame.Rect(center_x, 300, button_width, button_height)
        self.controls_button = pygame.Rect(center_x, 350, button_width, button_height)
        self.cheat_button = pygame.Rect(center_x, 400, button_width, button_height)
        self.exit_button = pygame.Rect(center_x, 450, button_width, button_height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.start_button.collidepoint(mouse_pos):
                return CharacterSelectScreen(self.screen, self.game_state)
            elif self.sound_button.collidepoint(mouse_pos):
                self.game_state.toggle_sound()
            elif self.cheat_button.collidepoint(mouse_pos):
                self.game_state.toggle_cheat_mode()
            elif self.exit_button.collidepoint(mouse_pos):
                pygame.quit()
                exit()
        
        return None

    def update(self):
        pass

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title box
        title_surface = pygame.Surface((self.screen.get_width(), 100))
        title_surface.fill(self.BLACK)
        title_surface.set_alpha(200)  # Semi-transparent
        self.screen.blit(title_surface, (0, 50))
        
        # Draw title
        title = self.font.render("DUNGEON QUEST", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw buttons with borders
        def draw_button(rect, text, active=False):
            # Draw button background
            pygame.draw.rect(self.screen, self.BLACK, rect)
            pygame.draw.rect(self.screen, self.WHITE, rect, 2)  # Border
            
            # Draw text
            text_surface = self.font.render(text, True, self.WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Draw all buttons
        draw_button(self.start_button, "START")
        
        # Draw options section
        options_text = self.font.render("OPTIONS", True, self.WHITE)
        options_rect = options_text.get_rect(center=(self.screen.get_width() // 2, 270))
        self.screen.blit(options_text, options_rect)
        
        # Draw sound toggle
        sound_text = f"Sound: {'[ON]' if self.game_state.sound_enabled else 'ON'} {'OFF' if self.game_state.sound_enabled else '[OFF]'}"
        draw_button(self.sound_button, sound_text)
        
        # Draw controls
        draw_button(self.controls_button, "Controls")
        
        # Draw cheat mode toggle
        cheat_text = f"Cheat Mode: {'[ON]' if self.game_state.cheat_mode else 'ON'} {'OFF' if self.game_state.cheat_mode else '[OFF]'}"
        draw_button(self.cheat_button, cheat_text)
        
        # Draw exit button
        draw_button(self.exit_button, "EXIT")
