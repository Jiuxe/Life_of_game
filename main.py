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

# Generar moviles
for num_mov in range(0,10):
    pivot = random.randint(0,50)
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

            n_neigh =   gameState[(x - 1)   % nxC, (y - 1)  % nyC] + \
                        gameState[(x)       % nxC, (y - 1)  % nyC] + \
                        gameState[(x + 1)   % nxC, (y - 1)  % nyC] + \
                        gameState[(x - 1)   % nxC, (y)      % nyC] + \
                        gameState[(x + 1)   % nxC, (y)      % nyC] + \
                        gameState[(x - 1)   % nxC, (y + 1)  % nyC] + \
                        gameState[(x)       % nxC, (y + 1)  % nyC] + \
                        gameState[(x + 1)   % nxC, (y + 1)  % nyC]

            # Regla 1 : Una celula muerta con 3 vecinas vivas, "revive"
            if gameState[x, y] == 0 and n_neigh == 3:
                newGameState[x,y] = 1

            # Regla 2 : Una celula viva con menos de 2 o mas de 3 vecinas vivas, "muere"
            elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                newGameState[x, y] = 0


            poly = [((x) * dimCW, y * dimCH),
                   ((x+1) * dimCW, y * dimCH),
                   ((x+1) * dimCW, (y+1) * dimCH),
                   ((x) * dimCW, (y+1) * dimCH)]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen,(128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen,(255, 255, 255), poly, 0)

    gameState = np.copy(newGameState)

    pygame.display.flip()

"""
if __name__ == '__main__':
"""

