import pygame
import time
import os
import cv2
from .base_screen import BaseScreen
from .welcome_screen import WelcomeScreen

class LoadingScreen(BaseScreen):
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.start_time = time.time()
        self.duration = 5
        
        # Load and prepare video
        video_path = os.path.join('assets', 'video', 'TL.mp4')
        self.cap = cv2.VideoCapture(video_path)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_time = 1/self.fps
        self.last_frame_time = 0
        self.current_frame = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        current_time = time.time()
        if current_time - self.last_frame_time >= self.frame_time:
            ret, frame = self.cap.read()
            if ret:
                # Convert frame from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Scale frame to fit screen
                frame = cv2.resize(frame, (self.screen.get_width(), self.screen.get_height()))
                # Convert to pygame surface
                frame = pygame.surfarray.make_surface(frame)
                frame = pygame.transform.rotate(frame, -90)
                frame = pygame.transform.flip(frame, False, False)
                self.current_frame = frame
                self.last_frame_time = current_time
            else:
                # Video ended, restart it
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        if self.current_frame:
            self.screen.blit(self.current_frame, (0, 0))

    def update(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.duration:
            self.cap.release()
            return WelcomeScreen(self.screen, self.game_state)
        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.cap.release()
            return WelcomeScreen(self.screen, self.game_state)
        return None