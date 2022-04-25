from constants import *
from Shuttle import Shuttle
from Alien import Alien
import pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

#? ------------------- initialize objects -------------------
shuttle = Shuttle("Apollo13", 100, INITIAL_SHUTTLE_POSITION)
alien = Alien("Yoda", INITIAL_ALIEN_POSITION)
alien.set_rect()
r1 = pygame.Rect(400, 200, 80, 80)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

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

    #? ------------------------ collisions --------------------------
    shuttle.collision(alien)
    print(shuttle.get_hit())
    if shuttle.get_hit():
        shuttle.set_position(INITIAL_SHUTTLE_POSITION)
        shuttle.set_hit(False)

    #? --------------------- drawing objects ---------------------------
    shuttle.draw_shuttle(screen)
    alien.draw_alien(screen)
    #print(f"position {shuttle.get_position()}")
    #print(f"rect {shuttle.get_rect()}")

    keys=pygame.key.get_pressed()

    pygame.display.flip()

pygame.quit()