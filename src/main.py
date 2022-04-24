from constants import *
from Shuttle import Shuttle
import pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    #? ------------------- initialize objects -------------------
    shuttle = Shuttle("Shuttle", 100, INITIAL_SHUTTLE_POSITION)

    #? -------------------- keys detection ---------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        shuttle.move_left()

    if keys[pygame.K_d]:
        shuttle.move_right()

    if keys[pygame.K_w]:
        shuttle.move_up()
    
    if keys[pygame.K_s]:
        shuttle.move_down()

    if keys[pygame.K_SPACE]:
        shuttle.shoot(screen, shuttle.get_position())

    #? --------------------- drawing objects ---------------------------
    shuttle.draw_shuttle(screen)

    keys=pygame.key.get_pressed()

    pygame.display.flip()

pygame.quit()