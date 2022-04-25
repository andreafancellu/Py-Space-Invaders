import pygame


class Bullet:

    def __init__(self, position):
        self.name = "Bullet"
        self.position = position
        self.rect = pygame.Rect(self.position[0], self.position[1], 10, 10)
                
    def get_name(self):
        return self.name

    def get_pos(self):
        return self.position

    def get_rect(self):
        return self.rect

    def set_pos(self, position):
        self.position = position
        
    def draw_bullet(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.position[0], self.position[1]), 10)

    def move_bullet(self):
        self.position[1] -= 0.7
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)