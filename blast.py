import pygame
import math
import random
from circleshape import CircleShape
from constants import BLAST_VERTICES

class Blast(CircleShape):
    def __init__(self, x: float, y: float, max_radius: float):
        super().__init__(x, y, radius=20)
        self.max_radius = max_radius
        self.time_integral = 0.0
        self.phase_velocity = random.uniform(2.0, 8.0)
        self.spatial_frequency = random.randint(7, 14)
        self.amplitude = random.randint(10, 20)

    def draw(self, screen):
        points = self.get_polar()
        pygame.draw.polygon(screen, "red", points, width=0)

    
    def update(self, dt):
        self.time_integral += dt
        self.radius += (self.max_radius * dt)
        if self.radius >= self.max_radius:
            self.kill()


    def get_polar(self) -> list:
        coordinates = []

        step_size = 2 * math.pi / BLAST_VERTICES

        for i in range(BLAST_VERTICES):

            theta = i * step_size
            blast_radius = self.radius + self.amplitude * math.sin(self.spatial_frequency * theta + self.phase_velocity * self.time_integral)

            x = self.position.x + blast_radius * math.cos(theta)
            y = self.position.y + blast_radius * math.sin(theta)

            coordinates.append((x, y))


        return coordinates
