import pygame

from constants import asset_path


class Bullet:
    def __init__(self, position, speed):
        self.name = "Bullet"
        self.position = list(position)
        self.speed = speed
        self.texture = pygame.image.load(asset_path("bomb.png")).convert_alpha()
        self.rect = self.texture.get_rect()
        self.update_rect()
                
    def get_name(self):
        return self.name

    def get_pos(self):
        return self.position

    def get_rect(self):
        return self.rect

    def set_pos(self, position):
        self.position = list(position)
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (round(self.position[0]), round(self.position[1]))
        
    def draw_bullet(self, screen):
        screen.blit(self.texture, self.position)

    def move_bullet(self, dt):
        self.position[1] -= self.speed * dt
        self.update_rect()

    def collision(self, obstacle):
        return not obstacle.get_is_dead() and self.rect.colliderect(obstacle.get_rect())
