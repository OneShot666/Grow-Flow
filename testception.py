import pygame
from math import *
from random import *

""" Collision des bulles d'un même groupe """

pygame.init()
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Bubble royale")
clock = pygame.time.Clock()

# Couleurs
bg_color = (84, 210, 250)                                                       # Couleur de fond
Colors = [(234, 48, 39), (254, 156, 39), (242, 242, 34), (169, 252, 41), (41, 232, 44), (41, 252, 217), (41, 217, 252),
          (41, 124, 252), (36, 45, 238), (144, 46, 255), (204, 56, 252), (232, 56, 239), (196, 88, 22)]


class Bubble(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, size=None, dx=None, dy=None, color=None, show_dir=False, *groups):
        super().__init__(*groups)
        max_size = 50
        self.show_dir = show_dir
        self.diameter = size if size is not None else randint(int(max_size * 0.25), max_size)
        self.radius = int(self.diameter * 0.5)
        self.pos_x = x if x is not None else randint(self.radius, window_width - self.diameter)
        self.pos_y = y if y is not None else randint(self.radius, window_height - self.diameter)
        self.direction_x = dx if dx is not None else choice([-1, 1]) * randint(1, 3)
        self.direction_y = dy if dy is not None else choice([-1, 1]) * randint(1, 3)
        self.border_width = int(self.diameter * 0.05)
        # Colors
        self.color_transparent = 160
        self.border_transparent = self.color_transparent + 40
        self.reflect_transparent = self.color_transparent - 40
        self.color = self.check_color(color)
        self.border_color = self.set_border_color(self.color)
        self.reflect_color = self.set_reflect_color(self.color)
        self.arrow_color = self.reflect_color
        # Bubble
        self.bubble_surface = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)           # Surface of the bubble
        pygame.draw.circle(self.bubble_surface, self.color, (self.radius, self.radius), self.radius)    # Bulle remplie
        pygame.draw.circle(self.bubble_surface, self.border_color, (self.radius, self.radius), self.radius, self.border_width)  # Rebords de la bulle
        # Reflect
        self.reflect_surface = pygame.Surface((int(self.diameter * 0.12), int(self.diameter * 0.3)), pygame.SRCALPHA)
        reflect_size = (0, 0, self.reflect_surface.get_width(), self.reflect_surface.get_height())
        pygame.draw.ellipse(self.reflect_surface, self.reflect_color, reflect_size)                     # Dessine reflet
        self.reflect_surface = pygame.transform.rotate(self.reflect_surface, -45)                       # Tourne surface
        self.bubble_surface.blit(self.reflect_surface, (self.radius * 0.25, self.radius * 0.25))

    def check_color(self, checked_color):
        checked_color = list(checked_color)
        if len(checked_color) == 3:
            checked_color = [*checked_color, self.color_transparent]
        elif checked_color[3] != self.color_transparent:
            checked_color[3] = self.color_transparent
        return tuple(checked_color)

    def set_border_color(self, border_color):
        border_color = list(border_color)
        if len(border_color) == 3:
            border_color = [*border_color, self.border_transparent]
        elif border_color[3] != self.border_transparent:
            border_color[3] = self.border_transparent
        for i in range(3):
            border_color[i] = int(border_color[i] * 1.2)
            border_color[i] = 255 if border_color[i] > 255 else border_color[i]
        return tuple(border_color)

    def set_reflect_color(self, reflect_color):
        reflect_color = list(reflect_color)
        if len(reflect_color) == 3:
            reflect_color = [*reflect_color, self.reflect_transparent]
        elif reflect_color[3] != self.reflect_transparent:
            reflect_color[3] = self.reflect_transparent
        for i in range(3):
            reflect_color[i] = int(reflect_color[i] * 1.8)
            reflect_color[i] = 255 if reflect_color[i] > 255 else reflect_color[i]
        return tuple(reflect_color)

    @staticmethod
    def get_min_distance(circle1, circle2):
        dx = (circle2.pos_x + circle2.direction_x) - (circle1.pos_x + circle1.direction_x)          # Calcule future pos
        dy = (circle2.pos_y + circle2.direction_y) - (circle1.pos_y + circle1.direction_y)
        return sqrt(dx ** 2 + dy ** 2) - circle1.radius - circle2.radius

    def update(self, circles=None):
        if circles is None:
            circles = []

        # Vérifie les collisions avec les autres cercles
        for circle in circles:
            distance = self.get_min_distance(self, circle)
            if circle is not self:
                if distance <= 0:
                    dx = self.pos_x - circle.pos_x
                    dy = self.pos_y - circle.pos_y
                    angle = atan2(dy, dx)                                       # Direction vecteur entre centres cercles
                    overlap = -distance / 2                                     # Distance de chevauchement entre cercles

                    # Déplace les cercles pour les séparer
                    self.pos_x += cos(angle) * overlap
                    self.pos_y += sin(angle) * overlap
                    self.check_screen_collision()
                    circle.pos_x -= cos(angle) * overlap
                    circle.pos_y -= sin(angle) * overlap
                    circle.check_screen_collision()

        # Met à jour la position
        self.pos_x += self.direction_x
        self.pos_y += self.direction_y
        self.check_screen_collision()

    def check_screen_collision(self):                                           # Vérifie collisions avec bords de l'écran
        self.direction_x = 1 if self.pos_x - self.radius < 0 else -1 if self.pos_x + self.radius > window_width else self.direction_x
        self.direction_y = 1 if self.pos_y - self.radius < 0 else -1 if self.pos_y + self.radius > window_height else self.direction_y

    def draw(self):
        screen.blit(self.bubble_surface, (self.pos_x - self.radius, self.pos_y - self.radius))

        # reflect_surface_pos = (self.pos_x - self.radius * 0.75, self.pos_y - self.radius * 0.75)
        # screen.blit(self.reflect_surface, reflect_surface_pos)                       # Dessine surface tournée avec reflet

        if self.show_dir:
            percent_gap_circle = 1.5
            percent_arrow_width = 0.15
            percent_arrow_height = 2
            angle = atan2(self.direction_y, self.direction_x)                       # Direction cercle (en radian)
            line_start = (self.pos_x + self.radius * 0.8 * cos(angle), self.pos_y + self.radius * 0.8 * sin(angle))
            line_end = (self.pos_x + self.radius * percent_gap_circle * cos(angle), self.pos_y + self.radius * percent_gap_circle * sin(angle))
            pygame.draw.line(screen, self.arrow_color, line_start, line_end, int(self.radius // 10))    # Tige flèche
            point1 = (self.pos_x + self.radius * percent_gap_circle * cos(angle - percent_arrow_width),
                      self.pos_y + self.radius * percent_gap_circle * sin(angle - percent_arrow_width))
            point2 = (self.pos_x + self.radius * percent_gap_circle * cos(angle + percent_arrow_width),
                      self.pos_y + self.radius * percent_gap_circle * sin(angle + percent_arrow_width))
            point3 = (self.pos_x + self.radius * percent_arrow_height * cos(angle),
                      self.pos_y + self.radius * percent_arrow_height * sin(angle))
            pygame.draw.polygon(screen, self.arrow_color, [point1, point2, point3])


# Créer des bulles
objects = []
nb_objet = 10 if len(Colors) <= 10 else len(Colors)
for _ in range(nb_objet):
    color = choice(Colors)
    objects.append(Bubble(color=color))
    Colors.remove(color)

running = True
pausing = False
fps = 100
old_pfs = fps
print(f"{fps}fps")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pausing = not pausing

            if event.key == pygame.K_j:
                fps -= 10
                old_pfs = fps
                print(f"{fps}fps")
            elif event.key == pygame.K_l:
                fps += 10
                old_pfs = fps
                print(f"{fps}fps")

            if event.key == pygame.K_q:
                running = False

    pressed = pygame.key.get_pressed()
    fps = 20 if pressed[pygame.K_k] else old_pfs

    screen.fill(bg_color)

    for obj in objects:                                                         # Met à jour et dessine tous les objets
        if not pausing:
            obj.update(objects)
        obj.draw()

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
