import pygame
from car import Car
import math
import numpy as np
from track_types import *
from agent import *

pygame.init()

WIDTH = 600
HEIGHT = 700
CELL_SIZE = 100
screen = pygame.display.set_mode([WIDTH, HEIGHT])

track_key = np.array([
    [0, 0, 0, 0, 0, 0],
    [6, 5, 6, 1, 1, 5],
    [2, 2, 4, 1, 5, 2],
    [2, 4, 1, 1, 3, 2],
    [2, 6, 1, 5, 6, 3],
    [2, 4, 5, 2, 4, 5],
    [4, 1, 3, 4, 1, 3],
])
TRACK = create_track(track_key, WIDTH, HEIGHT, CELL_SIZE)
TRACK_MASK = create_track(track_key, WIDTH, HEIGHT, CELL_SIZE, mask=True)
TRACK_MASK.set_colorkey((0, 0, 0))
TRACK_MASK = pygame.mask.from_surface(TRACK_MASK)

START_CELL = (0, 2)
END_CELL = (0, 1)
TRACK_CHECKPOINTS = get_track_checkpoints(track_key, START_CELL, END_CELL)

NUM_AGENTS = 10
agents = []
for i in range(NUM_AGENTS):
    agents.append(Agent(TRACK_MASK, TRACK_CHECKPOINTS, 50 + START_CELL[0] * 100, 50 + START_CELL[1] * 100, car_heading=math.pi/2))

MAX_STEPS = 2000
generation = 0
step = 0
running = True
highest_fitness = -999999999
while running:
    for step in range(MAX_STEPS):
        if step % 20 == 0:
            print('step', step, '/', MAX_STEPS)

        # check for events
        for event in pygame.event.get():
            # exit if X is pressed
            if event.type == pygame.QUIT:
                running = False
        
        # draw background
        screen.fill((255, 255, 0))
        # draw track
        screen.blit(TRACK, (0, 0))

        # step agents
        num_agents_alive = 0
        best_fitness = -999999999
        for agent in agents:
            agent.step(draw=True, screen=screen)
            if not agent.failed and not agent.completed:
                num_agents_alive += 1
            if agent.fitness > best_fitness:
                best_fitness = agent.fitness
        if best_fitness > highest_fitness:
            highest_fitness = best_fitness

        # display number of agents alive
        FONT_SIZE = 18
        font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
        text = font.render('Agents alive: ' + str(num_agents_alive) + ' / ' + str(NUM_AGENTS), False, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (5, 5)
        screen.blit(text, text_rect)

        # display generation
        text = font.render('Generation: ' + str(generation), False, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (5, 5 + FONT_SIZE + 5)
        screen.blit(text, text_rect)

        # display highest fitness of current generation
        text = font.render('Generation highest fitness: ' + str(best_fitness), False, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (5, 5 + 2 * (FONT_SIZE + 5))
        screen.blit(text, text_rect)

        # display highest fitness overall
        text = font.render('Overall highest fitness: ' + str(highest_fitness), False, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (5, 5 + 3 * (FONT_SIZE + 5))
        screen.blit(text, text_rect)

        # display screen and keep FPS constant
        pygame.display.flip()

        if num_agents_alive == 0:
            break

    for agent in agents:
        if agent.completed:
            print(agent.network.network)
    
    agents = create_offspring(agents, 50 + START_CELL[0] * 50, 50 + START_CELL[1] * 50, math.pi/2)
    generation += 1

pygame.quit()