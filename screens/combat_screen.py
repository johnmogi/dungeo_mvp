import pygame
import random
from .base_screen import BaseScreen
from .game_over_screen import GameOverScreen

class CombatScreen(BaseScreen):
   def __init__(self, screen, game_state):
       super().__init__(screen, game_state)
       self.choices = ['R', 'P', 'S']
       self.choice_emojis = {'R': '🪨', 'P': '📄', 'S': '✂️'}
       self.selected = 0
       self.monster_hp = 50
       self.monster_max_hp = 50
       self.player_choice = None 
       self.monster_choice = None
       self.last_result = None
       self.turn_phase = 'choose'
       self.combat_log = []

   def draw(self):
       self.screen.fill((20, 20, 30))
       self._draw_health_bars()
       
       if self.turn_phase == 'choose':
           self._draw_combat_options()
       else:
           self._draw_combat_result()
           for i, msg in enumerate(self.combat_log[-3:]):
               self.draw_text(msg, (200, 200, 200),
                   (self.screen.get_width()//2, 400 + i * 30))

   def _draw_health_bars(self):
       self.draw_text(f"Hero HP: {self.game_state.hp}/{self.game_state.max_hp}", 
                     (255, 255, 255), (200, 50))
       self.draw_text(f"Monster HP: {self.monster_hp}/{self.monster_max_hp}", 
                     (255, 255, 255), (600, 50))

   def _draw_combat_options(self):
       options = [f'Rock {self.choice_emojis["R"]}', 
                 f'Paper {self.choice_emojis["P"]}', 
                 f'Scissors {self.choice_emojis["S"]}', 
                 'Use Potion 🧪', 
                 'Flee 🏃']
       for i, option in enumerate(options):
           color = (255, 255, 0) if i == self.selected else (255, 255, 255)
           self.draw_text(option, color, 
                         (self.screen.get_width()//2, 250 + i * 50))

   def _draw_combat_result(self):
       if self.last_result:
           self.draw_text(self.last_result, (255, 255, 255), 
                         (self.screen.get_width()//2, 300))
           self.draw_text("Press SPACE to continue", (200, 200, 200), 
                         (self.screen.get_width()//2, 500))

   def handle_event(self, event):
       if event.type != pygame.KEYDOWN:
           return None

       if self.turn_phase == 'choose':
           return self._handle_choice(event.key)
       else:
           return self._handle_result(event.key)

   def _handle_choice(self, key):
       if key == pygame.K_UP:
           self.selected = (self.selected - 1) % 5
       elif key == pygame.K_DOWN:
           self.selected = (self.selected + 1) % 5
       elif key in [pygame.K_RETURN, pygame.K_SPACE]:
           if self.selected < 3:  # RPS choice
               self.player_choice = self.choices[self.selected]
               self.monster_choice = random.choice(self.choices)
               damage = self._calculate_damage()
               self.monster_hp -= damage
               self.last_result = f"You chose {self.choice_emojis[self.player_choice]}, Monster chose {self.choice_emojis[self.monster_choice]} "
               self.last_result += f"• Damage dealt: {damage}"
               self.turn_phase = 'result'
           elif self.selected == 3:  # Use potion
               if self.game_state.potions > 0:
                   self.game_state.potions -= 1
                   heal = min(30, self.game_state.max_hp - self.game_state.hp)
                   self.game_state.hp += heal
                   self.last_result = f"Used potion 🧪 • Healed {heal} HP"
                   self.combat_log.append("Potion used - Monster skips its turn!")
                   self.turn_phase = 'result'
                   return None  # Skip monster's turn
           elif self.selected == 4:  # Flee
               if random.random() < 0.7:
                   return self.parent_screen
               else:
                   self.last_result = "Failed to flee! 😱"
                   self.turn_phase = 'result'
       return None

   def _calculate_damage(self):
       if self.player_choice == self.monster_choice:
           return 10
       wins = {'R': 'S', 'P': 'R', 'S': 'P'}
       if wins[self.player_choice] == self.monster_choice:
           return 20
       return 5

   def _check_death(self):
       if self.game_state.hp <= 0:
           self.game_state.hp = 0
           return GameOverScreen(self.screen, self.game_state)
       return None

   def _handle_result(self, key):
       if key in [pygame.K_RETURN, pygame.K_SPACE]:
           self.turn_phase = 'choose'
           self.player_choice = None
           self.monster_choice = None
           return self._check_death()
       return None