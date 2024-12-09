import pygame

class CharacterSelectScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.SELECTED_COLOR = (255, 215, 0)  # Gold
        
        # Character options
        self.characters = ["WARRIOR", "ARCHER", "MAGE"]
        self.selected_index = 0
        
        # Button rectangles
        self.char_buttons = [pygame.Rect(150 + i*200, 150, 150, 50) for i in range(3)]
        self.confirm_button = pygame.Rect(250, 500, 150, 50)
        self.back_button = pygame.Rect(450, 500, 150, 50)
        
        # Character stats
        self.stats = {
            "WARRIOR": {"HP": 100, "ATK": 20, "DEF": 15},
            "ARCHER": {"HP": 80, "ATK": 25, "DEF": 10},
            "MAGE": {"HP": 70, "ATK": 30, "DEF": 5}
        }
        
        # Items and specials
        self.items = {
            "WARRIOR": ["Health Potion x2", "Basic Sword"],
            "ARCHER": ["Health Potion x2", "Basic Bow"],
            "MAGE": ["Health Potion x2", "Basic Staff"]
        }
        self.specials = {
            "WARRIOR": "Shield Block",
            "ARCHER": "Quick Shot",
            "MAGE": "Magic Barrier"
        }

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle character selection
            for i, button in enumerate(self.char_buttons):
                if button.collidepoint(mouse_pos):
                    self.selected_index = i
            
            # Handle confirm and back buttons
            if self.confirm_button.collidepoint(mouse_pos):
                self.game_state.selected_character = self.characters[self.selected_index]
                # TODO: Return game board screen
                pass
            elif self.back_button.collidepoint(mouse_pos):
                from screens.welcome_screen import WelcomeScreen
                return WelcomeScreen(self.screen, self.game_state)
        
        return None

    def draw(self):
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw title
        title = self.font.render("Select Your Hero", True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Draw character buttons
        for i, (button, char) in enumerate(zip(self.char_buttons, self.characters)):
            color = self.SELECTED_COLOR if i == self.selected_index else self.WHITE
            pygame.draw.rect(self.screen, color, button)
            char_text = self.font.render(char, True, self.BLACK)
            char_text_rect = char_text.get_rect(center=button.center)
            self.screen.blit(char_text, char_text_rect)
        
        # Draw selected character stats
        selected_char = self.characters[self.selected_index]
        stats = self.stats[selected_char]
        y_pos = 250
        for stat, value in stats.items():
            stat_text = self.small_font.render(f"{stat}: {value}", True, self.WHITE)
            self.screen.blit(stat_text, (50, y_pos))
            y_pos += 30
        
        # Draw items
        y_pos += 20
        items_text = self.small_font.render("Items:", True, self.WHITE)
        self.screen.blit(items_text, (50, y_pos))
        y_pos += 30
        for item in self.items[selected_char]:
            item_text = self.small_font.render(f"- {item}", True, self.WHITE)
            self.screen.blit(item_text, (70, y_pos))
            y_pos += 30
        
        # Draw special ability
        y_pos += 20
        special_text = self.small_font.render("Special:", True, self.WHITE)
        self.screen.blit(special_text, (50, y_pos))
        y_pos += 30
        ability_text = self.small_font.render(f"- {self.specials[selected_char]}", True, self.WHITE)
        self.screen.blit(ability_text, (70, y_pos))
        
        # Draw confirm and back buttons
        pygame.draw.rect(self.screen, self.WHITE, self.confirm_button)
        confirm_text = self.font.render("CONFIRM", True, self.BLACK)
        confirm_text_rect = confirm_text.get_rect(center=self.confirm_button.center)
        self.screen.blit(confirm_text, confirm_text_rect)
        
        pygame.draw.rect(self.screen, self.WHITE, self.back_button)
        back_text = self.font.render("BACK", True, self.BLACK)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)

    def update(self):
        pass
