# screens/game_board.py
import pygame
from .base_screen import BaseScreen
import random

class GameBoard(BaseScreen):  # Change name to match
   def __init__(self, screen, game_state):
       super().__init__(screen, game_state)
       self.cell_size = 150
       self.grid_size = 3
       self.margin_x = (screen.get_width() - self.cell_size * self.grid_size) // 2
       self.margin_y = 50
       self.player_pos = game_state.current_position
       
       # Initialize board if empty
       if not any(any(cell for cell in row) for row in game_state.board):
           self._generate_board()

   def _generate_board(self):
       # Place start and end
       self.game_state.board[0][0] = 'S'
       self.game_state.board[2][2] = 'E'
       
       # Place random events in other cells
       events = ['M', 'I', 'T'] # Monster, Item, Trap
       for i in range(3):
           for j in range(3):
               if (i,j) not in [(0,0), (2,2)]:
                   self.game_state.board[i][j] = random.choice(events)

   def draw(self):
       self.screen.fill((0, 0, 0))
       
       # Draw grid
       for i in range(self.grid_size):
           for j in range(self.grid_size):
               rect = pygame.Rect(
                   self.margin_x + j * self.cell_size,
                   self.margin_y + i * self.cell_size,
                   self.cell_size, self.cell_size
               )
               pygame.draw.rect(self.screen, (50, 50, 50), rect, 2)
               
               # Draw cell content
               cell = self.game_state.board[i][j]
               if cell:
                   if (i,j) == self.player_pos:
                       color = (255, 255, 0)  # Yellow for player
                   elif cell == 'S':
                       color = (0, 255, 0)    # Green for start
                   elif cell == 'E':
                       color = (255, 0, 0)    # Red for end
                   elif cell == 'M':
                       color = (200, 0, 0)    # Dark red for monster
                   elif cell == 'I':
                       color = (0, 200, 200)  # Cyan for item
                   elif cell == 'T':
                       color = (200, 200, 0)  # Yellow for trap
                   
                   # Draw colored symbol
                   text = self.font.render(cell, True, color)
                   text_rect = text.get_rect(center=(
                       self.margin_x + j * self.cell_size + self.cell_size // 2,
                       self.margin_y + i * self.cell_size + self.cell_size // 2
                   ))
                   self.screen.blit(text, text_rect)

       # Draw stats
       stats_text = f"HP: {self.game_state.hp}/{self.game_state.max_hp}  Potions: {self.game_state.potions}"
       self.draw_text(stats_text, (255, 255, 255), 
                     (self.screen.get_width()//2, self.margin_y//2))

   def handle_event(self, event):
       if event.type == pygame.KEYDOWN:
           x, y = self.player_pos
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
               self._handle_movement(new_pos)
               
       return None

   def _handle_movement(self, new_pos):
       self.player_pos = new_pos
       self.game_state.current_position = new_pos
       x, y = new_pos
       cell = self.game_state.board[x][y]
       
       if cell == 'M':
           # Combat screen
           pass
       elif cell == 'I':
           self.game_state.items_collected += 1
           self.game_state.potions += 1
           self.game_state.board[x][y] = None
       elif cell == 'T':
           self.game_state.hp = max(0, self.game_state.hp - 10)
           self.game_state.board[x][y] = None
       elif cell == 'E':
           # Victory screen
           pass

   def update(self):
       return None