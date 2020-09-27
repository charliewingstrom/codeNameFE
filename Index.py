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
from Game import Game
screenWidth = 1080
screenHeight = 720

window = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("codeFE")

unitArray = []        
map1 = Map(window, screenWidth, screenHeight)

robin = Unit(window)
map1.addUnit(robin, 1, 1)
unitArray.append(robin)

startGame = Game(window, map1)


run = True
while run:
    
    pygame.time.delay(100)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_LEFT] and startGame.cursor.pos[1] > 0:
        startGame.selectLeft()
    if keys[pygame.K_RIGHT] and startGame.cursor.pos[1] < startGame.currentMap.width-1:
        startGame.selectRight()
    if keys[pygame.K_UP] and startGame.cursor.pos[0] > 0:
        startGame.selectUp()
    if keys[pygame.K_DOWN] and startGame.cursor.pos[0] < startGame.currentMap.height-1:
        startGame.selectDown()
    if keys[pygame.K_z] and not startGame.cursor.unitSelected:
        startGame.selectUnit()
    elif keys[pygame.K_z] and startGame.cursor.unitSelected:
        startGame.placeUnit()
    if keys[pygame.K_x] and startGame.cursor.unitSelected:
        startGame.resetSelectedUnit()
    if keys[pygame.K_s]:
        startGame.currentMap.scrollDown()
    if keys[pygame.K_w]:
        startGame.currentMap.scrollUp()
    if keys[pygame.K_a]:
        startGame.currentMap.scrollLeft()
    if keys[pygame.K_d]:
        startGame.currentMap.scrollRight()
    
    window.fill((0,0,0))
    
    startGame.draw()
    for unit in unitArray:
        unit.draw()
    pygame.display.update()
    
        
        
        
pygame.quit()