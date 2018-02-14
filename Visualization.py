__author__ = 'Ivar A. Fauske'
# This Python file uses the following encoding: utf-8

import sys

import pygame

import Simulation

pygame.init()
done = False
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
background = [0,0,0]

snake = Simulation.Snake().make_random(9)  #fix this to make proper snake

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            done = True

    snake.move()    #here to update snake
    #c = [(x+1)%256 for x in c]
    screen.fill(background)
    for i in range(snake.get_size()-1):
        surf = pygame.Surface((10,10),flags=pygame.SRCALPHA)
        surf.fill((255,0,0,255))
        surf = pygame.transform.rotate(surf,snake.joints[i].rotation)
        screen.blit(surf,(snake.joints[i].pos[0],snake.joints[i].pos[1]))
        pygame.draw.circle(screen,[255,0,0],(snake.links[i].pos[0],snake.links[i].pos[1]),2)
    surf = pygame.Surface((10,10),flags=pygame.SRCALPHA)
    surf.fill((255,0,0,255))
    surf = pygame.transform.rotate(surf,snake.joints[-1].rotation)
    screen.blit(surf,(snake.joints[-1].pos[0],snake.joints[-1].pos[1]))

    pygame.display.flip()


pygame.quit()