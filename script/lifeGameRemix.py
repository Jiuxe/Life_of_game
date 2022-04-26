import pygame
import numpy as np
import  time
import random

pygame.init()

width, height = 1000, 1000

screen = pygame.display.set_mode((height, width))

bg = 25,25,25
screen.fill(bg)

nxC,nyC = 50, 50

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))

n_neigh_good = 0
n_neigh_bad = 0
n_neigh_killer = 0

# Generar moviles
for num_mov in range(0,40):
    pivot = random.randint(2,48)
    gameState[pivot - 1,    pivot]      = 1
    gameState[pivot,        pivot + 1]  = 1
    gameState[pivot + 1,    pivot - 1]  = 1
    gameState[pivot + 1,    pivot]      = 1
    gameState[pivot + 1,    pivot + 1] = 1

while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    for y in range(0,nxC):
        for x in range(0,nyC):

            if gameState[x,y] == 3 or gameState[x,y] == 4:
                n_neigh_good = 0
                n_neigh_bad = 0
                n_neigh_killer = 0
                for i in range(-1,1):
                    for j in range(-1,1):
                        if not (i == 0 and j == 0):
                            if gameState[(x + i) % nxC, (y + j) % nyC] == 3:
                                n_neigh_good += 1
                            elif gameState[(x + i) % nxC, (y + j) % nyC] == 4:
                                n_neigh_bad += 1
                            elif gameState[(x + i) % nxC, (y + j) % nyC] == 6:
                                n_neigh_killer += 1

            n_neigh = (gameState[(x - 1) % nxC, (y - 1) % nyC]) % 2 + \
                      (gameState[(x) % nxC, (y - 1) % nyC]) % 2 + \
                      (gameState[(x + 1) % nxC, (y - 1) % nyC]) % 2 + \
                      (gameState[(x - 1) % nxC, (y) % nyC]) % 2 + \
                      (gameState[(x + 1) % nxC, (y) % nyC]) % 2 + \
                      (gameState[(x - 1) % nxC, (y + 1) % nyC]) % 2 + \
                      (gameState[(x) % nxC, (y + 1) % nyC]) % 2 + \
                      (gameState[(x + 1) % nxC, (y + 1) % nyC]) % 2

            # Regla 1 : Una celula muerta con 3 vecinas vivas, "revive"
            if gameState[x, y] == 0 and n_neigh == 3:
                newGameState[x, y] = 1

            # Regla 2 : Una celula viva con menos de 2 o mas de 3 vecinas vivas, "muere"
            elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                newGameState[x, y] = 0

            # Regla 3: Una celula viva con 5 vecinos vivos, nace como una celula buena o mala
            if gameState[x, y] == 1 and n_neigh == 5:
                newGameState[x, y] = random.choice([3, 4])

            # Regla 4: Una celula buena vecina de 2 o mas celulas malas, muere
            if gameState[x, y] == 3 and n_neigh_bad > 2:
                newGameState[x, y] = 0

            # Regla 5: Una celula mala vecina de una celula mala puede morir o convertirse en asesina
            if gameState[x, y] == 4 and n_neigh_bad > 1:
                newGameState[x, y] = random.choice([0, 6])

            # Regla 6: Una celula nacida vecina de una celula asesina, muere
            if gameState[x,y] == 3 and n_neigh_killer != 0:
                newGameState[x, y] = 0

            poly = [((x) * dimCW, y * dimCH),
                   ((x+1) * dimCW, y * dimCH),
                   ((x+1) * dimCW, (y+1) * dimCH),
                   ((x) * dimCW, (y+1) * dimCH)]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen,(128, 128, 128), poly, 1)
            elif newGameState[x, y] == 3:
                pygame.draw.polygon(screen,(0, 255, 0), poly, 0)
            elif newGameState[x, y] == 4:
                pygame.draw.polygon(screen,(255, 0, 0), poly, 0)
            elif newGameState[x, y] == 6:
                pygame.draw.polygon(screen,(0, 0, 255), poly, 0)
            else:
                pygame.draw.polygon(screen,(255, 255, 255), poly, 0)

    gameState = np.copy(newGameState)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()