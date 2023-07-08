from math import *
from random import *
# from time import *
import pygame


# ! Add draw() here ? (+ blur effets ?) + make it one image
class Bubble(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, map_borders=None, size=16, color=(250, 240, 210), speed=5, *groups):
        super().__init__(*groups)
        self.show_dir = False
        self.group = groups
        self.map_borders = self.set_map_borders() if map_borders is None else map_borders
        self.diameter = size
        self.radius = size // 2
        self.membrane_width = int(self.diameter * 0.1)                          # Largeur du bord de l'anneau
        self.speed = speed
        self.dir_x = randint(-self.speed, self.speed)
        self.dir_y = randint(-self.speed, self.speed)
        self.transparence = 176
        self.transparence_border = self.transparence + 40
        self.transparence_reflect = self.transparence - 40
        self.color = (*color, self.transparence)
        self.color_border = self.set_color_border()
        self.color_reflect = self.set_color_reflect()
        self.image = None
        self.reflect_surface = None
        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.x = self.set_position_x() if x == 0 else x
        self.rect.y = self.set_position_y() if y == 0 else y

    @staticmethod
    def set_map_borders():
        screen_info = pygame.display.Info()
        return 0, 0, screen_info.current_w, screen_info.current_h

    def set_color_border(self):
        color = [0, 0, 0]
        for i in range(3):
            new = int(self.color[i] * 1.25)
            color[i] = 255 if new > 255 else new
        return *color, self.transparence_border

    def set_color_reflect(self):
        color = [0, 0, 0]
        for i in range(3):
            new = int(self.color[i] * 1.5)
            color[i] = 255 if new > 255 else new
        return *color, self.transparence_reflect

    def set_position_x(self):
        return randint(self.map_borders[0], self.map_borders[2] - self.diameter)

    def set_position_y(self):
        return randint(self.map_borders[1], self.map_borders[3] - self.diameter)

    def set_image(self):
        self.image = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, self.color_border, (self.radius, self.radius), self.radius, self.membrane_width)
        self.reflect_surface = pygame.Surface((int(self.diameter * 0.15), int(self.diameter * 0.3)), pygame.SRCALPHA)
        pygame.draw.ellipse(self.reflect_surface, self.color_reflect,
                            (0, 0, self.reflect_surface.get_width(), self.reflect_surface.get_height()))
        self.reflect_surface = pygame.transform.rotate(self.reflect_surface, -45)                       # Rotate surface
        self.image.blit(self.reflect_surface, (self.radius * 0.35, self.radius * 0.35))

    @staticmethod
    def get_min_distance(circle1, circle2):
        dx = (circle2.rect.x + circle2.dir_x) - (circle1.rect.x + circle1.dir_x)    # Calcule future pos
        dy = (circle2.rect.y + circle2.dir_y) - (circle1.rect.y + circle1.dir_y)
        return sqrt(dx ** 2 + dy ** 2) - circle1.radius - circle2.radius

    def update(self, circles):                                                  # Need to be lower to work in main
        self.Move()
        self.CheckBubbleCollision(circles)
        self.CheckBordersCollision()

    def Move(self):                                                             # Random bubble movements (upgrade later)
        self.dir_x = randint(-self.speed, self.speed)
        self.dir_y = randint(-self.speed, self.speed)
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y

    def CheckBubbleCollision(self, circles=None):
        if circles is None:
            circles = []

        # Vérifie les collisions avec les autres cercles
        for circle in circles:
            distance = self.get_min_distance(self, circle)
            if circle is not self:
                if distance <= 0:
                    dx = self.rect.x - circle.rect.x
                    dy = self.rect.y - circle.rect.y
                    angle = atan2(dy, dx)                                       # Direction vecteur entre centres cercles
                    overlap = -distance / 2                                     # Distance de chevauchement entre cercles

                    # Déplace les cercles pour les séparer
                    self.rect.x += cos(angle) * overlap
                    self.rect.y += sin(angle) * overlap
                    circle.rect.x -= cos(angle) * overlap
                    circle.rect.y -= sin(angle) * overlap

    def CheckBordersCollision(self, map_borders=None):                          # Keep bubble in map
        if map_borders is None:
            map_borders = self.map_borders

        if self.rect.x < map_borders[0]:
            self.rect.x = map_borders[0]
        if self.rect.x > map_borders[2] - self.radius:
            self.rect.x = map_borders[2] - self.radius
        if self.rect.y < map_borders[1]:
            self.rect.y = map_borders[1]
        elif self.rect.y > map_borders[3] - self.radius:
            self.rect.y = map_borders[3] - self.radius

    def SelfDestruction(self):                                                  # !! Untested yet
        del self


class LifeBubble(Bubble):
    def __init__(self, x=0, y=0, map_borders=None, size=24, color=(120, 250, 30), life_gain=25, speed=2, *groups):
        super().__init__(x, y, map_borders, size, color, speed, *groups)
        self.rect.x = self.set_position_x() if x == 0 else x
        self.rect.y = self.set_position_y() if y == 0 else y
        self.life_gain = life_gain


# ! Add attack player function in range
class Enemy(Bubble):
    def __init__(self, x=0, y=0, map_borders=None, size=40, color=(250, 60, 60), life=50, damage=5, speed=10, *groups):
        super().__init__(x, y, map_borders, size, color, speed, *groups)
        self.rect.x = self.set_position_x() if x == 0 else x
        self.rect.y = self.set_position_y() if y == 0 else y
        self.life = life
        self.damage = damage
