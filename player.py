from math import sqrt
# from random import *
# from time import *
from bubble import Bubble
import pygame


# ! [later] Upgrade functions Eat() + Attack()
# ! [later] Add function Evolve() (modify appearance + lenght of player)
class Player(Bubble):                                                           # Player in the game
    def __init__(self, x=0, y=0, map_borders=None, size=100, color=(216, 216, 216), name="Player", bg_size=None,
                 length=1, speed=20, *groups):
        super().__init__(x, y, map_borders, size, color, speed, *groups)
        self.name = name
        self.group = groups
        self.Methods = ["mouse", "keyboard"]
        self.move_method = self.Methods[0]                                      # Mouse movement by default
        self.evolution = 0                                                      # ! [later]
        self.length = length                                                    # ! [later]
        self.life = 100
        self.life_max = 100
        self.cells_eaten = 0
        self.cells_eaten_max = 0                                                # Depends on nb of cells in level
        self.life_color = (45, 240, 115)
        self.life_color_bg = (30, 160, 75)
        self.cell_color = (255, 230, 25)
        self.cell_color_bg = (255, 250, 225)

        self.membrane_width = int(self.diameter * 0.05)                         # Cellular membrane of player
        self.image = None
        self.reflect_surface = None
        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.x = self.set_position_x() if x == 0 else x
        self.rect.y = self.set_position_y() if y == 0 else y

    @staticmethod
    def setName(name):                                                          # Set player name ([later] move in menu)
        if name in ["Player", "", None]:
            name = input("Entrez votre nom : ")
        return name

    def set_position_x(self):                                                   # Put player in middle of map
        return int(self.map_borders[0] + self.map_borders[2] * 0.5 - self.radius)

    def set_position_y(self):                                                   # Same
        return int(self.map_borders[1] + self.map_borders[3] * 0.5 - self.radius)

    def set_image(self):
        self.image = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, self.color_border, (self.radius, self.radius), self.radius, self.membrane_width)
        self.reflect_surface = pygame.Surface((int(self.diameter * 0.15), int(self.diameter * 0.3)), pygame.SRCALPHA)
        pygame.draw.ellipse(self.reflect_surface, self.color_reflect,
                            (0, 0, self.reflect_surface.get_width(), self.reflect_surface.get_height()))
        self.reflect_surface = pygame.transform.rotate(self.reflect_surface, -45)                       # Rotate surface
        self.image.blit(self.reflect_surface, (self.radius * 0.3, self.radius * 0.3))

    def set_cells_eaten_max(self, value=0):                                     # Change nb of cells player can eat
        self.cells_eaten_max = value

    def ChangeLevel(self):                                                      # Adapt player to next level
        if self.cells_eaten >= self.cells_eaten_max:
            self.evolution += 1
            self.cells_eaten = 0
            self.life = self.life_max
        self.rect.x = self.set_position_x()
        self.rect.y = self.set_position_y()

    def Eat(self):
        self.cells_eaten += 1

    def Attack(self):                                                           # ! [later] Add damage, defense, skills...
        pass

    def ChangeMovementMethod(self):                                             # Change the movement type of the player
        self.move_method = self.Methods[0] if self.move_method == self.Methods[1] else self.Methods[1]

    def MovementManager(self, map_borders, screen_size=None, pressed=None):     # Manage the movements in the game
        if self.move_method == self.Methods[0]:
            self.MoveWithMouse(screen_size)
        elif self.move_method == self.Methods[1]:
            self.MoveWithKeyboard(pressed)

        self.CheckBordersCollision(map_borders)

    def MoveWithMouse(self, screen_size=None, goal_pos=None):                   # Go to the mouse position
        if screen_size is None:
            screen_info = pygame.display.Info()
            screen_size = [screen_info.current_w, screen_info.current_h]
        if goal_pos is None:
            goal_pos = pygame.mouse.get_pos()

        if 0 <= goal_pos[0] <= screen_size[0] and 0 <= goal_pos[1] <= screen_size[1]:
            goal_x = goal_pos[0] - self.radius
            goal_y = goal_pos[1] - self.radius
            pos_x = screen_size[0] // 2 - self.radius
            pos_y = screen_size[1] // 2 - self.radius
            dx = goal_x - pos_x                                                 # Calculate distance player-mouse
            dy = goal_y - pos_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5

            if distance <= self.radius:                                         # Mouse on player
                speed = 0
            elif self.radius < distance < self.diameter * 1.5:                  # Make dynamic speed
                speed = (distance - self.radius) / self.diameter * self.speed   # Percent x Speed
            else:                                                               # Max speed
                speed = self.speed

            if distance != 0:
                self.rect.x += (dx / distance) * speed
                self.rect.y += (dy / distance) * speed

    def MoveWithKeyboard(self, pressed=None):                                   # Move player with arrows
        if pressed is None:
            pressed = pygame.key.get_pressed()
        dir_x = 0
        dir_y = 0
        if pressed[pygame.K_z]:                                                 # Player movements
            dir_y -= 1
        elif pressed[pygame.K_s]:
            dir_y += 1
        if pressed[pygame.K_q]:
            dir_x -= 1
        elif pressed[pygame.K_d]:
            dir_x += 1

        distance = sqrt(dir_x ** 2 + dir_y ** 2)                                # Calculate distance to go
        if distance != 0:
            self.rect.x += (dir_x / distance) * self.speed                      # Update position
            self.rect.y += (dir_y / distance) * self.speed
