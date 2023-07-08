# from math import *
# from random import *
# from time import *
from copy import deepcopy


# ! Move map borders here ?
class Level:                                                                    # Create a level for the game
    def __init__(self, depth=1, color_name="blue", color=(50, 180, 255), music_name=None):
        self.depth = 1 if depth < 1 else depth
        self.color_name = color_name
        self.color = self.CheckColorValue(color)
        self.start_color, self.end_color = self.setEndColor(self.color)
        self.music_name = f"musics/{self.color_name}.mp3" if music_name is None else f"musics/{music_name}.mp3"
        self.nb_cells = int(self.depth * 100)
        self.nb_cells_max = int(self.depth * 100)
        self.nb_enemy = int(self.depth * 10)
        self.nb_enemy_max = int(self.depth * 10)
        self.nb_life = int(self.nb_enemy_max * 0.5)
        self.nb_life_max = int(self.nb_enemy_max * 0.5)
        self.map_size = [self.nb_cells_max * 30, self.nb_cells_max * 20]        # In pixels

    def present(self):                                                          # Present the level
        print(f"'{self.color_name}' {self.color} : lvl {self.depth}, {self.nb_cells} / {self.nb_cells_max} cells")

    @staticmethod
    def CheckColorValue(color):                                                 # Check if the colors values are correct
        color = list(color)
        color[0] = 0 if color[0] < 0 else 255 if color[0] > 255 else color[0]
        color[1] = 0 if color[1] < 0 else 255 if color[1] > 255 else color[1]
        color[2] = 0 if color[2] < 0 else 255 if color[2] > 255 else color[2]
        return tuple(color)

    @staticmethod
    def setEndColor(color):                                                     # Set start color and end color of level
        color = list(color)
        rgb_min = color.index(min(color))
        rgb_max = color.index(max(color))
        if rgb_min == rgb_max:                                                  # Si valeur similaire
            color_bis = deepcopy(color)
            color_bis.remove(color[rgb_min])
            rgb_max = color.index(max(color_bis))
        color_bis = deepcopy(color)
        color_bis.remove(color[rgb_min])
        color_bis.remove(color[rgb_max])
        rgb_median = color.index(color_bis[0])
        start_color = [0, 0, 0]
        start_color[rgb_min] = int(color[rgb_min] * 1.5) if int(color[rgb_min] * 1.5) <= 255 else 255
        start_color[rgb_median] = int(color[rgb_median] * 1.5) if int(color[rgb_median] * 1.5) <= 255 else 255
        start_color[rgb_max] = int(color[rgb_max] * 1.5) if int(color[rgb_max] * 1.5) <= 255 else 255
        for index, clr in enumerate(color):
            if clr == color[rgb_median]:
                start_color[index] = int(color[rgb_median] * 1.5) if int(color[rgb_median] * 1.5) <= 255 else 255
        end_color = [int(color[0] * 0.2), int(color[1] * 0.2), int(color[2] * 0.2)]
        return tuple(start_color), tuple(end_color)
