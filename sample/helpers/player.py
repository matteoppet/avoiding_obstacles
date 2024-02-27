import pygame

class Player:
    def __init__(self):
        super().__init__()
        # decide if give the pos and size when it is called or inside the init function
        # ... for now give them inside the init function
        pos = (100, 100) # topleft
        size = (50, 20)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.image.fill("#9381ff") # color the rect