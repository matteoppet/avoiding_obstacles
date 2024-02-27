import pygame

from helpers.player import Player

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

PLAYER = Player()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#f8f7ff")
    screen.blit(PLAYER.image, (PLAYER.rect.x, PLAYER.rect.y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()