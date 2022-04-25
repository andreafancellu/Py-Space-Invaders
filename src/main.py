from constants import *
from Shuttle import Shuttle
from Alien import Alien
import pygame
import time

pygame.init()

#? ----------------------- Initialize Variables -------------------------------
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("/home/andrea/Projects/Py-Space-Invaders/data/background.png")

#? ----------------------- Initialize Texts -----------------------------------
font_game_over = pygame.font.SysFont("uroob", 200)
font_text = pygame.font.SysFont("uroob", 30)

#? ----------------------- Initialize Game-Objects ----------------------------
shuttle = Shuttle("Apollo13", 100, INITIAL_SHUTTLE_POSITION)
alien = Alien("Yoda", INITIAL_ALIEN_POSITION)

running = True
start = time.time()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    #? ---------------------- Keys Detection ----------------------------------
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

    if keys[pygame.K_ESCAPE]:
        running = False

    #? ----------------------- Drawing Game-Objects ---------------------------
    screen.blit(bg, (0,0))
    shuttle.draw_shuttle(screen)
    alien.draw_alien(screen)

    #? ----------------------- Collisions -------------------------------------
    end = time.time()
    if (end - start) > 0.2:
        shuttle.collision(alien, screen)
        start = time.time()
        end = 0

    #? ----------------------- HP-Text ----------------------------------------
    if shuttle.get_hp() >= 70: 
        color_hp = (0, 255, 0)
    elif 40 <= shuttle.get_hp() <= 60:
        color_hp = (255, 255, 0)
    elif shuttle.get_hp() <= 30:
        color_hp = (255, 0, 0)
    hp_text = font_text.render("hp: ", True, (255, 255, 255))
    hp = font_text.render(f"{shuttle.get_hp()}", True, color_hp)
    screen.blit(hp_text, (10, 10))
    screen.blit(hp, (45, 10))

    #? ----------------------- Score-Text -------------------------------------
    score_text = font_text.render("Score: ", True, (255, 255, 255))
    score = font_text.render(f"{shuttle.get_score()}", True, (0, 0, 255))
    screen.blit(score_text, (SCREEN_WIDTH-90, 10))
    screen.blit(score, (SCREEN_WIDTH-20, 10))

    #? ----------------------- Game Over --------------------------------------
    if shuttle.get_is_dead():
        print("Game Over")
        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        text = font_game_over.render("Game Over", True, (255,255,255))
        screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
        


    

    #clock.tick(FPS)
    pygame.display.flip()
    

pygame.quit()