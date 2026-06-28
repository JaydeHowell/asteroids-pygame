import pygame

import random
import math
from dataclasses import dataclass

from circleshape import CircleShape
from constants import (
        LINE_WIDTH,
        ASTEROID_MIN_RADIUS,
        ASTEROID_MAX_RADIUS,
        ASTEROID_VERTICES,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        )
from logger import log_event

@dataclass
class Wave:
    frequency: int
    amplitude: float
    phase_shift: float

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.angle = random.uniform(7.0, 15.0)
        self.angular_velocity = random.uniform(-3.0, 2.0)
        self.fundamental_amplitude = random.uniform(0.1, 0.3) * self.radius
        self.harmonics = int(3 * (self.radius / ASTEROID_MIN_RADIUS))
        self.local_vertices = self.get_polar()
    
    def draw(self, screen: pygame.Surface) -> None:
        global_vertices = []

        for x, y in self.local_vertices:
            rotated_x, rotated_y = self.body_to_inertial(x, y)
            global_x = rotated_x + self.position.x
            global_y = rotated_y + self.position.y
            global_vertices.append((global_x, global_y))

        pygame.draw.polygon(screen, "white", global_vertices, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)

        self.angle += self.angular_velocity * dt

        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius


    # defines asteroid split logic and returns score for destroying an asteroid (L = 10, M = 15, S = 20)
    def split(self) -> int:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 20

        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        first_rotated = self.velocity.rotate(random_angle)
        second_rotated = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        
        first_asteroid.velocity = first_rotated * 1.2
        second_asteroid.velocity = second_rotated * 1.2
        
        if self.radius < ASTEROID_MAX_RADIUS:
            return 15
        return 10
    

    def get_polar(self) -> list:
        coordinates = []
        waves = []
        
        for i in range(2, self.harmonics + 2):
            wave = Wave(frequency=i, amplitude=(self.fundamental_amplitude / i**1.5), phase_shift=random.uniform(0.0, 2 * math.pi))
            waves.append(wave)


        step_size = 2 * math.pi / ASTEROID_VERTICES

        for i in range(ASTEROID_VERTICES):

            theta = i * step_size
            asteroid_radius = self.radius
            for wave in waves:
                asteroid_radius += wave.amplitude * math.sin(wave.frequency * theta + wave.phase_shift)

            x = asteroid_radius * math.cos(theta)
            y = asteroid_radius * math.sin(theta)

            coordinates.append((x, y))


        return coordinates


    def body_to_inertial(self, x: float, y: float) -> tuple[float, float]:
        dp_x = x * math.cos(self.angle) - y * math.sin(self.angle)
        dp_y = x * math.sin(self.angle) + y * math.cos(self.angle)

        return dp_x, dp_y
