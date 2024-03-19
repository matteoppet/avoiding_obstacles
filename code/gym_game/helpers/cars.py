import pygame
import math
import random

class AbstractCar:
    def __init__(self, top_speed, turnRate):
        self.img = self.IMG
        
        if not self.START_POS is None:
            self.x, self.y = self.START_POS
        else:
            self.x, self.y = (0,0)
        
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.mask = pygame.mask.from_surface(self.img)

        # Variables
        self.vel = 0
        self.acceleration = 0.05
        self.angle = 0

        # Constants
        self.topSpeed = top_speed
        self.turnRate = turnRate

    # rotate the car
    def rotate(self, left=False, right=False):
        if left:
            if self.angle > 360:
                self.angle = 0
            else:
                self.angle += self.turnRate
        elif right:
            if self.angle < 0:
                self.angle = 360
            else:
                self.angle -= self.turnRate


    def increase_velocity(self):
        if self.vel <= self.topSpeed:
            self.vel += 0.1

    def decrease_velocity(self):
        if self.vel > 0:
            self.vel -= 0.2
        
        if self.vel < 0: 
            self.vel = 0

    # move the car by the velocity and angle
    def move(self):
        # radians: 180 (degrees) = pi, 360 (degrees) = 2pi
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        self.rect.x = self.x
        self.rect.y = self.y

    # call the function for drawing
    def draw(self, win):
        self.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    # rotate the image and the rect, and draw them
    def blit_rotate_center(self, win, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle) # rotate the image from the topleft 
        
        new_rect = rotated_image.get_rect(
            center=image.get_rect(topleft=topleft).center
        ) # rotate the image without changing coordinates
        
        self.rect = new_rect

        win.blit(rotated_image, new_rect.topleft)

    # reset all the variables and return to the starting position
    def reset(self, random_position_start):
        random_position_start=random_position_start
        self.x, self.y = random_position_start
        self.rect.x, self.rect.y = random_position_start

        self.vel = 0
        self.acceleration = 0.05
        self.angle = 0

    def collisions(self, obstacles):
        for obstacle in obstacles:

            if self.rect.colliderect(obstacle.rect):
                return True

##########################################################################

absolute_path_image_car = "C:/Users/matte/programming/pythons/projects/avoiding_obstacles/assets/images/player.png" # TODO: change

class Player(AbstractCar):
    # both used in fun_utils/AbstractCar class
    IMG = pygame.image.load(absolute_path_image_car) 
    START_POS = (100, 200)

    def change_rotation(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)

    def accelerate(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.increase_velocity()
        if keys[pygame.K_s]:
            self.decrease_velocity()
        
        self.move()


class Agent(AbstractCar):
    IMG = pygame.image.load(absolute_path_image_car) 
    START_POS = None
    START_POSITIONS = [
        (1136, 198), 
        (576, 93), 
        (156, 206), 
        (1177, 452), 
        (950, 329), 
        (726, 611), 
        (137, 452), 
        (602, 452)
    ]

    def update_position(self, action):
        if action == 1: # accelerate
            self.increase_velocity()
        elif action == 2: # decelerate 
            self.decrease_velocity()
        elif action == 3: # steer right
            self.rotate(right=True)
        elif action == 4: # steer left
            self.rotate(left=True)

        self.move()

    def get_random_position(self):
        random_position = random.choice(self.START_POSITIONS)
        return random_position