import pygame
import random
from .base_screen import BaseScreen
from .game_over_screen import GameOverScreen
from .victory_screen import VictoryScreen

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
       
       # Initialize spells if not present
       if not hasattr(game_state, 'spells'):
           game_state.spells = {
               'fireball': 3,  # 3 uses
               'ice': 2,      # 2 uses
               'heal': 1      # 1 use
           }

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
       bar_width = 200
       bar_height = 20
       
       # Player health bar
       player_hp_percent = self.game_state.hp / self.game_state.max_hp
       pygame.draw.rect(self.screen, (100, 0, 0), (50, 50, bar_width, bar_height))
       pygame.draw.rect(self.screen, (0, 255, 0), 
                       (50, 50, bar_width * player_hp_percent, bar_height))
       
       # Monster health bar
       monster_hp_percent = self.monster_hp / self.monster_max_hp
       pygame.draw.rect(self.screen, (100, 0, 0), 
                       (self.screen.get_width() - 250, 50, bar_width, bar_height))
       pygame.draw.rect(self.screen, (255, 0, 0),
                       (self.screen.get_width() - 250, 50, 
                        bar_width * monster_hp_percent, bar_height))
       
       # Draw HP numbers with smaller font
       stats_font = pygame.font.SysFont('arial', 20)
       
       hp_text = f"{self.game_state.hp}/{self.game_state.max_hp} HP"
       hp_surface = stats_font.render(hp_text, True, (255, 255, 255))
       self.screen.blit(hp_surface, (50, 75))
       
       monster_hp_text = f"{self.monster_hp}/{self.monster_max_hp} HP"
       monster_hp_surface = stats_font.render(monster_hp_text, True, (255, 255, 255))
       self.screen.blit(monster_hp_surface, (self.screen.get_width() - 250, 75))
       
       # Draw potion count
       potion_text = f"🧪 {self.game_state.potions}"
       potion_surface = stats_font.render(potion_text, True, (255, 255, 255))
       self.screen.blit(potion_surface, (50, 100))
       
       # Draw spell counts
       if hasattr(self.game_state, 'spells'):
           spell_y = 125
           for spell, count in self.game_state.spells.items():
               spell_icons = {
                   'fireball': '🔥',
                   'ice': '❄️',
                   'heal': '💚'
               }
               spell_text = f"{spell_icons.get(spell, '📜')} {spell}: {count}"
               spell_surface = stats_font.render(spell_text, True, (255, 255, 255))
               self.screen.blit(spell_surface, (50, spell_y))
               spell_y += 25

   def _draw_combat_options(self):
       base_y = 250  # Start drawing options lower to avoid overlap
       options = [
           f'Rock {self.choice_emojis["R"]}', 
           f'Paper {self.choice_emojis["P"]}', 
           f'Scissors {self.choice_emojis["S"]}',
           'Use Potion 🧪'
       ]
       
       # Add spell options if available
       if hasattr(self.game_state, 'spells'):
           spell_icons = {
               'fireball': '🔥 Fireball (20 dmg)',
               'ice': '❄️ Ice Blast (15 dmg)',
               'heal': '💚 Healing Word (25 hp)'
           }
           for spell, count in self.game_state.spells.items():
               if count > 0:
                   options.append(spell_icons[spell])
       
       options.append('Flee 🏃')
       
       for i, option in enumerate(options):
           color = (255, 255, 0) if i == self.selected else (255, 255, 255)
           self.draw_text(option, color, 
                         (self.screen.get_width()//2, base_y + i * 40))

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
           self.selected = (self.selected - 1) % 7
       elif key == pygame.K_DOWN:
           self.selected = (self.selected + 1) % 7
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
           elif self.selected == 4:  # Use spell
               spell = list(self.game_state.spells.keys())[self.selected - 4]
               if self.game_state.spells[spell] > 0:
                   self.game_state.spells[spell] -= 1
                   if spell == 'fireball':
                       damage = 20
                       self.monster_hp -= damage
                       self.last_result = f"Cast 🔥 Fireball • Damage dealt: {damage}"
                   elif spell == 'ice':
                       damage = 15
                       self.monster_hp -= damage
                       self.last_result = f"Cast ❄️ Ice Blast • Damage dealt: {damage}"
                   elif spell == 'heal':
                       heal = min(25, self.game_state.max_hp - self.game_state.hp)
                       self.game_state.hp += heal
                       self.last_result = f"Cast 💚 Healing Word • Healed {heal} HP"
                   self.turn_phase = 'result'
           elif self.selected == 5:  # Flee
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
           if self.monster_hp <= 0:
               self.game_state.monsters_defeated += 1
               if self.game_state.monsters_defeated >= 3:  # Only show victory after 3+ monsters
                   return VictoryScreen(self.screen, self.game_state)
               return self.parent_screen  # Return to game board for regular monsters
           self.turn_phase = 'choose'
           self.player_choice = None
           self.monster_choice = None
           
           if not self.game_state.cheat_mode:  # Only take damage if not in cheat mode
               monster_damage = random.randint(10, 20)
               self.game_state.hp -= monster_damage
               death_check = self._check_death()
               if death_check:
                   return death_check
           return None
       return None