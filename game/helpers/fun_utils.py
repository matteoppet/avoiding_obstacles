import pygame
import math

class AbstractCar:
    def __init__(self, top_speed, turnRate):
        self.img = self.IMG
        self.x, self.y = self.START_POS
        
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

    # increase the velocity
    def increase_velocity(self):
        self.vel = min(self.vel + self.acceleration, self.topSpeed)
        self.move()

    # decrease the velocity 
    def decrease_velocity(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

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

        pygame.draw.rect(win, "red", new_rect)
        win.blit(rotated_image, new_rect.topleft)

    # reset all the variables and return to the starting position
    def reset(self):
        self.x, self.y = self.START_POS
        self.rect.x, self.rect.y = self.START_POS

        self.vel = 0
        self.acceleration = 0.05
        self.angle = 0
