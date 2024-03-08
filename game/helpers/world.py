import pygame

COLOR = (91, 155, 69)
obstacle_sprites_group = pygame.sprite.Group()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, info_rect, group):
        super().__init__(group)

        x, y, width, height = info_rect

        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)

class World:
    def __init__(self, win):
        self.win = win

    def create_rect(self, info_rect):
        Obstacle(info_rect, obstacle_sprites_group)

    def draw_rects(self):
        for sprite in obstacle_sprites_group:
            pygame.draw.rect(self.win, COLOR, sprite.rect)