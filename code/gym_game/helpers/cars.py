import pygame
import math
import random

class AbstractCar:
    def __init__(self, top_speed, turn_rate):
        # sprite setup for the car
        self.img = self.IMG
        self.x, self.y = (0,0) # * TEMPORARY POSITION, WILL CHANGE AT THE RESET OF THE CAR.
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.img)

        # variables of the car
        self.vel = 0
        self.angle = 0
        self.angle_line = -90

        # constants of the car
        self.topSpeed = top_speed
        self.turnRate = turn_rate
        self.acceleration = 0.05

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.turnRate
            self.angle_line -= self.turnRate
        if right:
            self.angle -= self.turnRate
            self.angle_line += self.turnRate

    def increase_velocity(self):
        if self.vel <= self.topSpeed:
            self.vel += 0.1

    def decrease_velocity(self):
        if self.vel > 0:
            self.vel -= 0.2

        if self.vel < 0:
            self.vel = 0

    def move(self):
        # radians: 180 (degrees) = pi, 360 (degrees) = 2pi
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        self.rect.x = self.x
        self.rect.y = self.y

    # rotate a point around another point
    def rotate_point(self, point, angle_deg, origin):
        angle_rad = math.radians(angle_deg)
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
        qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
        return round(qx), round(qy)

    def draw(self, screen):
        #pygame.draw.rect(screen, "black" , self.rect)

        color_circle = (255,102,102)
        radius_circle = 15
        pygame.draw.circle(screen, color_circle, (self.rect.centerx, self.rect.centery), radius_circle)

        color_line = "black"
        line_length = 15
        start_line = (self.rect.centerx-1, self.rect.centery)
        end_line = (start_line[0]+line_length, start_line[1])
        rotated_end_point = self.rotate_point(end_line, self.angle_line, start_line)
        pygame.draw.line(screen, color_line, start_line, rotated_end_point, width=2)


    def reset(self, random_pos_start):
        self.vel = 0
        self.angle = 0
        self.angle_line = -90

        self.x, self.y = random_pos_start
        self.rect.x, self.rect.y = random_pos_start

    def collisions(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True


class Player(AbstractCar):
    IMG = pygame.Surface((30, 30))
    START_POS = (200, 180)

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
    IMG = pygame.Surface((30, 30))
    START_POS = [
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
            self.move()
        elif action == 2: # decelerate 
            self.decrease_velocity()
            self.move()
        elif action == 3: # steer right
            self.rotate(right=True)
        elif action == 4: # steer left
            self.rotate(left=True)

    def get_random_start_pos(self):
        return random.choice(self.START_POS)