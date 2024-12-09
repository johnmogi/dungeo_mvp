# screens/game_board.py 
import pygame
import random
from .base_screen import BaseScreen
from .combat_screen import CombatScreen
from .game_over_screen import GameOverScreen
from .victory_screen import VictoryScreen
from .boss_combat import BossCombat

class GameBoard(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.cell_size = 120
        self.grid_size = 3
        self.margin_x = (screen.get_width() - self.cell_size * self.grid_size) // 2
        self.margin_y = 100
        self.revealed = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.revealed[0][0] = True
        
        if not any(any(cell for cell in row) for row in game_state.board):
            self._generate_board()

    def _get_cell_color(self, cell, pos):
        if pos == self.game_state.current_position:
            text = '👤'
            return text, (255, 255, 0)
        symbols = {
            'S': ('S', (0, 255, 0)),
            'E': ('👿', (255, 0, 0)),
            'M': ('👾', (200, 50, 50)),
            'I': ('💎', (50, 200, 200)),
            'T': ('💀', (200, 200, 50))
        }
        return symbols.get(cell, ('?', (255, 255, 255)))

    def _generate_board(self):
        self.game_state.board[0][0] = 'S'
        self.game_state.board[2][2] = 'E'
        events = ['M', 'I', 'T', 'M', 'I']
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i,j) not in [(0,0), (2,2)]:
                    self.game_state.board[i][j] = random.choice(events)

    def draw(self):
        self.screen.fill((20, 20, 30))
        
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

                if self.revealed[i][j]:
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
        self.draw_text("Dungeon Quest", (200, 200, 255), 
                      (self.screen.get_width()//2, 40))
        
        stats_text = f"HP: {self.game_state.hp}/{self.game_state.max_hp}  Potions: {self.game_state.potions}"
        self.draw_text(stats_text, (255, 255, 255), 
                      (self.screen.get_width()//2, self.screen.get_height() - 60))
        
        controls = "Arrow Keys: Move  |  ESC: Menu"
        self.draw_text(controls, (150, 150, 150),
                      (self.screen.get_width()//2, self.screen.get_height() - 30))

    def _check_death(self):
        if self.game_state.hp <= 0:
            self.game_state.hp = 0
            return GameOverScreen(self.screen, self.game_state)
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            x, y = self.game_state.current_position
            new_pos = None
            
            if event.key == pygame.K_UP and x > 0:
                new_pos = (x-1, y)
            elif event.key == pygame.K_DOWN and x < 2:
                new_pos = (x+1, y)
            elif event.key == pygame.K_LEFT and y > 0:
                new_pos = (x, y-1)
            elif event.key == pygame.K_RIGHT and y < 2:
                new_pos = (x, y+1)
                
            if new_pos:
                return self._handle_movement(new_pos)
        return None

    def _handle_movement(self, new_pos):
        x, y = new_pos
        self.revealed[x][y] = True
        cell = self.game_state.board[x][y]
        
        self.game_state.current_position = new_pos
        self.game_state.rooms_cleared += 1
        
        if cell == 'M':
            combat_screen = CombatScreen(self.screen, self.game_state)
            combat_screen.parent_screen = self
            return combat_screen
        elif cell == 'I':
            self.game_state.items_collected += 1
            self.game_state.potions += 1
            self.game_state.board[x][y] = None
        elif cell == 'T':
            damage = 10
            self.game_state.hp = max(0, self.game_state.hp - damage)
            self.game_state.board[x][y] = None
            
            death_check = self._check_death()
            if death_check:
                return death_check
        elif cell == 'E':
            boss_screen = BossCombat(self.screen, self.game_state)
            boss_screen.parent_screen = self
            return boss_screen
            
        return None