import pygame
import random

# Represents pixel values used for placement of images
# on the road
LEFT_START = 238
RIGHT_START = 582

class MyClock:
    def __init__(self, fps) -> None:
        self.CLOCK = pygame.time.Clock()
        self.FPS = fps
    
    def tick(self) -> None:
        self.CLOCK.tick(self.FPS)

class BackgroundImage:
    def __init__(self, width, height) -> None:
        self.IMAGE = pygame.image.load('./img/road.jpg').convert_alpha()
        self.IMAGE = pygame.transform.scale(self.IMAGE, (width, height))
        self.HEIGHT = height
        self.movableY = 0
        self.SPEED = 4

    def draw(self, screen) -> None:
        screen.blit(self.IMAGE, (0, self.movableY))
        screen.blit(self.IMAGE, (0, -self.HEIGHT + self.movableY))
        self.movableY += self.SPEED

        if self.movableY > self.HEIGHT:
            self.movableY = 0

class Player(pygame.sprite.Sprite):
    CAR_SCALE = (120, 150)
    OFFSET_CAR = 5

    HEALTH = 100

    def __init__(self, height) -> None:
        super().__init__()

        self.image = pygame.image.load('./img/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, self.CAR_SCALE)

        self.RIGHT_BORDER = RIGHT_START
        self.LEFT_BORDER = LEFT_START
        self.TOP_BORDER = self.OFFSET_CAR
        self.BOTTOM_BORDER = height - self.OFFSET_CAR

        self.SPEED = 5
        
        self.rect = self.image.get_rect( bottomleft = (self.LEFT_BORDER, self.BOTTOM_BORDER) )

        self.renderText()

    def onHit(self, damage):
        self.HEALTH -= damage

        if self.HEALTH > 100:
            self.HEALTH = 100
        
        self.renderText()
    
    def renderText(self):
        font = pygame.font.Font('./fonts/Pixeltype.ttf', 40)
        self.text = font.render(f'Health: {self.HEALTH}%', False, 'black')
        self.textRect = self.text.get_rect( topleft = (20, 20))

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.left -= self.SPEED
            if self.rect.left < self.LEFT_BORDER:
                self.rect.left = self.LEFT_BORDER

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.right += self.SPEED
            if self.rect.right > self.RIGHT_BORDER:
                self.rect.right = self.RIGHT_BORDER

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.bottom += self.SPEED
            if self.rect.bottom > self.BOTTOM_BORDER:
                self.rect.bottom = self.BOTTOM_BORDER

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.top -= self.SPEED
            if self.rect.top < self.TOP_BORDER:
                self.rect.top = self.TOP_BORDER

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

class Obstacles(pygame.sprite.Sprite):
    # Constants used to represent obstacles
    ROCKS = 1
    SAND = 2
    OIL = 3
    FUEL = 4

    # Constants used to represent amount of obstacles
    AMOUNT = [3, 5, 6, 4]
    CURRENT_AMOUNT = AMOUNT.copy()

    # Constants used to represent damage dealt to car
    ON_HIT = [25, 10, 15, -20]

    FUEL_SCALE = (100, 100)

    def __init__(self, height) -> None:
        super().__init__()

        self.OBSTACLE = self.generateRandomObstacle()

        self.image = pygame.image.load(f'./img/obstacle_{self.OBSTACLE}.png').convert_alpha()
        
        if self.OBSTACLE == 4:
            self.image = pygame.transform.scale(self.image, self.FUEL_SCALE)

        self.rect = self.generateSpawnSide()

        self.HEIGHT = height
        self.SPEED = 5

    def generateSpawnSide(self):
        side = random.choice([0, 1])

        if side == 0:
            return self.image.get_rect( topleft = (LEFT_START, -self.image.get_height()) )
        
        return self.image.get_rect( topright = (RIGHT_START, -self.image.get_height()))

    def restockObstacles(self):
        for amount in self.CURRENT_AMOUNT:
            if amount != 0:
                return

        self.CURRENT_AMOUNT = self.AMOUNT.copy()    

    def generateRandomObstacle(self):
        self.restockObstacles()

        choice = random.choice([self.ROCKS, self.SAND, self.OIL, self.FUEL])

        while self.CURRENT_AMOUNT[choice - 1] == 0:
            choice = random.choice([self.ROCKS, self.SAND, self.OIL, self.FUEL])

        self.CURRENT_AMOUNT[choice - 1] -= 1

        return choice
    

    def update(self, player=None) -> None:
        if player:
            player.onHit(self.ON_HIT[self.OBSTACLE - 1])
            return

        self.rect.top += self.SPEED

        if self.rect.top > self.HEIGHT:
            self.kill()

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)