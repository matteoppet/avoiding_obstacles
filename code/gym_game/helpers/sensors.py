import pygame
import math
import numpy as np


LINE_LENGTH = 200
COLOR_SENSOR = (190, 190, 190)
SENSORS_COLLISIONS_DATA = {}
NO_COLLISION_DETECTED = 9999


def update_position_sensors(SENSORS_DATA, player_center, angle_player):
    SENSORS_DATA = SENSORS_DATA
    for sensor in SENSORS_DATA:
        angle = sensor["angle"]

        start_pos = player_center

        angle_to_calculate = angle_player+angle

        end_pos = (
            start_pos[0] + math.cos(math.radians(-angle_to_calculate)) * LINE_LENGTH,
            start_pos[1] + math.sin(math.radians(-angle_to_calculate)) * LINE_LENGTH
        )

        sensor["start_pos"] = start_pos
        sensor["end_pos"] = end_pos


def create_sensors_data(player_center):
    return [
        {"name": 1, "angle": 0, "start_pos": player_center, "end_pos": None},
        {"name": 2, "angle": 45, "start_pos": player_center, "end_pos": None},
        {"name": 3, "angle": 90, "start_pos": player_center, "end_pos": None},
        {"name": 4, "angle": 135, "start_pos": player_center, "end_pos": None},
        {"name": 5, "angle": 180, "start_pos": player_center, "end_pos": None},
        {"name": 6, "angle": 225, "start_pos": player_center, "end_pos": None},
        {"name": 7, "angle": 270, "start_pos": player_center, "end_pos": None},
        {"name": 8, "angle": 315, "start_pos": player_center, "end_pos": None},
    ]


def draw_sensors(SENSORS_DATA, screen):
    for sensor in SENSORS_DATA:
        start = sensor["start_pos"]
        end = sensor["end_pos"]

        pygame.draw.line(screen, COLOR_SENSOR, start, end, 2)


def collision_sensors(SENSORS_DATA, obstacles):
    for sensor in SENSORS_DATA:
        start = sensor["start_pos"]
        end = sensor["end_pos"]

        collisions = {}
        for obstacle in obstacles:
            points_collision = obstacle.rect.clipline(start, end)

            if points_collision:
                x, y = points_collision[0] # the contact of the sensor less far from the player

                distance = np.linalg.norm(
                    np.array([*start]) - np.array([x, y])
                )

                distance = calculate_proportion(
                    distance,
                    16,
                    200
                )

                collisions[distance] = (x, y)

        if collisions != {}:
            collision_lessfar = min(collisions)
            point_of_collision = collisions[collision_lessfar]

            SENSORS_COLLISIONS_DATA[sensor["name"]] = {
                "point_of_collision": point_of_collision,
                "distance": collision_lessfar
            }
        else:
            SENSORS_COLLISIONS_DATA[sensor["name"]] = {
                "point_of_collision": None,
                "distance": NO_COLLISION_DETECTED
            }


def calculate_proportion(collision_distance, player_radius, max_distance):
    proportion = (collision_distance - player_radius) / max_distance
    return int(round(proportion * 100))