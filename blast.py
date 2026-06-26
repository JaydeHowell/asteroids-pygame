import pygame
from circleshape import CircleShape

class Blast(CircleShape):
    def __init__(self, x: float, y: float, max_radius: float):
        super().__init__(x, y, 0)
        self.max_radius = max_radius

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, width=0)

    
    def update(self, dt):
        self.radius += (self.max_radius * dt)
        if self.radius >= self.max_radius:
            self.kill()

