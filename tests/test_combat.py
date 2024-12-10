import unittest
import pygame
from screens.combat_screen import CombatScreen
from game_state import GameState

class MockScreen:
    def __init__(self):
        self.width = 800
        self.height = 600
        
    def get_width(self):
        return self.width
        
    def get_height(self):
        return self.height
        
    def fill(self, color):
        pass
        
    def blit(self, *args):
        pass

class TestCombatScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()

    def setUp(self):
        self.game_state = GameState()
        self.game_state.hp = 100
        self.game_state.max_hp = 100
        self.game_state.attack = 20
        self.game_state.defense = 15
        self.screen = MockScreen()
        self.combat = CombatScreen(self.screen, self.game_state)

    def test_initial_state(self):
        """Test initial combat screen state"""
        self.assertEqual(self.combat.monster_hp, 50)
        self.assertEqual(self.combat.monster_max_hp, 50)
        self.assertEqual(self.combat.turn_phase, 'choose')
        self.assertIsNone(self.combat.player_choice)
        self.assertIsNone(self.combat.monster_choice)

    def test_damage_calculation(self):
        """Test damage calculation for different scenarios"""
        # Test tie
        self.combat.player_choice = 'R'
        self.combat.monster_choice = 'R'
        self.assertEqual(self.combat._calculate_damage(), 10)
        
        # Test win
        self.combat.player_choice = 'R'
        self.combat.monster_choice = 'S'
        self.assertEqual(self.combat._calculate_damage(), 20)
        
        # Test loss
        self.combat.player_choice = 'R'
        self.combat.monster_choice = 'P'
        self.assertEqual(self.combat._calculate_damage(), 5)

    def test_handle_choice(self):
        """Test combat choice handling"""
        # Test selection movement
        initial_selected = self.combat.selected
        self.combat._handle_choice(pygame.K_DOWN)
        self.assertEqual(self.combat.selected, (initial_selected + 1) % 5)
        
        # Test potion use
        self.combat.selected = 3  # Potion option
        self.game_state.hp = 70
        self.game_state.potions = 1
        self.combat._handle_choice(pygame.K_RETURN)
        self.assertEqual(self.game_state.hp, 100)
        self.assertEqual(self.game_state.potions, 0)

    def test_death_check(self):
        """Test death condition checking"""
        self.game_state.hp = 0
        result = self.combat._check_death()
        self.assertIsNotNone(result)
        
        self.game_state.hp = 50
        result = self.combat._check_death()
        self.assertIsNone(result)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
