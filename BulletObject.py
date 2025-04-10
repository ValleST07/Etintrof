import math

class Bullet:
    def __init__(self, pos, angle, speed=5):
        self.pos=pos
        self.angle = angle
        self.speed = speed

    def move(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

    def get_position(self):
        return self.pos