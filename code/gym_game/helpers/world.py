import pygame
import numpy as np

COLOR = (110, 128, 113)
obstacle_sprites_group = pygame.sprite.Group()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, info_rect):
        super().__init__()

        x, y, width, height = info_rect

        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)

class World:
    def __init__(self, window_size, screen, background):
        self.window_size = window_size
        self.screen = screen
        self.background = background 


    def bounds_window(self, window_size):
        x_window = window_size[0]
        y_window = window_size[1]

        return [
            (-50, 0, 50, y_window),
            (0, -50, x_window, 50),
            (x_window, 0, x_window+50, y_window),
            (0, y_window, x_window, y_window+50)
        ]
    

    def rect_in_map(self, window_size):
        x_window = window_size[0]
        y_window = window_size[1]

        return [
            (100, 100, 80, 80),
            (500, 500, 80, 80),
            (200, 350, 80, 80),
            (800, 550, 80, 80),
            (700, 200, 80, 80),
            (400, 250, 80, 80),
            (950, 250, 80, 80),
            (1000, 500, 80, 80),
            (1020, 80, 80, 80),
            (100, 600, 80, 80),
            (-50, 0, 50, y_window),
            (0, -50, x_window, 50),
            (x_window, 0, x_window+50, y_window),
            (0, y_window, x_window, y_window+50)
        ]
    

    def generate_obstacles(self, number_of_obstacles):
        obstacles_to_draw = [
            (0, -50, self.window_size[0], 50),
            (self.window_size[0]+1, 0, 50, self.window_size[1]),
            (0, self.window_size[1]+1, self.window_size[0], 50),
            (-50, +1, 50, self.window_size[1]-2)
        ]
        position_already_taken = [
            (0, -50),
            (self.window_size[0]+1, 0),
            (0, self.window_size[1]+1),
            (-50, +1)
        ]

        temporary_rect_list = []
        
        count = 0
        while count != number_of_obstacles:

            x = np.random.randint(0, self.window_size[0])
            y = np.random.randint(0, self.window_size[1])
            temporary_rect = pygame.Rect(x, y, 50, 50)

            less_far_obstacle = 9999
            for obstacle_info in obstacles_to_draw:
                center_x_obstacle = obstacle_info[0]+(obstacle_info[2]/2)
                center_y_obstacle = obstacle_info[1]+(obstacle_info[3]/2)
                
                distance = np.linalg.norm(
                    np.array([center_x_obstacle, center_y_obstacle]) - np.array([x+40, y+40])
                )
                
                if distance < less_far_obstacle:
                    less_far_obstacle = distance

            if not (x, y) in position_already_taken and less_far_obstacle > 200:

                for temp_x, temp_y, temp_width, temp_height in obstacles_to_draw:
                    temporary_rect_list.append(pygame.Rect(temp_x, temp_y, temp_width, temp_height))

                collides = temporary_rect.collidelist(temporary_rect_list)
                if collides == -1:
                    obstacles_to_draw.append((x, y, 80, 80))
                    position_already_taken.append((x, y))
                    count += 1


        # TODO clean this code

        return obstacles_to_draw
    

    def reset_obstacles(self, obstacle_group, number_of_obstacles):
        obstacle_group.empty()
        info_rects = self.generate_obstacles(number_of_obstacles)
        for info_rect in info_rects:
            obstacle = Obstacle(info_rect)
            obstacle_group.add(obstacle)


    def draw_rects(self, win):
        for sprite in obstacle_sprites_group:
            pygame.draw.rect(win, COLOR, sprite.rect)


# spawb random obstacles each time the map is reloaded4