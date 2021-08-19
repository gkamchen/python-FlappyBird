import os

import neat
import pygame

import bird as cbird
import floor as cfloor
import pipe as cpipe

ai_playing = True
generation = 0

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

    if ai_playing:
        text = FONT_POINTS.render(f"Geração: {generation}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    floor.draw(screen)
    pygame.display.update()


def main(genomes, config):  # fitness function
    global generation
    generation += 1

    if ai_playing:
        # criar vários pássaros
        networks = []
        list_genomes = []
        birds = []

        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)
            genome.fitness = 0
            list_genomes.append(genome)
            birds.append(cbird.Bird(230, 350))
    else:
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

            if not ai_playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()

        index_pipe = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].UP_PIPE_IMG.get_width()):
                index_pipe = 1
        else:
            running = False
            break

        # mover os pássaros no jogo
        for i, bird in enumerate(birds):
            bird.move()
            # aumentar um pouco o fitness
            list_genomes[i].fitness += 0.1
            output = networks[i].activate((bird.y,
                                           abs(bird.y - pipes[index_pipe].height),
                                           abs(bird.y - pipes[index_pipe].down_pos)))

            if output[0] > 0.5:
                bird.jump()

        # mover o chão
        floor.move()

        # mover os canos
        pipe_add = False
        pipes_remove = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)

                    if ai_playing:
                        list_genomes[i].fitness -= 1
                        list_genomes.pop(i)
                        networks.pop(i)
                    else:
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

            for genome in list_genomes:
                genome.fitness += 5

        for pipe in pipes_remove:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
                if ai_playing:
                    list_genomes.pop(i)
                    networks.pop(i)
                else:
                    # ao bater no chão ou sair da tela, encerra o jogo
                    running = False

        draw_screen(screen, birds, pipes, floor, points)


def working(path_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                path_config)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if ai_playing:
        population.run(main, 50)
    else:
        main(None, None)


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    path_config = os.path.join(path, 'config.txt')
    working(path_config)
