import pygame

from gym_game.helpers.cars import Player
from gym_game.helpers.sensors import create_sensors_data, update_position_sensors, draw_sensors, collisions, SENSORS_COLLISIONS_DATA
from gym_game.helpers.world import World, obstacle_sprites_group

import math


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


SENSORS_DATA = create_sensors_data(PLAYER.rect.center)


color_circle = (255,102,102)
center_circle = (100, 100)
radius_circle = 15

start_line = (center_circle[0]-1, center_circle[1])
end_line = (center_circle[0]-1, center_circle[1]-radius_circle+1)
line_length = 15
rotation_angle_degrees = 0
rotation_speed = 2

# Function to rotate a point around another point
def rotate_point(point, angle_deg, origin):
    angle_rad = math.radians(angle_deg)
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
    qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
    return round(qx), round(qy)


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
    update_position_sensors(SENSORS_DATA, PLAYER.rect.center, PLAYER.angle)
    draw_sensors(SENSORS_DATA, screen)
    collisions(SENSORS_DATA, obstacle_sprites_group)


    # position_text_distance_sensor = (300, 280)
    for sensor_name in SENSORS_COLLISIONS_DATA:

        if SENSORS_COLLISIONS_DATA[sensor_name]["point_of_collision"] != None:
            x = SENSORS_COLLISIONS_DATA[sensor_name]["point_of_collision"][0]
            y = SENSORS_COLLISIONS_DATA[sensor_name]["point_of_collision"][1]

            rect = pygame.Rect(x, y, 5, 5)
            pygame.draw.rect(screen, "red", rect)

            
    #         distance = collisions_sensors_dict[name_sensor]["distance"]
    #         distance_text = font.render(f"{name_sensor}: {round(distance, 2)}", False, (0,0,0))
    #         screen.blit(distance_text, position_text_distance_sensor)

    #         position_text_distance_sensor = (position_text_distance_sensor[0], position_text_distance_sensor[1] + 20)

    PLAYER.draw(screen)
    PLAYER.change_rotation()
    PLAYER.accelerate()
    collided = PLAYER.collisions(obstacle_sprites_group)

    if collided:
        PLAYER.reset()

    velocity_text = font.render(f"Velocity: {round(PLAYER.vel,2)}", False, (0,0,0))
    screen.blit(velocity_text,(20, 315))

    fps_text = font.render(f"FPS: {clock.get_fps()}", False, (0,0,0))
    screen.blit(fps_text, (20, 20))

    # offset_x, offset_y = (PLAYER.rect.x - AGENT.rect.x), (PLAYER.rect.y - AGENT.rect.y)
    # if PLAYER.mask.overlap(AGENT.mask, (offset_x, offset_y)):
    #     PLAYER.reset()
    #     AGENT.reset()




    # keys = pygame.key.get_pressed()
    # # Update rotation angle
    # if keys[pygame.K_g]:
    #     rotation_angle_degrees -= rotation_speed

    # if keys[pygame.K_j]:
    #     rotation_angle_degrees += rotation_speed

    # # Calculate end point after rotation
    # end_line = (start_line[0] + line_length, start_line[1])
    # rotated_end_point = rotate_point(end_line, rotation_angle_degrees, start_line)


    # pygame.draw.rect(screen, "black", pygame.Rect(85, 85, 30, 30))
    # pygame.draw.circle(screen, color_circle, center_circle, radius_circle)
    # pygame.draw.line(screen, "black", start_line, rotated_end_point, width=2)


    pygame.display.flip()
    pygame.display.update()

    clock.tick(30)

pygame.quit()