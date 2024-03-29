from random import random
from constants import *
from Shuttle import Shuttle
from Bullet import Bullet
from Alien import Alien
from Boss import Boss
import pygame
import time
import random

pygame.init()

#? ----------------------- Initialize Variables -------------------------------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("data/background.png")
pygame.display.set_caption('Py-Space-Invaders')

#? ----------------------- Initialize Texts -----------------------------------
font_game_over = pygame.font.SysFont("uroob", 180)
font_text = pygame.font.SysFont("uroob", 30)

#? ----------------------- Initialize Game-Objects ----------------------------
shuttle = Shuttle("Apollo13", 100, INITIAL_SHUTTLE_POSITION)
bullet = Bullet([shuttle.get_position()[0]+20, shuttle.get_position()[1]-10])
boss = Boss("Alienoooo", 100, [SCREEN_WIDTH/2, SCREEN_HEIGHT-600])
left, right = True, False # used for Aliens movement

aliens = []
for i in range(31):
    if i <= 10:
        aliens.append(Alien(f"Alien {i}", [SCREEN_WIDTH-77*i, SCREEN_HEIGHT-650]))
    if 11 <= i <= 20:
        aliens.append(Alien(f"Alien {i}", [SCREEN_WIDTH-77*(i-10), SCREEN_HEIGHT-500]))
    if 21 <= i <= 30:
        aliens.append(Alien(f"Alien {i}", [SCREEN_WIDTH-77*(i-20), SCREEN_HEIGHT-350]))
    

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
        shuttle.shoot()

    if keys[pygame.K_ESCAPE]:
        running = False

    #? ----------------------- Drawing Game-Objects ---------------------------
    screen.blit(bg, (0,0))
    shuttle.draw_shuttle(screen)
    for alien in aliens:
        alien.draw_alien(screen)
    boss.draw_boss(screen)

    #? ----------------------- Aliens Movements ----------------------------
    rand = random.randint(0,1)

    for alien in aliens:
        alien.move_down()

    for alien in aliens:

        if left:
            alien.move_left()
            if alien.get_position()[0] <= 0:
                right = True
                left = False
                
        if right:
            alien.move_right()
            if alien.get_position()[0] >= SCREEN_WIDTH+30:
                left = True
                right = False

    #? ----------------------- Shooting ----------------------------
    if shuttle.get_shot():
        bullet.move_bullet()
        bullet.draw_bullet(screen) 

    if not(shuttle.get_shot()):
        bullet.set_pos([shuttle.get_position()[0]+20, shuttle.get_position()[1]-10])

    if bullet.get_pos()[1] < 0:
        shuttle.set_shot(False)

    #? ----------------------- Collisions -------------------------------------
    end = time.time()
    if (end - start) > 0.2:
        for alien in aliens:
            shuttle.collision(alien)
            start = time.time()
            end = 0
    
    for alien in aliens:
        if bullet.collision(alien):
            alien.die()
            shuttle.set_shot(False)
            shuttle.score_up()

    '''if (end - start) > 0.1:
        alien.collision(bullet)'''

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
    score_text = font_text.render("score: ", True, (255, 255, 255))
    score = font_text.render(f"{shuttle.get_score()}", True, (0, 0, 255))
    screen.blit(score_text, (SCREEN_WIDTH-90, 10))
    screen.blit(score, (SCREEN_WIDTH-20, 10))

    #? ----------------------- Win  -------------------------------------------as
    if (len(aliens) - 1) == shuttle.get_score():
        print("You Win!")
        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        shuttle.draw_shuttle(screen)
        text = font_game_over.render("You Win!!!", True, (255,255,255))
        screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
        score_text = font_text.render("Final Score: ", True, (255, 255, 255))
        score = font_text.render(f"{shuttle.get_score() * shuttle.get_hp()}", True, (0, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH-480, 500))
        screen.blit(score, (SCREEN_WIDTH-370, 500))
        
    #? ----------------------- Game Over --------------------------------------
    if shuttle.get_is_dead():
        print("Game Over")
        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        text = font_game_over.render("Game Over :(", True, (255,255,255))
        screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
        
    pygame.display.flip()
    

pygame.quit()