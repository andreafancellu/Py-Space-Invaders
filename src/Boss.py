import pygame

from constants import SCREEN_WIDTH, asset_path


class Boss:
    def __init__(self, name, hp, position, speed, texture_filename="boss.png"):
        self.name = name
        self.hp = hp
        self.is_dead = False
        self.position = list(position)
        self.speed = speed
        self.texture = pygame.image.load(asset_path(texture_filename)).convert_alpha()
        self.rect = self.texture.get_rect()
        self.update_rect()

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

    def set_is_dead(self, death):
        self.is_dead = death

    def set_position(self, position):
        self.position = list(position)
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (round(self.position[0]), round(self.position[1]))

    def move(self, direction, dt):
        if self.is_dead:
            return direction

        self.position[0] += direction * self.speed * dt
        if self.position[0] <= 0:
            self.position[0] = 0
            direction = 1
        elif self.position[0] >= SCREEN_WIDTH - self.rect.width:
            self.position[0] = SCREEN_WIDTH - self.rect.width
            direction = -1

        self.update_rect()
        return direction

    def die(self):
        self.is_dead = True
        print(f"{self.name} has died")

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.die()
        else:
            print(f"{self.name} has taken {damage} damage, now has {self.hp} hp")
        #self.draw_shuttle(screen)   

    def collision(self, obstacle):
        if self.rect.colliderect(obstacle.get_rect()):
            print(f"{self.name} has collided with {obstacle.get_name()}")
            self.take_damage(10)

    def draw_boss(self, screen):
        if not self.is_dead:
            screen.blit(self.texture, self.position)
