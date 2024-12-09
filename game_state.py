class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        # Screen management
        self.current_screen = None
        self.sound_enabled = True
        self.cheat_mode = False
        
        # Board state
        self.board = [[None] * 3 for _ in range(3)]
        self.current_position = (0, 0)
        
        # Character stats
        self.selected_character = None
        self.hp = 0
        self.max_hp = 0
        self.attack = 0
        self.defense = 0
        self.potions = 3
        
        # Game progress
        self.rooms_cleared = 0
        self.monsters_defeated = 0
        self.items_collected = 0
        
        # Achievements
        self.achievements = {
            "Perfect Victory": False,  # Complete game with full HP
            "Monster Slayer": False,  # Defeat all monsters
            "Treasure Hunter": False,  # Collect all items
            "Speed Runner": False,    # Clear dungeon in minimal moves
            "Survivor": False         # Win with less than 25% HP
        }

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def toggle_cheat_mode(self):
        self.cheat_mode = not self.cheat_mode
        return self.cheat_mode

    def update_achievements(self):
        if self.hp == self.max_hp:
            self.achievements["Perfect Victory"] = True
        if self.monsters_defeated >= 3:  # Assuming 3 monsters on board
            self.achievements["Monster Slayer"] = True
        if self.items_collected >= 2:    # Assuming 2 items on board
            self.achievements["Treasure Hunter"] = True
        if self.rooms_cleared <= 5:      # Optimal path is 5 moves
            self.achievements["Speed Runner"] = True
        if self.hp <= self.max_hp * 0.25:
            self.achievements["Survivor"] = True
