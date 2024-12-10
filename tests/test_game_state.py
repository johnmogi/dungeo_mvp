import unittest
from game_state import GameState

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_initial_state(self):
        """Test initial game state values"""
        self.assertTrue(self.game_state.sound_enabled)
        self.assertFalse(self.game_state.cheat_mode)
        self.assertEqual(self.game_state.hp, 0)
        self.assertEqual(self.game_state.max_hp, 0)
        self.assertEqual(self.game_state.current_position, (0, 0))
        self.assertEqual(len(self.game_state.board), 3)
        self.assertEqual(len(self.game_state.board[0]), 3)

    def test_toggle_sound(self):
        """Test sound toggle functionality"""
        initial_state = self.game_state.sound_enabled
        self.game_state.toggle_sound()
        self.assertNotEqual(initial_state, self.game_state.sound_enabled)
        self.game_state.toggle_sound()
        self.assertEqual(initial_state, self.game_state.sound_enabled)

    def test_toggle_cheat_mode(self):
        """Test cheat mode toggle and its effects"""
        # Set up character first
        self.game_state.selected_character = "Warrior"
        self.game_state.hp = 100
        self.game_state.max_hp = 100
        
        # Test toggle
        self.game_state.toggle_cheat_mode()
        self.assertTrue(self.game_state.cheat_mode)
        self.assertEqual(self.game_state.hp, 999999)
        self.assertEqual(self.game_state.max_hp, 999999)
        
        # Test toggle back
        self.game_state.toggle_cheat_mode()
        self.assertFalse(self.game_state.cheat_mode)

    def test_update_achievements(self):
        """Test achievement updates based on game progress"""
        # Set up game state
        self.game_state.hp = 100
        self.game_state.max_hp = 100
        self.game_state.monsters_defeated = 3
        self.game_state.items_collected = 2
        self.game_state.rooms_cleared = 5
        
        # Update achievements
        self.game_state.update_achievements()
        
        # Check achievements
        self.assertTrue(self.game_state.achievements["Perfect Victory"])
        self.assertTrue(self.game_state.achievements["Monster Slayer"])
        self.assertTrue(self.game_state.achievements["Treasure Hunter"])
        self.assertTrue(self.game_state.achievements["Speed Runner"])
        self.assertFalse(self.game_state.achievements["Survivor"])

    def test_reset(self):
        """Test game state reset functionality"""
        # Modify state
        self.game_state.hp = 100
        self.game_state.monsters_defeated = 5
        self.game_state.cheat_mode = True
        
        # Reset
        self.game_state.reset()
        
        # Verify reset
        self.assertEqual(self.game_state.hp, 0)
        self.assertEqual(self.game_state.monsters_defeated, 0)
        self.assertFalse(self.game_state.cheat_mode)

if __name__ == '__main__':
    unittest.main()
