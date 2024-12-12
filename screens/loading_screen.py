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
        self.duration = 3  # seconds
        self.font = pygame.font.SysFont('arial', 36)
        self.frame_time = 1.0 / 30  # Default to 30 FPS
        self.last_frame_time = 0
        
        # Video setup with error handling
        try:
            self.cap = cv2.VideoCapture('assets/loading.mp4')
            if not self.cap.isOpened():
                print("Warning: Could not open video file")
                self.current_frame = None
                return
                
            # Get video properties
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            if self.fps > 0:  # Only update frame_time if FPS is valid
                self.frame_time = 1.0 / self.fps
            
            # Pre-process first frame
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = self._process_frame(frame)
            else:
                self.current_frame = None
                
        except Exception as e:
            print(f"Error initializing video: {e}")
            self.cap = None
            self.current_frame = None

    def _process_frame(self, frame):
        if frame is None:
            return None
            
        try:
            # Convert color and flip
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)  # Horizontal flip
            
            # Calculate scaling
            screen_ratio = self.screen.get_width() / self.screen.get_height()
            frame_ratio = frame.shape[1] / frame.shape[0]
            
            if frame_ratio > screen_ratio:
                new_width = self.screen.get_width()
                new_height = int(new_width / frame_ratio)
            else:
                new_height = self.screen.get_height()
                new_width = int(new_height * frame_ratio)
                
            # Resize frame
            frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert to pygame surface
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            return surface, new_width, new_height
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Handle video frame if video is available
        if hasattr(self, 'cap') and self.cap is not None:
            current_time = time.time()
            if current_time - self.last_frame_time >= self.frame_time:
                try:
                    ret, frame = self.cap.read()
                    if ret:
                        processed = self._process_frame(frame)
                        if processed:
                            self.current_frame = processed
                    else:
                        # Reset video to start
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.last_frame_time = current_time
                except Exception as e:
                    print(f"Error reading frame: {e}")
        
        # Draw current frame if available
        if self.current_frame:
            try:
                surface, width, height = self.current_frame
                x = (self.screen.get_width() - width) // 2
                y = (self.screen.get_height() - height) // 2
                self.screen.blit(surface, (x, y))
            except Exception as e:
                print(f"Error drawing frame: {e}")
                
        # Draw loading text with animated dots
        dots = "." * (int(time.time() * 2) % 4)
        text = self.font.render(f"Loading{dots}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width()//2, 
                                        self.screen.get_height() - 50))
        self.screen.blit(text, text_rect)

    def update(self):
        if time.time() - self.start_time >= self.duration:
            if hasattr(self, 'cap') and self.cap is not None:
                self.cap.release()
            return WelcomeScreen(self.screen, self.game_state)
        return None

    def __del__(self):
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()