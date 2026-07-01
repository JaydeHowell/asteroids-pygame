import pygame
from core.circleshape import CircleShape
from core.constants import SHOT_RADIUS, BOMB_DELAY, BOMB_BLAST_RADIUS
from actors.blast import Blast

class Bomb(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, SHOT_RADIUS)
        self.bomb_delay = BOMB_DELAY

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, "yellow", self.position, self.radius, width=0)

    
    def update(self, dt):
        self.position -= (self.velocity * dt)
        if self.bomb_delay <= 0:
            self.explode()
            return
        
        self.bomb_delay = max(0, self.bomb_delay - dt)


    def explode(self):
        self.kill()
        bomb_blast = Blast(self.position.x, self.position.y, BOMB_BLAST_RADIUS)

