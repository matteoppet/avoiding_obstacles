import pygame
import math

def draw_sensors(win, player_center_x, player_center_y, standard_angle, angle_sensor, line_length):
    start_pos = (player_center_x, player_center_y)
    
    angle_to_draw = standard_angle+angle_sensor

    end_pos_sensor = (
        start_pos[0] + math.cos(math.radians(-angle_to_draw)) * line_length, # x
        start_pos[1] + math.sin(math.radians(-angle_to_draw)) * line_length # y
    )

    pygame.draw.line(win, "red", start_pos, end_pos_sensor, 3)