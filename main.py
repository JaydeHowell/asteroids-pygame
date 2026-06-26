import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from bomb import Bomb
from blast import Blast


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    bg_unscaled = pygame.image.load("images/background.png").convert()

    background = pygame.transform.scale(bg_unscaled, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    dt = 0.0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    asteroids = pygame.sprite.Group()

    shots = pygame.sprite.Group()

    bombs = pygame.sprite.Group()
    blasts = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    Bomb.containers = (updatable, drawable, bombs)
    Blast.containers = (updatable, drawable, blasts)

    screen.blit(background, (0, 0))

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    field = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit(1)
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
            for bomb in bombs:
                if asteroid.collides_with(bomb):
                    bomb.explode()
            for blast in blasts:
                if asteroid.collides_with(blast):
                    log_event("explosion_hit_asteroid")
                    asteroid.split()

        screen.blit(background, (0, 0))

        for char in drawable:
            char.draw(screen)

        dt = clock.tick(60) / 1000
        pygame.display.flip()

if __name__ == "__main__":
    main()
