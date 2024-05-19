import pygame
import sys
from grid import Grid

pygame.init()
color_of_background = (61, 173, 29)


screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("super tetriz merito edition")


clock = pygame.time.Clock()

game_grid = Grid()
game_grid.print_grid()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #kolor tła okna z grą
    screen.fill(color_of_background)
    pygame.display.update()
    clock.tick(60)
