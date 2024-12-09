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
            "Perfect Victory": False,
            "Monster Slayer": False,
            "Treasure Hunter": False,
            "Speed Runner": False,
            "Survivor": False
        }

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def toggle_cheat_mode(self):
        self.cheat_mode = not self.cheat_mode
        if self.cheat_mode and self.selected_character:  # Only if character is selected
            self.hp = 999999
            self.max_hp = 999999
        return self.cheat_mode

    def update_achievements(self):
        if self.hp == self.max_hp:
            self.achievements["Perfect Victory"] = True
        if self.monsters_defeated >= 3:
            self.achievements["Monster Slayer"] = True
        if self.items_collected >= 2:
            self.achievements["Treasure Hunter"] = True
        if self.rooms_cleared <= 5:
            self.achievements["Speed Runner"] = True
        if self.hp <= self.max_hp * 0.25:
            self.achievements["Survivor"] = True

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def toggle_cheat_mode(self):
        self.cheat_mode = not self.cheat_mode
        if self.cheat_mode:
            self.hp = 999999
            self.max_hp = 999999

# combat_screen.py and boss_combat.py - add to _handle_result:
def _handle_result(self, key):
    if key == pygame.K_SPACE:
        if self.monster_hp <= 0:
            self.game_state.monsters_defeated += 1
            return self.parent_screen
        self.turn_phase = 'choose'
        
        if not self.game_state.cheat_mode:  # Only take damage if not in cheat mode
            monster_damage = random.randint(5, 15)
            self.game_state.hp -= monster_damage

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
