import pygame

class MyClock:
    def __init__(self, fps) -> None:
        self.CLOCK = pygame.time.Clock()
        self.FPS = fps
    
    def tick(self) -> None:
        self.CLOCK.tick(self.FPS)