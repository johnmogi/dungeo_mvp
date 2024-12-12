class ScreenManager:
    @staticmethod
    def get_screen(screen_name, screen, game_state):
        if screen_name == 'welcome':
            from .welcome_screen import WelcomeScreen
            return WelcomeScreen(screen, game_state)
        elif screen_name == 'character_select':
            from .character_select import CharacterSelect
            return CharacterSelect(screen, game_state)
        elif screen_name == 'game_board':
            from .game_board import GameBoard
            return GameBoard(screen, game_state)
        elif screen_name == 'combat':
            from .combat_screen import CombatScreen
            return CombatScreen(screen, game_state)
        elif screen_name == 'boss_combat':
            from .boss_combat import BossCombat
            return BossCombat(screen, game_state)
        elif screen_name == 'game_over':
            from .game_over_screen import GameOverScreen
            return GameOverScreen(screen, game_state)
        elif screen_name == 'victory':
            from .victory_screen import VictoryScreen
            return VictoryScreen(screen, game_state)
        else:
            raise ValueError(f"Unknown screen name: {screen_name}")
