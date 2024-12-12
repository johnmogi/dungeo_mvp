import pygame
import random
from .base_screen import BaseScreen
from .game_board import GameBoard  # Import GameBoard from game_board module

class CombatScreen(BaseScreen):
   def __init__(self, screen, game_state):
       super().__init__(screen, game_state)
       self.choices = ['R', 'P', 'S']
       self.choice_emojis = {'R': '⚔️', 'P': '🛡️', 'S': '💚'}
       self.selected = 0
       self.monster_hp = 50
       self.monster_max_hp = 50
       self.monster_attack = 10
       self.monster_defense = 5
       self.last_result = ""
       self.turn_phase = 'choice'  # 'choice' or 'result'
       self.combat_log = []
       self.current_monster = None
       self.options = []  # Initialize options list
       self._update_options()  # Update options when screen is created

   def _update_options(self):
       # Update the available options
       self.options = [
           ('Attack', '⚔️'),
           ('Defend', '🛡️'),
           ('Use Potion', '💚'),
           ('Run', '🏃')
       ]
       
       # Add character abilities if available
       if hasattr(self.game_state, 'selected_character'):
           char_data = self.game_state.selected_character
           if char_data and 'abilities' in char_data:
               for ability_name, ability in char_data['abilities'].items():
                   if ability['uses'] > 0:
                       self.options.append((ability['desc'], ability['icon']))

   def draw(self):
       self.screen.fill((20, 20, 30))
       self._draw_health_bars()
       
       if self.turn_phase == 'choice':
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
       
       hp_text = f"{self.game_state.hp}/{self.game_state.max_hp} 👨"
       hp_surface = stats_font.render(hp_text, True, (255, 255, 255))
       self.screen.blit(hp_surface, (50, 75))
       
       monster_hp_text = f"{self.monster_hp}/{self.monster_max_hp} ❤️"
       monster_hp_surface = stats_font.render(monster_hp_text, True, (255, 255, 255))
       self.screen.blit(monster_hp_surface, (self.screen.get_width() - 250, 75))
       
       # Draw potion count
       potion_text = f"💚 {self.game_state.potions}"
       potion_surface = stats_font.render(potion_text, True, (255, 255, 255))
       self.screen.blit(potion_surface, (50, 100))
       
       # Draw character abilities
       if hasattr(self.game_state, 'selected_character'):
           char_data = self.game_state.selected_character
           if char_data and 'abilities' in char_data:
               ability_y = 125
               for ability_name, ability in char_data['abilities'].items():
                   if ability['uses'] > 0:
                       ability_text = f"{ability['icon']} {ability['desc']}: {ability['uses']} uses"
                       ability_surface = stats_font.render(ability_text, True, (255, 255, 255))
                       self.screen.blit(ability_surface, (50, ability_y))
                       ability_y += 25

   def _draw_combat_options(self):
       base_y = 250
        
       # Update options before drawing
       self._update_options()
        
       # Draw standard options
       for i, (option, icon) in enumerate(self.options):
           color = (255, 255, 0) if i == self.selected else (255, 255, 255)
           self.draw_text(f"{icon} {option}", color, 
                         (self.screen.get_width()//2, base_y + i * 40))
            
           # If this is the selected option and it's an ability, show description
           if i == self.selected and i >= 4:
               char_data = self.game_state.selected_character
               ability_idx = i - 4
               abilities = list(char_data['abilities'].items())
               if ability_idx < len(abilities):
                   _, ability = abilities[ability_idx]
                   desc = []
                   if 'damage' in ability:
                       desc.append(f"Damage: {ability['damage']}")
                   if 'heal' in ability:
                       desc.append(f"Heal: {ability['heal']}")
                   if 'defense' in ability:
                       desc.append(f"Defense: {ability['defense']}")
                   desc.append(f"Uses left: {ability['uses']}")
                    
                   for j, text in enumerate(desc):
                       self.draw_text(text, (150, 150, 150),
                                     (self.screen.get_width()//2, base_y + len(self.options) * 40 + j * 25))

   def _draw_combat_result(self):
       if self.last_result:
           self.draw_text(self.last_result, (255, 255, 255), 
                         (self.screen.get_width()//2, 300))
           self.draw_text("Press SPACE to continue", (200, 200, 200), 
                         (self.screen.get_width()//2, 500))

   def handle_event(self, event):
       if event.type != pygame.KEYDOWN:
           return None

       if self.turn_phase == 'choice':
           return self._handle_choice(event.key)
       else:
           return self._handle_result(event.key)

   def _handle_choice(self, key):
       if key == pygame.K_RETURN:
           if self.selected == len(self.options) - 1:  # Run option
               if random.random() < 0.5:
                   self.last_result = "Escaped successfully! 🏃"
                   return GameBoard(self.screen, self.game_state)
               else:
                   self.last_result = "Failed to escape! 😱"
                   self.turn_phase = 'result'
                   return None
            
           elif self.selected == 2:  # Use Potion
               if self.game_state.potions > 0:
                   self.game_state.potions -= 1
                   heal = min(30, self.game_state.max_hp - self.game_state.hp)
                   self.game_state.hp += heal
                   self.last_result = f"Used potion 💚 • Healed {heal} HP"
                   self.combat_log.append("Potion used - Monster skips its turn!")
                   self.turn_phase = 'result'
                   return None
               else:
                   self.last_result = "No potions left! 😱"
                   return None
            
           elif self.selected == 0:  # Attack
               damage = max(1, self.game_state.attack - self.monster_defense)
               self.monster_hp -= damage
               self.last_result = f"You dealt {damage} damage! ⚔️"
               self.turn_phase = 'result'
               return None
            
           elif self.selected == 1:  # Defend
               self.game_state.defense += 5
               self.last_result = "Defense increased! 🛡️"
               self.turn_phase = 'result'
               return None
            
           else:  # Use ability
               char_data = self.game_state.selected_character
               ability_idx = self.selected - 4
               abilities = list(char_data['abilities'].items())
               if ability_idx < len(abilities):
                   ability_name, ability = abilities[ability_idx]
                    
                   if ability['uses'] > 0:
                       ability['uses'] -= 1
                       if 'damage' in ability:
                           damage = ability['damage']
                           self.monster_hp -= damage
                           self.last_result = f"{ability['icon']} {ability['desc']} dealt {damage} damage!"
                       elif 'heal' in ability:
                           heal = min(ability['heal'], self.game_state.max_hp - self.game_state.hp)
                           self.game_state.hp += heal
                           self.last_result = f"{ability['icon']} {ability['desc']} healed {heal} HP!"
                       elif 'defense' in ability:
                           self.game_state.defense += ability['defense']
                           self.last_result = f"{ability['icon']} {ability['desc']} increased defense by {ability['defense']}!"
                       self.turn_phase = 'result'
                       return None
                   else:
                       self.last_result = "No uses left! 😱"
                       return None
        
       elif key == pygame.K_UP:
           self.selected = (self.selected - 1) % len(self.options)
       elif key == pygame.K_DOWN:
           self.selected = (self.selected + 1) % len(self.options)
        
       return None

   def _handle_result(self, key):
       if key in [pygame.K_RETURN, pygame.K_SPACE]:
           if self.monster_hp <= 0:
               self.game_state.monsters_defeated += 1
               if self.game_state.monsters_defeated >= 3:  # Only show victory after 3+ monsters
                   return VictoryScreen(self.screen, self.game_state)
               return self.parent_screen  # Return to game board for regular monsters
           self.turn_phase = 'choice'
           self.last_result = ""
           
           if not self.game_state.cheat_mode:  # Only take damage if not in cheat mode
               monster_damage = random.randint(10, 20)
               self.game_state.hp -= monster_damage
               death_check = self._check_death()
               if death_check:
                   return death_check
           return None
       return None

   def _check_death(self):
       if self.game_state.hp <= 0:
           self.game_state.hp = 0
           return GameOverScreen(self.screen, self.game_state)
       return None