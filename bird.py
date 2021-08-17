import os

import pygame

IMAGES_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))
]

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

