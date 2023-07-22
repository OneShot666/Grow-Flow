from math import sqrt
# from random import *
# from time import *
from bubble import Bubble, CellEaten
import pygame


# ! [later] Upgrade function Attack()
# ! [later] Add function Evolve() (modify appearance)
class Player(Bubble):                                                           # Player in the game
    def __init__(self, x=0, y=0, map_borders=None, screen_size=None, size=100, color=(216, 216, 216),
                 name="Player", length=1, speed=20, *groups):
        super().__init__(x, y, map_borders, size, color, speed, *groups)
        self.is_dead = False
        self.name = name
        self.group = groups
        self.Methods = ["mouse", "keyboard"]
        self.move_method = self.Methods[0]                                      # Mouse movement by default
        self.screen_size = screen_size
        self.evolution = 0                                                      # ! [later] Appearance
        self.length = length                                                    # ! [later]

        self.max_diameter = size
        self.max_radius = int(size * 0.5)
        self.current_radius = int(self.max_radius * 0.5)
        self.current_diameter = self.current_radius * 2
        self.screen_pos = (int(self.screen_size[0] * 0.5 - self.current_radius), int(self.screen_size[1] * 0.5 - self.current_radius))

        self.life = 100
        self.life_max = 100
        self.cells_eaten = 0
        self.cells_eaten_max = 1                                                # Depends on nb of cells in level
        self.stomach_capacity = 10
        self.Stomach = []                                                       # [later] Use as money ?

        self.life_color = (45, 240, 115)
        self.life_color_bg = (30, 160, 75)
        self.cell_color = (255, 230, 25)
        self.cell_color_bg = (255, 250, 225)

        self.membrane_width = int(self.current_radius * 0.1)                    # Cellular membrane of player
        self.image = None
        self.reflect_surface = None
        self.set_image(self.current_radius)
        self.rect = self.image.get_rect()
        self.rect.x = self.set_position_x() if x == 0 else x
        self.rect.y = self.set_position_y() if y == 0 else y

    def setName(self, name=None):                                                     # Set player name
        self.name = "Player" if name is None else name

    def set_position_x(self):                                                   # Put player in middle of map
        return int(self.map_borders[0] + self.map_borders[2] * 0.5 - self.current_radius)

    def set_position_y(self):                                                   # //
        return int(self.map_borders[1] + self.map_borders[3] * 0.5 - self.current_radius)

    def set_image(self, radius=None):
        radius = self.current_radius if radius is None else radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        pygame.draw.circle(self.image, self.color_border, (radius, radius), radius, self.membrane_width)
        self.reflect_surface = pygame.Surface((int(radius * 0.3), int(radius * 0.6)), pygame.SRCALPHA)
        pygame.draw.ellipse(self.reflect_surface, self.color_reflect,
                            (0, 0, self.reflect_surface.get_width(), self.reflect_surface.get_height()))
        self.reflect_surface = pygame.transform.rotate(self.reflect_surface, -45)   # Rotate surface
        self.image.blit(self.reflect_surface, (radius * 0.3, radius * 0.3))

    def set_cells_eaten_max(self, value=0):                                     # Change nb of cells player can eat
        self.cells_eaten_max = value

    def ChangeLevel(self):                                                      # Adapt player to next level
        self.evolution += 1
        self.cells_eaten = 0
        self.Stomach = []
        self.current_radius = int(self.max_radius * 0.5)
        self.current_diameter = self.current_radius * 2
        self.screen_pos = (int(self.screen_size[0] * 0.5 - self.current_radius), int(self.screen_size[1] * 0.5 - self.current_radius))
        self.membrane_width = int(self.current_radius * 0.1)
        self.rect.x = self.set_position_x()
        self.rect.y = self.set_position_y()
        self.set_image()

    def Eat(self):
        self.cells_eaten += 1
        self.current_radius += self.cells_eaten / self.cells_eaten_max * (self.max_radius - self.current_radius)  # Grow
        self.current_diameter = self.current_radius * 2
        self.membrane_width = int(self.current_radius * 0.1)
        self.screen_pos = (int(self.screen_size[0] * 0.5 - self.current_radius), int(self.screen_size[1] * 0.5 - self.current_radius))
        self.set_image(self.current_radius)

        if len(self.Stomach) < self.stomach_capacity:
            self.Stomach.append(CellEaten(player=self))
        for cell in self.Stomach:
            cell.set_player_radius(self.current_radius)

    def Attack(self):                                                           # ! [later] Add damage, defense, skills...
        pass

    def GainLife(self, amount=0):
        self.life += amount
        if self.life >= self.life_max:
            self.life = self.life_max

    def TakeDamage(self, amount=0):
        self.life -= amount
        if self.life <= 0:
            self.life = 0
            self.death_sound.play()
            self.is_dead = True

    def ChangeMovementMethod(self):                                             # Change the movement type of the player
        self.move_method = self.Methods[0] if self.move_method == self.Methods[1] else self.Methods[1]

    # Manage the movements in the game
    def MovementManager(self, map_borders, screen_size, pressed=None, Cells=None, LifeBubbles=None, Enemies=None):
        if self.move_method == self.Methods[0]:
            self.MoveWithMouse(screen_size)
        elif self.move_method == self.Methods[1]:
            self.MoveWithKeyboard(pressed)

        self.CheckBordersCollision(map_borders)
        self.CheckCellsCollision(Cells)
        self.CheckLifeBubblesCollision(LifeBubbles)
        self.CheckEnemiesCollision(Enemies)

    def MoveWithMouse(self, screen_size=None, goal_pos=None):                   # Go to the mouse position
        if screen_size is None:
            screen_info = pygame.display.Info()
            screen_size = [screen_info.current_w, screen_info.current_h]
        if goal_pos is None:
            goal_pos = pygame.mouse.get_pos()

        if 0 <= goal_pos[0] <= screen_size[0] and 0 <= goal_pos[1] <= screen_size[1]:
            goal_x = goal_pos[0] - self.current_radius
            goal_y = goal_pos[1] - self.current_radius
            pos_x = screen_size[0] // 2 - self.current_radius
            pos_y = screen_size[1] // 2 - self.current_radius
            dx = goal_x - pos_x                                                 # Calculate distance player-mouse
            dy = goal_y - pos_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5

            if distance <= self.current_radius:                                 # Mouse on player
                speed = 0
            elif self.current_radius < distance < self.diameter * 1.5:          # Make dynamic speed
                speed = (distance - self.current_radius) / self.diameter * self.speed   # Percent x Speed
            else:                                                               # Max speed
                speed = self.speed

            if distance != 0:
                self.dir_x = (dx / distance) * speed
                self.dir_y = (dy / distance) * speed
            self.rect.x += self.dir_x
            self.rect.y += self.dir_y

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
        self.dir_x = (dir_x / distance) * self.speed if distance != 0 else 0
        self.dir_y = (dir_y / distance) * self.speed if distance != 0 else 0
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y

    def check_touch_circle(self, circle):
        return sqrt((circle.rect.x + circle.radius - self.rect.x - self.current_radius) ** 2 +
                    (circle.rect.y + circle.radius - self.rect.y - self.current_radius) ** 2) <= self.current_radius - circle.radius

    def CollideBubble(self, bubble):
        distance = self.get_min_distance(self, bubble)
        if distance <= int(bubble.radius * 0.5):                                # Prevent player from eating bubble
            bubble.rect.x += self.current_radius if self.rect.x < bubble.rect.x else - self.current_radius
            bubble.rect.y += self.current_radius if self.rect.y < bubble.rect.y else - self.current_radius

    def CheckCellsCollision(self, Cells=None):                                  # Check if eat cells
        if Cells is None:
            return

        for cell in Cells:
            if self.check_touch_circle(cell):
                self.Eat()
                cell.SelfDestruction()
                Cells.remove(cell)

    def CheckLifeBubblesCollision(self, LifeBubbles=None):                      # Check if eat life-bubbles
        if LifeBubbles is None:
            return

        for life_bubble in LifeBubbles:
            if self.check_touch_circle(life_bubble):
                if self.life < self.life_max:                                   # Prevent player from wasting healing
                    self.GainLife(life_bubble.life_gain)
                    life_bubble.SelfDestruction()
                    LifeBubbles.remove(life_bubble)
                else:
                    self.CollideBubble(life_bubble)

    def CheckEnemiesCollision(self, Enemies=None):                              # Check if can eat enemies
        if Enemies is None:
            return

        for enemy in Enemies:
            if self.check_touch_circle(enemy):
                if self.current_radius >= enemy.radius * 1.5:                   # Prevent player from taking damage
                    self.TakeDamage(enemy.damage)
                    enemy.SelfDestruction()
                    Enemies.remove(enemy)
                else:
                    self.CollideBubble(enemy)
