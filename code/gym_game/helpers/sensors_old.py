import pygame
import math
import numpy as np

SENSORS_NAME_ANGLE = [
    {"name": "diagonal_left", "angle": 45}, 
    {"name": "center", "angle": 90}, 
    {"name": "diagonal_right", "angle": 135},
    {"name": "right", "angle": 0},
    {"name": "left", "angle": 180}]
LINE_LENGTH_SENSOR = 200

NO_OBJECT_DETECTED = 200
SENSORS_COLLISIONS_INFO = {
    sensor["name"]: {"point_of_collision": None, "distance": NO_OBJECT_DETECTED} for sensor in SENSORS_NAME_ANGLE
}

SENSORS_POSITION_DATA = {}

COLOR_SENSOR = (27, 91, 252)


def draw_sensors(win, start_position, end_position):
    start_position = start_position
    end_position = end_position

    pygame.draw.line(win, COLOR_SENSOR, start_position, end_position, 3)


def update_sensors_position_data(standard_angle, player_center_position):
    for infos in SENSORS_NAME_ANGLE:
        name = infos["name"]
        angle = infos["angle"]

        start_pos_x = player_center_position[0]
        start_pos_y = player_center_position[1]
        
        angle_to_draw = standard_angle+angle

        end_pos_sensor = (
            start_pos_x + math.cos(math.radians(-angle_to_draw)) * LINE_LENGTH_SENSOR, # x
            start_pos_y + math.sin(math.radians(-angle_to_draw)) * LINE_LENGTH_SENSOR # y
        )

        SENSORS_POSITION_DATA[name] = {"start": (start_pos_x, start_pos_y), "end": end_pos_sensor}

    return SENSORS_POSITION_DATA


def collision_sensors(obstacles):
    for name in SENSORS_POSITION_DATA:
        start = SENSORS_POSITION_DATA[name]["start"]
        end = SENSORS_POSITION_DATA[name]["end"]

        collisions = {}
        for obstacle in obstacles:
            points_collision = obstacle.rect.clipline(start, end)

            if points_collision:
                x_point, y_point = points_collision[0]

                distance = np.linalg.norm(
                    np.array([*start]) - np.array([x_point, y_point])
                )

                collisions[distance] = (x_point, y_point)

        if collisions != {}:
            min_distance_collision = min(collisions)
            point_of_collision = collisions[min_distance_collision]

            SENSORS_COLLISIONS_INFO[name] = {
                "point_of_collision": point_of_collision,
                "distance": min_distance_collision
            }
        else:
            SENSORS_COLLISIONS_INFO[name] = {
                "point_of_collision": None,
                "distance": NO_OBJECT_DETECTED
            }

    return SENSORS_COLLISIONS_INFO