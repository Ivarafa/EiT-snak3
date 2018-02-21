__author__ = 'Ivar A. Fauske'
# This Python file uses the following encoding: utf-8

import sys, pygame, Simulation
import numpy as np
pygame.init()
done = False
size = width, height = 1500, 600
screen = pygame.display.set_mode(size)
background = [0,0,0]
snake = Simulation.Snake(7).make()  #fix this to make proper snake

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            done = True

    snake.move()    #here to update snake
    #c = [(x+1)%256 for x in c]
    screen.fill(background)
    #start_pos = np.matrix([[300],[300]]) - snake.get_cm()
    start_pos = snake.get_pos() - snake.get_cm()
    pygame.draw.circle(screen,(255,0,0,255),start_pos,2)
    for i in range(0, snake.get_size()):
        stop_pos = start_pos + snake.links[i].get_displacement()
        pygame.draw.line(screen, (255,0,0,255),start_pos,stop_pos,2)
        pygame.draw.circle(screen,(255,0,0,255),stop_pos,2)
        start_pos = stop_pos
    start_pos = snake.get_pos() - snake.get_cm()
    pygame.draw.circle(screen,(255,0,0,255),start_pos,2)
    XY = snake.big_XY()
    XY_dot = snake.big_XY_dot()
    for i in range(0, snake.get_size()):
        stop_pos = np.matrix([[XY[0,i]],[XY[1,i]]]) - snake.get_cm() + snake.get_pos()
        pygame.draw.line(screen, (0,255,0,255),stop_pos,stop_pos + np.matrix([[XY_dot[0,i]],[XY_dot[1,i]]]),2)
        pygame.draw.circle(screen,(0,0,255,255),stop_pos,2)
        start_pos = stop_pos
    pygame.display.flip()
pygame.quit()