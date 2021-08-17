import os

import pygame
import bird as cbird
import pipe as cpipe
import floor as cfloor

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
IMAGE_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))


pygame.font.init()
FONT_POINTS = pygame.font.SysFont('arial', 50)


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
    birds = [cbird.Bird(230, 350)]
    floor = cfloor.Floor(730)
    pipes = [cpipe.Pipe(700)]
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
                    # ao colidir ele encerra o jogo
                    running = False

                if not pipe.pass_bird and bird.x > pipe.x:
                    pipe.pass_bird = True
                    pipe_add = True
            pipe.move()

            if pipe.x + pipe.UP_PIPE_IMG.get_width() < 0:
                pipes_remove.append(pipe)

        if pipe_add:
            points += 1
            pipes.append(cpipe.Pipe(600))

        for pipe in pipes_remove:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
                # ao bater no chão ou sair da tela, encerra o jogo
                running = False

        draw_screen(screen, birds, pipes, floor, points)


if __name__ == '__main__':
    main()
