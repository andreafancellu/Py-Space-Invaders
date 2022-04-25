import pygame

class Alien:

    def __init__(self, name, position):
        self.name = name
        self.is_dead = False
        self.position = position
        self.texture = pygame.image.load("/home/andrea/Projects/Py-Space-Invaders/data/alien.png").convert()
        self.rect = self.texture.get_rect()
        pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)

    #* getters and setters
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
        self.position = position

    def set_rect(self):
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)

    #* in-game functions
    def draw_alien(self, screen):
        screen.blit(self.texture, self.position)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)
    

    