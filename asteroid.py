import pygame

import random

from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)

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
