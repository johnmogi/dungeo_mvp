import pygame
import sys
from screens.loading_screen import LoadingScreen
from game_state import GameState

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dungeon Quest")
        
        # Initialize game state
        self.game_state = GameState()
        
        # Initialize with loading screen
        self.current_screen = LoadingScreen(self.screen, self.game_state)
        
        # Set up game clock
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle events for current screen
                next_screen = self.current_screen.handle_event(event)
                if next_screen:
                    self.current_screen = next_screen

            # Update current screen
            next_screen = self.current_screen.update()
            if next_screen:
                self.current_screen = next_screen
            
            # Draw current screen
            self.current_screen.draw()
            
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
