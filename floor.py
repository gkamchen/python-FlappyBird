import os

import pygame

IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'floor.png')))


class Floor:
    SPEED = 5
    WIDTH = IMAGE_FLOOR.get_width()
    IMAGE = IMAGE_FLOOR

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        # Quando o chão 1 sair da tela, ele vai para trás do chão 2
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        # Quando o chão 2 sair da tela, ele vai para trás do chão 1
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))
