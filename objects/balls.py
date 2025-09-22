import pygame
import random
import math
from .base import SimObject

class Ball(SimObject):
    def __init__(self, x, y, radius=10, color=(255, 0, 0),
                 gravity=(0, 0.1), collisions=True, energy_return=1.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.gravity = gravity
        self.collisions = collisions
        self.energy_return = energy_return
        self.time_since_color_change = 0

    def update(self, dt):
        # Apply gravity
        self.vx += self.gravity[0] * dt
        self.vy += self.gravity[1] * dt

        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def bounce(self, normal):
        dot = self.vx * normal[0] + self.vy * normal[1]
        self.vx -= 2 * dot * normal[0]
        self.vy -= 2 * dot * normal[1]
        self.vx *= self.energy_return
        self.vy *= self.energy_return

    def check_collision(self, other):
        # Ball-to-ball collision
        if isinstance(other, Ball):
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < self.radius + other.radius:
                return ("ball_ball", dx/dist, dy/dist)
        return None
