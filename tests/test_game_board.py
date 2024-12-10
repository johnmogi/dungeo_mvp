import unittest
import pygame
from screens.game_board import GameBoard
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

class TestGameBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()

    def setUp(self):
        self.game_state = GameState()
        self.game_state.hp = 100
        self.game_state.max_hp = 100
        self.screen = MockScreen()
        self.board = GameBoard(self.screen, self.game_state)

    def test_initial_board_state(self):
        """Test initial board setup"""
        # Check board dimensions
        self.assertEqual(len(self.game_state.board), 3)
        self.assertEqual(len(self.game_state.board[0]), 3)
        
        # Check start and end positions
        self.assertEqual(self.game_state.board[0][0], 'S')
        self.assertEqual(self.game_state.board[2][2], 'E')
        
        # Check revealed cells
        self.assertTrue(self.board.revealed[0][0])
        self.assertFalse(self.board.revealed[1][1])

    def test_movement_handling(self):
        """Test movement and cell interaction"""
        # Test valid movement
        next_screen = self.board._handle_movement((0, 1))
        self.assertTrue(self.board.revealed[0][1])
        
        # Test movement to item cell
        self.game_state.board[0][1] = 'I'
        initial_potions = self.game_state.potions
        next_screen = self.board._handle_movement((0, 1))
        self.assertEqual(self.game_state.potions, initial_potions + 1)
        self.assertIsNone(self.game_state.board[0][1])
        
        # Test movement to trap
        self.game_state.board[1][0] = 'T'
        initial_hp = self.game_state.hp
        next_screen = self.board._handle_movement((1, 0))
        self.assertLess(self.game_state.hp, initial_hp)
        self.assertIsNone(self.game_state.board[1][0])

    def test_death_check(self):
        """Test death condition checking"""
        self.game_state.hp = 0
        result = self.board._check_death()
        self.assertIsNotNone(result)
        
        self.game_state.hp = 50
        result = self.board._check_death()
        self.assertIsNone(result)

    def test_cell_symbols(self):
        """Test cell symbol and color generation"""
        # Test player position
        text, color = self.board._get_cell_color(None, self.game_state.current_position)
        self.assertEqual(text, '👤')
        self.assertEqual(color, (255, 255, 0))
        
        # Test other cells
        monster_text, monster_color = self.board._get_cell_color('M', (1, 1))
        self.assertEqual(monster_text, '👾')
        
        item_text, item_color = self.board._get_cell_color('I', (1, 1))
        self.assertEqual(item_text, '💎')

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
