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
from EnemyUnit import EnemyUnit
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

Bandit = EnemyUnit(window)
map1.addUnit(Bandit, 1, 4)
unitArray.append(Bandit)
startGame = Game(window, map1)
run = True
while run:
    
    pygame.time.delay(60)
    keys = pygame.key.get_pressed()
    
    ## put key here if you don't want a held key to repeat the action
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if startGame.unitIsPlaced:
                if pygame.K_z == key:
                    startGame.selectMenuOption()
            elif not startGame.unitIsPlaced:
                if pygame.K_z == key and startGame.cursor.unitSelected:
                    startGame.placeUnit()
                elif pygame.K_z == key and not startGame.cursor.unitSelected:
                    startGame.selectUnit()
    ## if you do want a held key to repeat the action (such as scrolling a list) put the key here
    if startGame.unitIsPlaced:
        if keys[pygame.K_UP]:
            startGame.menu.highlightUp()
        if keys[pygame.K_DOWN]:
            startGame.menu.highlightDown()
    elif not startGame.unitIsPlaced:
        if keys[pygame.K_LEFT] and startGame.cursor.pos[1] > 0:
            startGame.selectLeft()
        if keys[pygame.K_RIGHT] and startGame.cursor.pos[1] < startGame.currentMap.width-1:
            startGame.selectRight()
        if keys[pygame.K_UP] and startGame.cursor.pos[0] > 0:
            startGame.selectUp()
        if keys[pygame.K_DOWN] and startGame.cursor.pos[0] < startGame.currentMap.height-1:
            startGame.selectDown()
        
        
    
    if keys[pygame.K_x] and startGame.cursor.unitSelected:
        startGame.resetSelectedUnit()
    

    window.fill((0,0,0))
    
    startGame.draw()
    for unit in unitArray:
        unit.draw()
    pygame.display.update()
    
    pygame.time.delay(60)
        
        
pygame.quit()