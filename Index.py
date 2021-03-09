# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 22:03:13 2020

@author: Charlie
"""
import sys
sys.path.append('./Units')
sys.path.append('./weapons')
sys.path.append('./consumables')
import pygame

from Game import Game
from Map import Map

from PlayerUnit import PlayerUnit
from EnemyUnit import EnemyUnit

from sword import sword
from javelin import javelin
from weapon import weapon
from estus import Estus


screenWidth = 1500
screenHeight = 1000
green = (0, 255, 0)
grey = (192,190,194)
window = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("codeFE")

map1 = Map(window, screenWidth, screenHeight)

unitArray = []    
robin = PlayerUnit(window, "Robin")
map1.addUnit(robin, 1, 1)
unitArray.append(robin)
Byleth = PlayerUnit(window, "Byleth")
Byleth.weapons.append(javelin())
map1.addUnit(Byleth, 2, 2)
unitArray.append(Byleth)

for unit in unitArray: unit.weapons.append(sword())

enemyArray = []   
Bandit = EnemyUnit(window, "Pirate")
map1.addUnit(Bandit, 1, 10)
enemyArray.append(Bandit)
Bandit2 = EnemyUnit(window, "Bandit")
map1.addUnit(Bandit2, 2, 10)
enemyArray.append(Bandit2)
Bandit3 = EnemyUnit(window, "Knight")
map1.addUnit(Bandit3, 0, 10)
enemyArray.append(Bandit3)

for enemy in enemyArray: enemy.weapons.append(sword())

for unit in unitArray:
    print(str(unit) + " holds a " + str(unit.weapons[0]))
    unit.inventory.append(Estus())

for i in range(6):
    map1.Tiles[i][4].walkable = False
    map1.Tiles[i][4].defaultBorderColor = grey
    map1.Tiles[i][4].setColor(grey)

for i in range(5, 10):
    map1.Tiles[5][i].walkable = False
    map1.Tiles[5][i].defaultBorderColor = grey
    map1.Tiles[5][i].setColor(grey)

for i in range(5, 10):
    map1.Tiles[7][i].walkable = False
    map1.Tiles[7][i].defaultBorderColor = grey
    map1.Tiles[7][i].setColor(grey)

for i in range(7, 20):
    map1.Tiles[i][4].walkable = False
    map1.Tiles[i][4].defaultBorderColor = grey
    map1.Tiles[i][4].setColor(grey)
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
            if startGame.inventoryOpen:
                if pygame.K_z == key:
                    tmp = False
                    if (startGame.inventory.itemSelected):
                        tmp = True
                    startGame.inventory.selectOption()
                    if tmp:
                        startGame.cleanupAfterAction()
                if pygame.K_LEFT == key or pygame.K_RIGHT == key:
                    startGame.inventory.toggleWeaponsOrInv()
            elif startGame.attacking:
                if pygame.K_LEFT == key or pygame.K_RIGHT == key:
                    startGame.combat.changeAttackTarget()
                elif pygame.K_DOWN == key:
                    startGame.combat.changeEquippedWeaponCurrentUnit(1)
                elif pygame.K_UP == key:
                    startGame.combat.changeEquippedWeaponCurrentUnit(0)
                elif pygame.K_z == key:
                    startGame.attack()
            elif startGame.unitIsPlaced:
                if pygame.K_z == key:
                    startGame.selectMenuOption()
            elif not startGame.unitIsPlaced:
                if pygame.K_z == key and startGame.unitSelected:
                    startGame.placeUnit()
                elif pygame.K_z == key and not startGame.unitSelected:
                    startGame.selectUnit()
    ## if you do want a held key to repeat the action (such as scrolling a list) put the key here
    if startGame.inventoryOpen:
        if keys[pygame.K_UP]:
            startGame.inventory.highlightUp()
        if keys[pygame.K_DOWN]:
            startGame.inventory.highlightDown()
    if startGame.unitIsPlaced:
        if keys[pygame.K_UP]:
            startGame.actionMenu.highlightUp()
        if keys[pygame.K_DOWN]:
            startGame.actionMenu.highlightDown()
    else:
        if keys[pygame.K_LEFT] and startGame.cursor.pos[1] > 0:
            startGame.moveCursor("left")
        if keys[pygame.K_RIGHT] and startGame.cursor.pos[1] < startGame.currentMap.width-1:
            startGame.moveCursor("right")
        if keys[pygame.K_UP] and startGame.cursor.pos[0] > 0:
            startGame.moveCursor("up")
        if keys[pygame.K_DOWN] and startGame.cursor.pos[0] < startGame.currentMap.height-1:
            startGame.moveCursor("down")
        
        
    
    if keys[pygame.K_x] and startGame.unitSelected:
        startGame.resetSelectedUnit()
    

    window.fill((0,0,0))
    
    startGame.draw()
    pygame.display.update()
    
    pygame.time.delay(60)
        
        
pygame.quit()