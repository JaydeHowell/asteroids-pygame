import pygame
from circleshape import CircleShape
from shot import Shot
from constants import (
        PLAYER_RADIUS,
        LINE_WIDTH,
        PLAYER_TURN_SPEED,
        PLAYER_SPEED,
        PLAYER_SHOOT_SPEED,
        PLAYER_SHOOT_COOLDOWN_SECONDS,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        )

class Player(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0


    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        draw_points = self.triangle()
        pygame.draw.polygon(screen, "white", draw_points, LINE_WIDTH)

    
    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt


    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt)

        if keys[pygame.K_d]:
            self.rotate(dt * -1)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(dt * -1)

        if keys[pygame.K_SPACE]:
            self.shoot()

        if keys[pygame.K_c]:
            self.drop_bomb()

        self.shot_cooldown = max(0, self.shot_cooldown - dt)

        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT


    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector


    def shoot(self) -> None:
        if not self.shot_cooldown > 0:
            bullet = Shot(self.position.x, self.position.y)
            velocity_vector = pygame.Vector2(0,1)
            rotated_vector = velocity_vector.rotate(self.rotation)
            bullet.velocity = rotated_vector * PLAYER_SHOOT_SPEED
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def drop_bomb(self) -> None:
        bomb = Bomb(self.position.x, self.position.y)
