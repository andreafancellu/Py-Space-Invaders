import pygame

class Alien:

    def __init__(self, name, position):
        self.name = name
        self.is_dead = False
        self.position = position
        self.texture = pygame.image.load("/home/andrea/Projects/Py-Space-Invaders/data/alien.png").convert()
        self.rect = self.texture.get_rect()

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
        if not(self.is_dead):
            screen.blit(self.texture, self.position)
            self.rect = pygame.Rect(self.position[0], self.position[1], self.rect.width, self.rect.height)
            #pygame.draw.rect(screen, (124, 123, 89), self.rect)

    def move_down(self):
        self.position[1] += 0.1
        self.set_rect()
        if self.position[1] > 700:
            self.position[1] = 0
    
    def move_left(self):
        self.position[0] -= 0.5
        self.set_rect()
    
    def move_right(self):
        self.position[0] += 0.5
        self.set_rect()
        
    def die(self):
        self.set_is_dead = True
        self.set_position([-100, -100])

    #! inutile post bullet.collision(alien)
    def collision(self, obstacle):
        if self.rect.colliderect(obstacle.get_rect()):
            print(f"{self.name} has collided with {obstacle.get_name()}")
            self.die()

            
    

    