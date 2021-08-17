import os
import random

import pygame

RANGE_PIPE_MIN = 50
RANGE_PIPE_MAX = 450

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))


class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.up_pos = 0
        self.down_pos = 0
        self.UP_PIPE_IMG = pygame.transform.flip(IMAGE_PIPE, False, True)
        self.DOWN_PIPE_IMG = IMAGE_PIPE
        self.pass_bird = False
        self.define_height()

    def define_height(self):
        self.height = random.randrange(RANGE_PIPE_MIN, RANGE_PIPE_MAX)
        self.up_pos = self.height - self.UP_PIPE_IMG.get_height()
        self.down_pos = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.UP_PIPE_IMG, (self.x, self.up_pos))
        screen.blit(self.DOWN_PIPE_IMG, (self.x, self.down_pos))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        up_pipe_mask = pygame.mask.from_surface(self.UP_PIPE_IMG)
        down_pipe_mask = pygame.mask.from_surface(self.DOWN_PIPE_IMG)

        up_distance = (round(self.x) - round(bird.x), round(self.up_pos) - round(bird.y))
        down_distance = (round(self.x) - round(bird.x), round(self.down_pos) - round(bird.y))

        point_collide_up = bird_mask.overlap(up_pipe_mask, up_distance)
        point_collide_down = bird_mask.overlap(down_pipe_mask, down_distance)

        if point_collide_down or point_collide_up:
            return True
        else:
            return False
