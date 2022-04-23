from constants import *
from classes.Shuttle import Shuttle
import pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    pygame.draw.circle(screen, (0, 0, 255), INITIAL_SHUTTLE_POSITION, 20)
    apollo13 = Shuttle("Apollo13", 100, INITIAL_SHUTTLE_POSITION)
    apollo13.draw_shuttle(screen)
    apollo13.move_left()
    apollo13.draw_shuttle(screen)

    pygame.display.flip()

pygame.quit()