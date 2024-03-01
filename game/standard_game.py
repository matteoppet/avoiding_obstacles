import pygame

from helpers.cars import Player, Agent
from helpers.sensors import draw_sensors
from helpers.world import World

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1280, 720)) # change size window
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("calibri", 20)

# two cars
topSpeed = 3
turnRate = 3

PLAYER = Player(
    topSpeed,
    turnRate
)
AGENT = Agent(
    topSpeed,
    turnRate
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#f8f7ff")

    for angle_sensor in [45, 90, 135]:
        draw_sensors(
            win=screen, 
            player_center_x=PLAYER.rect.centerx, 
            player_center_y=PLAYER.rect.centery, 
            standard_angle=PLAYER.angle,
            angle_sensor=angle_sensor,
            line_length=100
        )

    PLAYER.draw(screen)
    PLAYER.change_rotation()
    PLAYER.accelerate()

    AGENT.draw(screen)

    offset_x, offset_y = (PLAYER.rect.x - AGENT.rect.x), (PLAYER.rect.y - AGENT.rect.y)
    if PLAYER.mask.overlap(AGENT.mask, (offset_x, offset_y)):
        PLAYER.reset()
        AGENT.reset()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()