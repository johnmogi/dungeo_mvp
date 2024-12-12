import pygame
import math
from .base_screen import BaseScreen
from .combat_screen import CombatScreen

class CombatTransition(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.font = pygame.font.Font(None, 74)
        self.timer = 0
        self.transition_time = 2000  # 2 seconds
        self.start_time = pygame.time.get_ticks()
        
        # Load character portraits if available
        try:
            char_type = self.game_state.selected_character.get('type', 'warrior').lower()
            self.player_portrait = pygame.image.load(f'assets/{char_type}.png')
            self.player_portrait = pygame.transform.scale(self.player_portrait, (200, 200))
        except:
            self.player_portrait = None
            
        try:
            self.enemy_portrait = pygame.image.load('assets/monster.png')
            self.enemy_portrait = pygame.transform.scale(self.enemy_portrait, (200, 200))
        except:
            self.enemy_portrait = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks()
        progress = (current_time - self.start_time) / self.transition_time
        
        # Draw VS text in the center
        vs_text = self.font.render("VS", True, (255, 0, 0))
        vs_rect = vs_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        # Calculate positions with animation
        left_x = -200 + (self.screen.get_width() // 4 + 200) * min(1, progress * 2)
        right_x = self.screen.get_width() + 200 - (self.screen.get_width() // 4 + 200) * min(1, progress * 2)
        
        # Draw player portrait/icon on the left
        if self.player_portrait:
            player_rect = self.player_portrait.get_rect(center=(left_x, self.screen.get_height() // 2))
            self.screen.blit(self.player_portrait, player_rect)
        else:
            player_text = self.font.render(self.game_state.player_emoji, True, (255, 255, 255))
            player_rect = player_text.get_rect(center=(left_x, self.screen.get_height() // 2))
            self.screen.blit(player_text, player_rect)
        
        # Draw enemy portrait/icon on the right
        if self.enemy_portrait:
            enemy_rect = self.enemy_portrait.get_rect(center=(right_x, self.screen.get_height() // 2))
            self.screen.blit(self.enemy_portrait, enemy_rect)
        else:
            enemy_text = self.font.render("👿", True, (255, 255, 255))
            enemy_rect = enemy_text.get_rect(center=(right_x, self.screen.get_height() // 2))
            self.screen.blit(enemy_text, enemy_rect)
        
        # Draw VS text with pulsing effect
        if progress > 0.3:  # Start showing VS after portraits start moving
            vs_scale = 1 + math.sin(progress * 10) * 0.2  # Pulsing effect
            scaled_vs = pygame.transform.scale(vs_text, 
                (int(vs_text.get_width() * vs_scale), 
                 int(vs_text.get_height() * vs_scale)))
            vs_rect = scaled_vs.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(scaled_vs, vs_rect)
        
        # Draw player name and enemy type
        if progress > 0.5:  # Show names after VS appears
            player_name = self.font.render(self.game_state.name, True, (255, 255, 255))
            enemy_name = self.font.render("Enemy", True, (255, 255, 255))
            
            self.screen.blit(player_name, 
                           player_name.get_rect(centerx=left_x, 
                                              centery=self.screen.get_height() // 2 + 150))
            self.screen.blit(enemy_name, 
                           enemy_name.get_rect(centerx=right_x, 
                                             centery=self.screen.get_height() // 2 + 150))

    def handle_event(self, event):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.transition_time:
            return CombatScreen(self.screen, self.game_state)
        return None
