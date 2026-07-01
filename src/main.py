import pygame
import sys

from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from system.logger import log_state, log_event
from actors.player import Player
from actors.asteroid import Asteroid
from actors.asteroidfield import AsteroidField
from actors.shot import Shot
from actors.bomb import Bomb
from actors.blast import Blast


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Jayde")

    bg_unscaled = pygame.image.load("../assets/background.png").convert()

    background = pygame.transform.scale(bg_unscaled, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    dt = 0.0

    score_font = pygame.font.SysFont(None, 36)
    score_value = 0
    
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
                print(f"Final Score: {score_value}")
                sys.exit(1)
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score_value += asteroid.split()
                    shot.kill()
            for bomb in bombs:
                if asteroid.collides_with(bomb):
                    bomb.explode()
            for blast in blasts:
                if asteroid.collides_with(blast):
                    log_event("explosion_hit_asteroid")
                    asteroid.split()

        score_text = score_font.render(f"Score: {score_value}", True, "White")

        screen.blit(background, (0, 0))
        screen.blit(score_text, (20, 20))

        for char in drawable:
            char.draw(screen)

        dt = clock.tick(60) / 1000
        pygame.display.flip()

if __name__ == "__main__":
    main()
