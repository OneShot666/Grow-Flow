from math import sqrt
# from random import *
# from time import *
import pygame


class Player:
    def __init__(self, name="Player", size=None, screen_size=None, position=None, length=1, speed=20, color=(255, 255, 255),
                 color_name="white"):
        self.Methods = ["mouse", "keyboard"]
        self.move_method = self.Methods[0]
        self.name = name
        self.size = [100, 100] if size is None else size
        self.screen_size = self.set_screen_size() if screen_size is None else screen_size
        self.pos_x = int(self.screen_size[0] * 0.5 - self.size[0] * 0.5) if position is None else position[0]
        self.pos_y = int(self.screen_size[1] * 0.5 - self.size[1] * 0.5) if position is None else position[1]
        self.life = 100
        self.life_max = 100
        self.life_color = (45, 240, 115)
        self.life_color_bg = (30, 160, 75)
        self.cells_nb = 0                                                       # ! [later]
        self.cells_nb_max = 10                                                  # ! [later]
        self.length = length                                                    # ! [later]
        self.image_name = f"images/player.png"
        self.image = pygame.image.load(f"images/player.png")
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.width = int(self.size[0] / 20)                                     # Largeur du bord de l'anneau
        self.speed = speed
        self.color = color
        self.color_name = color_name

    @staticmethod
    def setName(name):
        if name == "Player":
            name = input("Entrez votre nom : ")
        return name

    @staticmethod
    def set_screen_size():
        screen_info = pygame.display.Info()
        return [screen_info.current_w, screen_info.current_h]

    def ChangeMovementMethod(self):
        self.move_method = self.Methods[0] if self.move_method == self.Methods[1] else self.Methods[1]

    def MovementManager(self, screen_size=None, pressed=None):
        if screen_size is None:
            screen_size = self.screen_size

        if self.move_method == self.Methods[0]:
            self.MoveWithMouse()
        elif self.move_method == self.Methods[1]:
            self.MoveWithKeyboard(pressed)

        self.CheckScreenCollision(screen_size)

    def MoveWithMouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        goal_x = mouse_x - self.size[0] // 2
        goal_y = mouse_y - self.size[1] // 2
        # Calcul de la distance en x et y entre le joueur et la position de la souris
        dx = goal_x - self.pos_x
        dy = goal_y - self.pos_y
        distance = max(abs(dx), abs(dy))

        if distance <= self.speed:                                              # Si dépasse objectif, va directement dessus
            self.pos_x = goal_x
            self.pos_y = goal_y
        else:                                                                   # Sinon, va vers souris
            direction_x = dx / distance
            direction_y = dy / distance
            self.pos_x += direction_x * self.speed
            self.pos_y += direction_y * self.speed

    def MoveWithKeyboard(self, pressed=None):
        dir_x = 0
        dir_y = 0
        if pressed is None:
            pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:                                                # Player movements (with arrows)
            dir_y -= 1
        elif pressed[pygame.K_DOWN]:
            dir_y += 1
        if pressed[pygame.K_LEFT]:
            dir_x -= 1
        elif pressed[pygame.K_RIGHT]:
            dir_x += 1

        distance = sqrt(dir_x ** 2 + dir_y ** 2)                                # Calcul distance à parcourir
        if distance != 0:
            dir_x /= distance                                                   # Calcul new direction de déplacement
            dir_y /= distance
            self.pos_x += dir_x * self.speed                                    # Mise à jour position
            self.pos_y += dir_y * self.speed

    def CheckScreenCollision(self, screen_size=None):
        if screen_size is None:
            screen_size = self.screen_size

        if self.pos_x < 0:
            self.pos_x = 0
        if self.pos_x > screen_size[0] - self.size[0]:
            self.pos_x = screen_size[0] - self.size[0]
        if self.pos_y < 0:
            self.pos_y = 0
        elif self.pos_y > screen_size[1] - self.size[1]:
            self.pos_y = screen_size[1] - self.size[1]
