import pygame
from sys import exit
from classes import *

class Game:
    def __init__(self, width, height, title) -> None:
        pygame.init()

        self.WIDTH = width
        self.HEIGHT = height
        self.SCREEN = pygame.display.set_mode((width, height))
        
        pygame.display.set_caption(title)

        self.CLOCK = MyClock(60)

        self.BACKGROUND = BackgroundImage(width, height)

        self.PLAYER = Player(height)

        self.obstacles = pygame.sprite.Group()
        self.obstaclesSpawnTime = 2000
        self.obstacleCurrentTime = 0

    def quit(self) -> None:
        pygame.quit()
        exit()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.BACKGROUND.draw(self.SCREEN)

            if pygame.time.get_ticks() - self.obstacleCurrentTime > self.obstaclesSpawnTime:
                self.obstacles.add( Obstacles(self.HEIGHT) )
                self.obstacleCurrentTime = pygame.time.get_ticks()
            
            self.obstacles.update()
            self.obstacles.draw(self.SCREEN)

            # Used for player damage detection
            obstacle = pygame.sprite.spritecollide(self.PLAYER, self.obstacles, True)
            if obstacle:
                for ob in obstacle:
                    ob.update(self.PLAYER)

            print(self.PLAYER.HEALTH)

            self.PLAYER.update()
            self.PLAYER.draw(self.SCREEN)

            if self.PLAYER.HEALTH <= 0:
                self.quit()

            pygame.display.update()
            self.CLOCK.tick()

if __name__ == '__main__':
    game = Game(800, 800, 'Car Driver')
    game.run()