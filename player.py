# from math import *
# from random import *
# from time import *
import pygame


class Player:
    def __init__(self, name="Player", size=None, screen_size=None, position=None, length=1, speed=20, color=(255, 255, 255),
                 color_name="white"):
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

    def Move(self, direction, screen_size=None):
        if screen_size is None:
            screen_size = self.screen_size
        if direction == "up":
            if self.pos_y - self.speed < 0:
                self.pos_y = 0
            else:
                self.pos_y -= self.speed
        elif direction == "down":
            if self.pos_y + self.speed > screen_size[1] - self.size[1]:
                self.pos_y = screen_size[1] - self.size[1]
            else:
                self.pos_y += self.speed
        if direction == "left":
            if self.pos_x - self.speed < 0:
                self.pos_x = 0
            else:
                self.pos_x -= self.speed
        elif direction == "right":
            if self.pos_x + self.speed > screen_size[0] - self.size[0]:
                self.pos_x = screen_size[0] - self.size[0]
            else:
                self.pos_x += self.speed
