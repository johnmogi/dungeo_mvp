class GameState:
    def __init__(self):
        self.sound_enabled = True
        self.cheat_mode = False
        self.selected_character = None
        self.hp = 100
        self.max_hp = 100
        self.attack = 20
        self.defense = 15
        self.potions = 2
        self.current_position = (0, 0)
        self.rooms_cleared = 0
        self.monsters_defeated = 0
        self.items_collected = 0
        self.start_time = None
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.achievements = {
            "First Blood": False,
            "Potion Master": False,
            "Perfect Run": False
        }

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled

    def toggle_cheat_mode(self):
        self.cheat_mode = not self.cheat_mode

    def reset(self):
        self.__init__()
