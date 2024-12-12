# screens/game_board.py 
import pygame
import random
from .base_screen import BaseScreen

class GameBoard(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.cell_size = 120
        self.grid_size = 3
        self.margin_x = (screen.get_width() - self.cell_size * self.grid_size) // 2
        self.margin_y = 100
        self.revealed = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.revealed[0][0] = True
        self.story_log = []  # Add story log
        
        if not any(any(cell for cell in row) for row in game_state.board):
            self._generate_board()

    def _get_cell_color(self, cell, pos):
        if pos == self.game_state.current_position:
            return self.game_state.player_emoji, (255, 255, 0)
        symbols = {
            'S': ('⭐', (0, 255, 0)),  
            'E': ('👿', (255, 0, 0)),
            'M': ('👾', (200, 50, 50)),
            'I': ('💎', (50, 200, 200)),
            'T': ('💀', (200, 200, 50))
        }
        return symbols.get(cell, ('?', (255, 255, 255)))

    def _generate_board(self):
        # Clear the board
        self.game_state.board = [[None] * self.grid_size for _ in range(self.grid_size)]
        
        # Set start position
        self.game_state.board[0][0] = 'S'
        
        # Place monsters in a way that forces encounters before boss
        # First monster in the first row
        self.game_state.board[0][1] = 'M'
        
        # Second monster in the middle row
        self.game_state.board[1][1] = 'M'
        
        # Third monster guarding the boss
        self.game_state.board[2][1] = 'M'
        
        # Place boss at the end
        self.game_state.board[2][2] = 'E'
        
        # Fill remaining positions with random events
        events = ['I', 'T']  # Items and traps only (no additional monsters)
        empty_positions = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)
                         if self.game_state.board[i][j] is None]
        
        for pos in empty_positions:
            self.game_state.board[pos[0]][pos[1]] = random.choice(events)
            
        # Update story log
        self.story_log.append("You enter the dungeon. Defeat 3 monsters to reach the boss!")

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = self.margin_x + j * self.cell_size
                y = self.margin_y + i * self.cell_size
                
                cell_color = (40, 40, 50)
                if self.revealed[i][j]:
                    cell_color = (60, 60, 70)
                pygame.draw.rect(self.screen, cell_color, 
                               (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (80, 80, 90), 
                               (x, y, self.cell_size, self.cell_size), 2)

                # Always show player at current position
                if (i, j) == self.game_state.current_position:
                    text = self.game_state.player_emoji
                    color = (255, 255, 0)
                    text_surface = self.font.render(text, True, color)
                    text_rect = text_surface.get_rect(center=(
                        x + self.cell_size//2,
                        y + self.cell_size//2
                    ))
                    self.screen.blit(text_surface, text_rect)
                # Show other cell contents if revealed
                elif self.revealed[i][j]:
                    cell = self.game_state.board[i][j]
                    if cell:
                        text, color = self._get_cell_color(cell, (i,j))
                        text_surface = self.font.render(text, True, color)
                        text_rect = text_surface.get_rect(center=(
                            x + self.cell_size//2,
                            y + self.cell_size//2
                        ))
                        self.screen.blit(text_surface, text_rect)

        self._draw_ui()

    def _draw_ui(self):
        # Draw stats in top-left corner with a smaller font
        stats_font = pygame.font.SysFont('segoeuiemoji', 24)
        
        # Health bar
        hp_text = f"{self.game_state.hp}/{self.game_state.max_hp} {self.game_state.player_emoji}"
        hp_surface = stats_font.render(hp_text, True, (255, 255, 255))
        self.screen.blit(hp_surface, (10, 10))
        
        # Potions
        potion_text = f"🧪 {self.game_state.potions}"
        potion_surface = stats_font.render(potion_text, True, (255, 255, 255))
        self.screen.blit(potion_surface, (10, 40))
        
        # Scrolls (if implemented)
        if hasattr(self.game_state, 'scrolls'):
            scroll_text = f"📜 {self.game_state.scrolls}"
            scroll_surface = stats_font.render(scroll_text, True, (255, 255, 255))
            self.screen.blit(scroll_surface, (10, 70))

        self.draw_story_log()

    def draw_story_log(self):
        # Use system font for story log
        log_font = pygame.font.SysFont('arial', 18)
        
        # Get the last few log entries
        visible_log = self.story_log[-3:]  # Show last 3 entries
        
        # Draw log entries from bottom up
        for i, entry in enumerate(reversed(visible_log)):
            y_pos = self.screen.get_height() - 30 - (i * 25)
            text_surface = log_font.render(entry, True, (200, 200, 200))
            text_rect = text_surface.get_rect(bottomleft=(10, y_pos))
            self.screen.blit(text_surface, text_rect)

    def _check_death(self):
        if self.game_state.hp <= 0:
            self.game_state.hp = 0
            from .game_over_screen import GameOverScreen
            return GameOverScreen(self.screen, self.game_state)
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            new_pos = self.game_state.current_position
            
            if event.key == pygame.K_LEFT:
                new_pos = (new_pos[0], max(0, new_pos[1] - 1))
            elif event.key == pygame.K_RIGHT:
                new_pos = (new_pos[0], min(self.grid_size - 1, new_pos[1] + 1))
            elif event.key == pygame.K_UP:
                new_pos = (max(0, new_pos[0] - 1), new_pos[1])
            elif event.key == pygame.K_DOWN:
                new_pos = (min(self.grid_size - 1, new_pos[0] + 1), new_pos[1])
            
            if new_pos != self.game_state.current_position:
                cell = self.game_state.board[new_pos[0]][new_pos[1]]
                self.game_state.current_position = new_pos
                
                if cell == 'E':  # Enemy encounter
                    from .combat_transition import CombatTransition
                    return CombatTransition(self.screen, self.game_state)
                elif cell == 'M':
                    from .combat_screen import CombatScreen
                    combat_screen = CombatScreen(self.screen, self.game_state)
                    combat_screen.parent_screen = self
                    self.story_log.append("⚔️ Encountered a monster!")
                    return combat_screen
                elif cell == 'I':
                    self.game_state.potions += 1
                    self.game_state.items_collected += 1
                    self.game_state.board[new_pos[0]][new_pos[1]] = None
                    self.story_log.append("💎 Found a healing potion!")
                elif cell == 'T':
                    damage = random.randint(10, 20)
                    self.game_state.hp -= damage
                    self.game_state.board[new_pos[0]][new_pos[1]] = None
                    self.story_log.append(f"💀 Triggered a trap! Took {damage} damage!")
                    if self._check_death():
                        from .game_over_screen import GameOverScreen
                        return GameOverScreen(self.screen, self.game_state)
        
        return None