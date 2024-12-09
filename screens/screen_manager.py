class ScreenManager:
    @staticmethod
    def get_screen(screen_name, screen, game_state):
        # Import screens here to avoid circular imports
        from .welcome_screen import WelcomeScreen
        from .loading_screen import LoadingScreen
        from .character_select import CharacterSelect
        from .game_board import GameBoard
        from .combat_screen import CombatScreen
        from .game_over_screen import GameOverScreen
        from .victory_screen import VictoryScreen

        screens = {
            'welcome': WelcomeScreen,
            'loading': LoadingScreen,
            'character_select': CharacterSelect,
            'game_board': GameBoard,
            'combat': CombatScreen,
            'game_over': GameOverScreen,
            'victory': VictoryScreen
        }
        
        return screens[screen_name](screen, game_state)
