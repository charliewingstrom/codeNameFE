# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 22:03:13 2020

@author: Charlie
"""
import sys
sys.path.append('./Units')

import pygame
import math
import random
from Map import Map
from PlayerUnit import PlayerUnit
from EnemyUnit import EnemyUnit
from Game import Game
screenWidth = 1080
screenHeight = 720
green = (0, 255, 0)
window = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("codeFE")

map1 = Map(window, screenWidth, screenHeight)

unitArray = []    
robin = PlayerUnit(window, "Robin")
map1.addUnit(robin, 1, 1)
unitArray.append(robin)
Byleth = PlayerUnit(window, "Byleth")
map1.addUnit(Byleth, 2, 2)
unitArray.append(Byleth)

enemyArray = []   
Bandit = EnemyUnit(window)
map1.addUnit(Bandit, 1, 4)
enemyArray.append(Bandit)
Bandit2 = EnemyUnit(window)
map1.addUnit(Bandit2, 2, 5)
enemyArray.append(Bandit2)
Bandit3 = EnemyUnit(window)
map1.addUnit(Bandit3, 0, 3)
enemyArray.append(Bandit3)

map1.Tiles[3][1].defaultBorderColor = green
map1.Tiles[3][1].movPenalty = 2
map1.Tiles[2][1].movPenalty = 2
startGame = Game(window, map1, unitArray, enemyArray)
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
            startGame.actionMenu.highlightUp()
        if keys[pygame.K_DOWN]:
            startGame.actionMenu.highlightDown()
    elif not startGame.unitIsPlaced:
        if keys[pygame.K_LEFT] and startGame.cursor.pos[1] > 0:
            startGame.moveCursor("left")
        if keys[pygame.K_RIGHT] and startGame.cursor.pos[1] < startGame.currentMap.width-1:
            startGame.moveCursor("right")
        if keys[pygame.K_UP] and startGame.cursor.pos[0] > 0:
            startGame.moveCursor("up")
        if keys[pygame.K_DOWN] and startGame.cursor.pos[0] < startGame.currentMap.height-1:
            startGame.moveCursor("down")
        
        
    
    if keys[pygame.K_x] and startGame.cursor.unitSelected:
        startGame.resetSelectedUnit()
    

    window.fill((0,0,0))
    
    startGame.draw()
    pygame.display.update()
    
    pygame.time.delay(60)
        
        
pygame.quit()