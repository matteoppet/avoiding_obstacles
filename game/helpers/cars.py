import pygame
from helpers.fun_utils import AbstractCar

absolute_path_image_car = "C:/Users/matte/programming/pythons/projects/avoiding_obstacles/assets/images/player.png"

class Player(AbstractCar):
    # both used in fun_utils/AbstractCar class
    IMG = pygame.image.load(absolute_path_image_car) 
    START_POS = (100, 100)

    def change_rotation(self):
        keys = pygame.key.get_pressed()

        if self.vel != 0:
            if keys[pygame.K_a]:
                self.rotate(left=True)
            if keys[pygame.K_d]:
                self.rotate(right=True)

    def accelerate(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_w]:
            moved = True
            self.increase_velocity()
        
        if not moved:
            self.decrease_velocity()


class Agent(AbstractCar):
    IMG = pygame.image.load(absolute_path_image_car) 
    START_POS = (200, 200)