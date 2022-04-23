import pygame
class Shuttle:
    
    def __init__(self, name, hp, position):
        self.name = name
        self.hp = hp
        self.is_dead = False
        self.position = position
        self.texture = pygame.image.load("/home/andrea/Projects/Py-Space-Invaders/data/shuttle.jpeg").convert()

    #* getters and setters
    def set_name(self, name):
        self.name = name
    
    def set_hp(self, hp):
        self.hp = hp

    def set_is_dead(self, is_dead):
        self.is_dead = is_dead

    def set_position(self, position):
        self.position = position

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_is_dead(self):
        return self.is_dead

    def get_position(self):
        return self.position

    #* in-game functions
    def move_left(self):
        self.position[0] -= 10

    def move_right(self):
        self.position[0] += 10

    def move_up(self):
        self.position[1] -= 10

    def move_down(self):
        self.position[1] += 10

    def die(self):
        self.hp = 0
        self.is_dead = True
        print(f"{self.name} has died")

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()
        else:
            print(f"{self.name} has taken {damage} damage")

    def draw_shuttle(self, screen):
        screen.blit(self.texture, self.position)

    def __str__(self):
        return f"the shuttle named {self.name} has {self.hp}"