# from math import *
from random import *
# from time import *
import pygame


# ! Add can merge together
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, map_borders=None, x=0, y=0, size=1, color=(167, 195, 219), *groups):
        super().__init__(*groups)
        self.group = groups
        self.map_borders = self.set_map_borders() if map_borders is None else map_borders
        self.size = size
        self.radius_max = 50                                                    # In pixels
        self.nb_circle = randint(3, 8)
        self.height = self.radius_max * self.nb_circle * 0.5
        self.width = self.radius_max * self.nb_circle * 0.5
        self.transparence = 176
        self.color = (*color, self.transparence)
        self.image = None
        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.x = self.set_position_x() if x == 0 else x
        self.rect.y = self.set_position_y() if y == 0 else y
        self.dir_x = 0
        self.dir_y = 0
        self.speed = randint(1, 3)

    @staticmethod
    def set_map_borders():
        screen_info = pygame.display.Info()
        return 0, 0, screen_info.current_w, screen_info.current_h

    def set_position_x(self):
        return randint(self.map_borders[0], self.map_borders[2])

    def set_position_y(self):
        return randint(self.map_borders[1], self.map_borders[3])

    def set_image(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for _ in range(self.nb_circle):
            radius = randint(10, self.radius_max)
            x = randint(radius, self.width - radius)
            y = randint(radius, self.height - radius)
            pygame.draw.circle(self.image, self.color, (x, y), radius)

    def Merge(self):
        pass

    def Move(self):                                                             # Gradually slows down
        if self.dir_x > 0:
            self.dir_x -= 1
        elif self.dir_x < 0:
            self.dir_x += 1
        if self.dir_y > 0:
            self.dir_y -= 1
        elif self.dir_y < 0:
            self.dir_y += 1

        self.rect.x += self.speed * self.dir_x
        self.rect.y += self.speed * self.dir_y
