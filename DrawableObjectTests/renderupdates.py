import pygame
from pygame.locals import *
from boxes import UpDownBox
from time import time

pygame.init()
boxes = pygame.sprite.RenderUpdates()
for color, location in [([255, 0, 0], [0, 0]),
		        ([0, 255, 0], [0, 60]),
                        ([0, 0, 255], [0, 120])]:
    boxes.add(UpDownBox(color, location))

screen = pygame.display.set_mode([150, 150])
background = pygame.image.load("Room.gif")
#background.fill(pygame.image.load("Room.gif"))
screen.blit(background, [0, 0])
pygame.display.flip()
start = time()
for i in range(500):
    boxes.update(pygame.time.get_ticks(), 150)
    rectlist = boxes.draw(screen)
    pygame.display.update(rectlist)
    #pygame.time.delay(10)
    boxes.clear(screen, background)
    
print 500/(time() - start)
