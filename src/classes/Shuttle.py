class Shuttle:
    
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.is_dead = False
        self.texture = "Py-Space-Invaders\data\shuttle.png"

    def set_name(self, name):
        self.name = name
    
    def set_hp(self, hp):
        self.hp = hp

    def set_is_dead(self, is_dead):
        self.is_dead = is_dead

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_is_dead(self):
        return self.is_dead

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

    def __str__(self):
        return f"the shuttle named {self.name} has {self.hp}"