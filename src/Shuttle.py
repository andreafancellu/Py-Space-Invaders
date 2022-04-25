from constants import *
from Bullet import Bullet
import pygame

from constants import INITIAL_SHUTTLE_POSITION

class Shuttle:
    
    def __init__(self, name, hp, position):
        self.name = name
        self.hp = hp
        self.is_dead = False
        self.position = position
        self.texture = pygame.image.load("/home/andrea/Projects/Py-Space-Invaders/data/shuttle.png").convert()
        self.rect = self.texture.get_rect()
        self.score = 0
        self.shot = False
        self.hit = True 

    #* getters and setters
    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_is_dead(self):
        return self.is_dead

    def get_position(self):
        return self.position

    def get_rect(self):
        return self.rect

    def get_score(self):
        return self.score

    def get_shot(self):
        return self.shot

    def get_hit(self):
        return self.hit

    def set_hp(self, hp):
        self.hp = hp

    def set_is_dead(self, is_dead):
        self.is_dead = is_dead

    def set_position(self, position):
        self.position = position

    def set_score(self, score):
        self.score = score

    def set_shot(self, shot):
        self.shot = shot

    def set_hit(self, hit):
        self.hit = hit

    #* in-game functions
    def move_left(self):
        self.position[0] -= 0.5
        if self.position[0] < 0:
            self.position[0] = 0
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)

    def move_right(self):
        self.position[0] += 0.5
        if self.position[0] > 760:
            self.position[0] = 760
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)

    def move_up(self):
        self.position[1] -= 1
        if self.position[1] < 0:
            self.position[1] = 0
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)

    def move_down(self):
        self.position[1] += 1
        if self.position[1] > 660:
            self.position[1] = 660
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)

    def die(self):
        self.is_dead = True
        print(f"{self.name} has died")

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()
        else:
            print(f"{self.name} has taken {damage} damage, now has {self.hp} hp")
        #self.draw_shuttle(screen)   

    def collision(self, obstacle):
        if self.rect.colliderect(obstacle.get_rect()):
            print(f"{self.name} has collided with {obstacle.get_name()}")
            self.take_damage(10)

    def draw_shuttle(self, screen):
        screen.blit(self.texture, self.position)
    
    def shoot(self):
        self.shot = True

    def __str__(self):
        return f"the shuttle named {self.name} has {self.hp}"