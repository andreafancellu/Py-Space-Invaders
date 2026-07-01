from constants import *
import pygame


class Shuttle:
    def __init__(self, name, hp, position, speed):
        self.name = name
        self.hp = hp
        self.is_dead = False
        self.position = list(position)
        self.speed = speed
        self.texture = pygame.image.load(asset_path("shuttle.png")).convert_alpha()
        self.rect = self.texture.get_rect()
        self.update_rect()
        self.score = 0
        self.shot = False
        self.hit = True

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
        self.position = list(position)
        self.update_rect()

    def set_score(self, score):
        self.score = score

    def set_shot(self, shot):
        self.shot = shot

    def set_hit(self, hit):
        self.hit = hit

    def update_rect(self):
        self.rect.topleft = (round(self.position[0]), round(self.position[1]))

    def move(self, dx, dy, dt):
        self.position[0] += dx * self.speed * dt
        self.position[1] += dy * self.speed * dt
        self.position[0] = max(0, min(SCREEN_WIDTH - self.rect.width, self.position[0]))
        self.position[1] = max(0, min(SCREEN_HEIGHT - self.rect.height, self.position[1]))
        self.update_rect()

    def die(self):
        self.is_dead = True
        print(f"{self.name} has died")

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()
        else:
            print(f"{self.name} has taken {damage} damage, now has {self.hp} hp")

    def collision(self, obstacle):
        if not obstacle.get_is_dead() and self.rect.colliderect(obstacle.get_rect()):
            print(f"{self.name} has collided with {obstacle.get_name()}")
            self.take_damage(10)

    def draw_shuttle(self, screen):
        screen.blit(self.texture, self.position)
    
    def shoot(self):
        if not self.shot:
            self.shot = True

    def score_up(self):
        self.score += 1
    
    def score_down(self):
        self.score -= 1

    def __str__(self):
        return f"the shuttle named {self.name} has {self.hp}"
