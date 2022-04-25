import pygame


class Bullet:

    def __init__(self, pos):
        self.pos = pos
                
    def get_pos(self):
        return self.pos

    def get_shot(self):
        return self.shot
        
    def draw_bullet(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.get_pos()[0]+20, self.get_pos()[1]), 10)
        self.move_bullet()

    def move_bullet(self):
        self.pos[1] -= 1