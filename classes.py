import pygame

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
    def __init__(self, width, height) -> None:
        super().__init__()
        CAR_SCALE = (120, 150)
        OFFSET_CAR = 5

        self.image = pygame.image.load('./img/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, CAR_SCALE)

        self.RIGHT_BORDER = width - 213
        self.LEFT_BORDER = 233
        self.TOP_BORDER = OFFSET_CAR
        self.BOTTOM_BORDER = height - OFFSET_CAR

        self.SPEED = 5
        
        self.rect = self.image.get_rect( bottomleft = (self.LEFT_BORDER, self.BOTTOM_BORDER) )

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