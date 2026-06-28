import pygame
import math
import random
from circleshape import CircleShape
from wave import Wave
from constants import BLAST_VERTICES

class Blast(CircleShape):
    def __init__(self, x: float, y: float, max_radius: float):
        super().__init__(x, y, radius=0)
        self.max_radius = max_radius
        self.time_integral = 0.0
        self.k_p = 4.7
        self.fundamental_amplitude = random.uniform(0.15, 0.3) * self.max_radius
        self.harmonics = random.randint(3, 9)


    def draw(self, screen):
        local_vertices = self.get_polar()
        pygame.draw.polygon(screen, "red", local_vertices, width=0)

    
    def update(self, dt):
        self.time_integral += dt

        error = self.max_radius - self.radius
        command_velocity = error * self.k_p
        self.radius += command_velocity * dt
        if error <= 0.05:
            self.kill()


    def get_polar(self) -> list:
        coordinates = []
        waves = []

        for i in range(2, self.harmonics + 2):
            wave = Wave(frequency=i, amplitude=(self.fundamental_amplitude / i**1.5), phase_shift=random.uniform(0.0, 2 * math.pi))
            waves.append(wave)

        step_size = 2 * math.pi / BLAST_VERTICES

        for i in range(BLAST_VERTICES):

            theta = i * step_size
            blast_radius = self.radius
            for wave in waves:
                phase_velocity = wave.phase_shift
                blast_radius += wave.amplitude * math.sin(wave.frequency * theta + phase_velocity * self.time_integral)

            x = self.position.x + blast_radius * math.cos(theta)
            y = self.position.y + blast_radius * math.sin(theta)

            coordinates.append((x, y))


        return coordinates
