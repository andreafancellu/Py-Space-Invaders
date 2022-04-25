import pygame


class Bullet:

    def __init__(self, position):
        self.name = "Bullet"
        self.position = position
        self.texture = pygame.image.load("/home/andrea/Projects/Py-Space-Invaders/data/bomb.png").convert()
        self.rect = self.texture.get_rect()
                
    #* getters and setters
    def get_name(self):
        return self.name

    def get_pos(self):
        return self.position

    def get_rect(self):
        return self.rect

    def set_pos(self, position):
        self.position = position
        
    #* in-game functions
    def draw_bullet(self, screen):
        screen.blit(self.texture, self.position)
        #pygame.draw.rect(screen, (0, 120, 120), self.rect)

    def move_bullet(self):
        self.position[1] -= 2
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)

    def collision(self, obstacle):
        return self.rect.colliderect(obstacle.get_rect())