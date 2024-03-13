import pygame

from helpers.cars import Player, Agent
from helpers.sensors import draw_sensors, update_sensors_position_data, collision_sensors
from helpers.world import World, obstacle_sprites_group

from stable_baselines3 import PPO

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1280, 720)) # change size window
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("calibri", 20)

# two cars
topSpeed = 4
turnRate = 3

PLAYER = Player(
    topSpeed,
    turnRate
)
WORLD = World()
WORLD.create_rect()
obstacle_sprites_group = obstacle_sprites_group

path_model = "trained_agent/models/trained_agent/models/1710347473/PPO_MODEL_1000000.zip"
MODEL = PPO.load(path_model)


def get_observation():
    pass


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)

    screen.fill("#d3d3d3")

    WORLD.draw_rects(screen)
    
    # SENSORS SECTION
    data_sensors = update_sensors_position_data(
        player_center_position=PLAYER.rect.center,
        standard_angle=PLAYER.angle,
    )

    for name, info in data_sensors.items():
        draw_sensors(win=screen, start_position=info["start"], end_position=info["end"])

    collisions_sensors_dict = collision_sensors(obstacle_sprites_group)

    for name_sensor in collisions_sensors_dict:

        if collisions_sensors_dict[name_sensor]["point_of_collision"] != None:
            x = collisions_sensors_dict[name_sensor]["point_of_collision"][0]
            y = collisions_sensors_dict[name_sensor]["point_of_collision"][1]

            rect = pygame.Rect(x, y, 5, 5)
            pygame.draw.rect(screen, "red", rect)

    # PLAYER.draw(screen)
    # PLAYER.change_rotation()
    # PLAYER.accelerate()
    # PLAYER.collisions(obstacle_sprites_group)

    velocity_text = font.render(f"Velocity: {round(PLAYER.vel,2)}", False, (0,0,0))
    screen.blit(velocity_text,(20, 315))

    fps_text = font.render(f"FPS: {clock.get_fps()}", False, (0,0,0))
    screen.blit(fps_text, (20, 20))

    # offset_x, offset_y = (PLAYER.rect.x - AGENT.rect.x), (PLAYER.rect.y - AGENT.rect.y)
    # if PLAYER.mask.overlap(AGENT.mask, (offset_x, offset_y)):
    #     PLAYER.reset()
    #     AGENT.reset()

    pygame.display.flip()
    pygame.display.update()

    clock.tick(30)

pygame.quit()