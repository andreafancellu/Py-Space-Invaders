import pygame

from constants import asset_path


class Alien:
    def __init__(self, name, position):
        self.name = name
        self.is_dead = False
        self.position = list(position)
        self.texture = pygame.image.load(asset_path("alien.png")).convert_alpha()
        self.rect = self.texture.get_rect()
        self.update_rect()

    def get_name(self):
        return self.name

    def get_is_dead(self):
        return self.is_dead

    def get_position(self):
        return self.position

    def get_rect(self):
        return self.rect

    def set_is_dead(self, is_dead):
        self.is_dead = is_dead

    def set_position(self, position):
        self.position = list(position)
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (round(self.position[0]), round(self.position[1]))

    def draw_alien(self, screen):
        if not self.is_dead:
            screen.blit(self.texture, self.position)

    def move_down(self, distance):
        if self.is_dead:
            return

        self.position[1] += distance
        if self.position[1] > 700:
            self.position[1] = 0
        self.update_rect()

    def move_horizontal(self, distance):
        if self.is_dead:
            return

        self.position[0] += distance
        self.update_rect()
        
    def die(self):
        self.is_dead = True
        self.set_position([-100, -100])

    def collision(self, obstacle):
        if not self.is_dead and self.rect.colliderect(obstacle.get_rect()):
            print(f"{self.name} has collided with {obstacle.get_name()}")
            self.die()
