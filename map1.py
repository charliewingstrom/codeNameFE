# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 22:03:13 2020

@author: Charlie
"""

import pygame
import math
import random
from Map import Map
from Unit import Unit
screenWidth = 1080
screenHeight = 1080

window = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("codeFE")

UnitArray = []        
map1 = Map(window)

robin = Unit(window)
map1.addUnit(robin, 1, 1)

UnitArray.append(robin)
run = True
while run:
    
    pygame.time.delay(90)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_LEFT] and map1.cursor[1] > 0:
        map1.selectLeft()
    if keys[pygame.K_RIGHT] and map1.cursor[1] < map1.width-1:
        map1.selectRight()
    if keys[pygame.K_UP] and map1.cursor[0] > 0:
        map1.selectUp()
    if keys[pygame.K_DOWN] and map1.cursor[0] < map1.height-1:
        map1.selectDown()
    window.fill((0,0,0))
    
    map1.draw()
    for unit in unitArray:
        unit.draw()
    pygame.display.update()
    
        
        
        
pygame.quit()