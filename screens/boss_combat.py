import pygame
import random
from .combat_screen import CombatScreen
from .victory_screen import VictoryScreen

class BossCombat(CombatScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.monster_hp = 100
        self.monster_max_hp = 100
        
    def _calculate_damage(self):
        base_damage = super()._calculate_damage()
        return int(base_damage * 0.7)  # Boss takes less damage

    def _handle_result(self, key):
        if key == pygame.K_SPACE:
            if self.monster_hp <= 0:
                self.game_state.monsters_defeated += 1
                return VictoryScreen(self.screen, self.game_state)
            self.turn_phase = 'choose'
            
            # Boss hits harder
            monster_damage = random.randint(15, 25)
            self.game_state.hp -= monster_damage
            
            death_check = self._check_death()
            if death_check:
                return death_check
        return None