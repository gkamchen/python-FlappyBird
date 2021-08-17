import os
import random

import pygame

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
RANGE_PIPE_MIN = 50
RANGE_PIPE_MAX = 450

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'floor.png')))
IMAGE_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
IMAGES_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))
]

pygame.font.init()
FONT_POINTS = pygame.font.SysFont('arial', 50)


class Bird:
    IMGS = IMAGES_BIRD
    # animações da rotação, efeito parábola
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.count_image = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # calcular o deslocamento
        self.time += 1
        displacement = 1.5 * (self.time ** 2) + self.speed * self.time

        # restringir o deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            # Desloca o pássaro 2x mais pra cima para ficar mais jogável, visto que ele sobe pouco sem isso
            displacement -= 2

        self.y += displacement

        # angulo do pássaro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.SPEED_ROTATION

    def draw(self, screen):
        # definir imagem do pássaro
        self.count_image += 1

        if self.count_image < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.count_image < self.ANIMATION_TIME * 2:
            self.image = self.IMGS[1]
        elif self.count_image < self.ANIMATION_TIME * 3:
            self.image = self.IMGS[2]
        elif self.count_image < self.ANIMATION_TIME * 4:
            self.image = self.IMGS[1]
        elif self.count_image >= self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.count_image = 0

        # se o pássaro estiver caindo, não bater asa
        if self.angle <= -80:
            self.image = self.IMGS[1]
            # definir que a primeira batida de asa é pra baixo
            self.count_image = self.ANIMATION_TIME * 2

        # desenhar imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center_pos = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=image_center_pos)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


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


def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(IMAGE_BG, (0, 0))
    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    text = FONT_POINTS.render(f"Pontuação: {points}", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    floor.draw(screen)
    pygame.display.update()


def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        # interação do usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        # mover os pássaros no jogo
        for bird in birds:
            bird.move()

        # mover o chão
        floor.move()

        # mover os canos
        pipe_add = False
        pipes_remove = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                if not pipe.pass_bird and bird.x > pipe.x:
                    pipe.pass_bird = True
                    pipe_add = True
            pipe.move()

            if pipe.x + pipe.UP_PIPE_IMG.get_width() < 0:
                pipes_remove.append(pipe)

        if pipe_add:
            points += 1
            pipes.append(Pipe(600))

        for pipe in pipes_remove:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, points)


if __name__ == '__main__':
    main()
