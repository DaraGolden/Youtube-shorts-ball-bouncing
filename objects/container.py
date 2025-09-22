import pygame
import math
from .base import SimObject

class Container(SimObject):
    def __init__(self, x, y, shape="circle", size=200,
                 rotation_speed=0, energy_return=1.0, holes=None):
        self.x = x
        self.y = y
        self.shape = shape
        self.size = size
        self.rotation_speed = rotation_speed
        self.energy_return = energy_return
        self.rotation_angle = 0
        self.holes = holes if holes else []

    def update(self, dt):
        self.rotation_angle += self.rotation_speed * dt

    def draw(self, surface):
        if self.shape == "circle":
            pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.size, width=3)

    def check_collision(self, ball):
        if self.shape == "circle":
            dx = ball.x - self.x
            dy = ball.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist + ball.radius > self.size:  # crossed boundary
                nx, ny = dx / dist, dy / dist
                # reposition ball just inside boundary
                ball.x = self.x + nx * (self.size - ball.radius)
                ball.y = self.y + ny * (self.size - ball.radius)
                return ("ball_container", nx, ny)
        return None

