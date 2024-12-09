import pygame
import cv2
import os
import numpy as np
from screens.welcome_screen import WelcomeScreen

class LoadingScreen:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.video_path = os.path.join("assets", "video", "TL.mp4")
        self.cap = cv2.VideoCapture(self.video_path)
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.duration = 5000  # 5 seconds in milliseconds
        self.progress = 0
        self.skip_button = pygame.Rect(self.screen.get_width() - 100, 10, 90, 30)
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.skip_button.collidepoint(event.pos):
                self.cap.release()
                return WelcomeScreen(self.screen, self.game_state)
        return None

    def update(self):
        current_time = pygame.time.get_ticks()
        self.progress = min((current_time - self.start_time) / self.duration, 1.0)
        
        if self.progress >= 1.0:
            self.cap.release()
            return WelcomeScreen(self.screen, self.game_state)
        return None

    def draw(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Read and display video frame
        ret, frame = self.cap.read()
        if ret:
            # If we reached the end of the video, loop it
            if frame is None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            
            # Convert frame from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.screen.get_width(), self.screen.get_height()))
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.screen.blit(surface, (0, 0))
        
        # Draw progress bar
        bar_width = self.screen.get_width() - 100
        bar_height = 20
        bar_x = 50
        bar_y = self.screen.get_height() - 50
        
        # Background bar
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (bar_x, bar_y, bar_width, bar_height))
        # Progress bar
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (bar_x, bar_y, bar_width * self.progress, bar_height))
        
        # Draw skip button
        pygame.draw.rect(self.screen, (200, 200, 200), self.skip_button)
        skip_text = self.font.render("Skip", True, (0, 0, 0))
        self.screen.blit(skip_text, (self.skip_button.x + 10, self.skip_button.y + 5))
