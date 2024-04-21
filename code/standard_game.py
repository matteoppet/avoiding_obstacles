import pygame

from gym_game.helpers.cars import Player
from gym_game.helpers.sensors import create_sensors_data, update_position_sensors, draw_sensors, collision_sensors, SENSORS_COLLISIONS_DATA
from gym_game.helpers.world import World

import math
import numpy as np


pygame.init()
pygame.font.init()

SIZE_WINDOW = (1280, 720)

screen = pygame.display.set_mode(SIZE_WINDOW) # change size window
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("calibri", 20)
background = pygame.Surface(SIZE_WINDOW)

topSpeed = 3
turnRate = 3

PLAYER = Player(
    topSpeed,
    turnRate
)
PLAYER.reset(PLAYER.START_POS)


WORLD = World(
    SIZE_WINDOW
)
obstacle_group = pygame.sprite.Group()
WORLD.reset_obstacles(obstacle_group, 1)

SENSORS_DATA = create_sensors_data(PLAYER.rect.center)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            WORLD.reset_obstacles(obstacle_group, 1)

    # WORLD.draw_rects(screen)
    screen.fill("#d3d3d3")
    obstacle_group.draw(screen, background)
    
    # SENSORS SECTION
    update_position_sensors(SENSORS_DATA, PLAYER.rect.center, PLAYER.angle)
    draw_sensors(SENSORS_DATA, screen)

    PLAYER.draw(screen)
    PLAYER.change_rotation()
    PLAYER.accelerate()
    collided = PLAYER.collisions(obstacle_group)

    if collided:
        PLAYER.reset((
            np.random.randint(0, SIZE_WINDOW[0]),
            np.random.randint(0, SIZE_WINDOW[1])
        ))

    velocity_text = font.render(f"Velocity: {round(PLAYER.vel,2)}", False, (0,0,0))
    screen.blit(velocity_text,(20, 315))

    fps_text = font.render(f"FPS: {clock.get_fps()}", False, (0,0,0))
    screen.blit(fps_text, (20, 20))

    pygame.display.flip()
    pygame.display.update()

    clock.tick(40)

pygame.quit()
