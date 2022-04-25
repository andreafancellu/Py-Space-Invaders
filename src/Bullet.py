import pygame


class Bullet:

    def __init__(self, pos):
        self.pos = pos
                
    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos
        
    def draw_bullet(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.pos[0], self.pos[1]), 10)

    def move_bullet(self):
        self.pos[1] -= 1