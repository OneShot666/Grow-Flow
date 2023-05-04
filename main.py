# from math import *
# from random import *
from time import time
from os import getcwd
from player import Player
from level import Level
import pygame
import sys


# !! [0.2.5] Modifier vitesse player en diagonale
# ! [0.2.5] Replace red.mp3 (music)
# ! [0.2.5] Replace orange.mp3 & green.mp3 ?
# ! [0.2.5] Make SoundManager() work
# ! [later: 0.5.0] Add move player (avec souris) + centrer camera
# ! [later: 0.5.0] Add spawn cells (food) + grow player (food_counter: level)
# ! [later: 0.5.0] Add change background & music avec fleches et souris
# ! [later: 0.5.0] Add condition pour accéder aux autres musiques / level (taille)
# ! [later: 1.0.0] Add parameter (choose manière de bouger, de changer fond, Commandes, Credits, ...)
# ! [later: 1.0.0] Add effects (flou, rayons, bulles, creatures au fond ?)
# ! [later: 1.0.0] Add comms en anglais + documentation
# ! [later: 1.5.0] Add enemies + dégâts
# ! [later: 1.5.0] Add saves
class Game:                                                                     # Main class of the game
    def __init__(self):
        # Load and game data
        pygame.init()
        self.running = True
        self.game_name = "Grow Flow"
        self.creator = "One Shot"
        self.version = "v0.2.1"
        print(f"Bienvenue sur {self.game_name} ! ({self.version})\n")
        pygame.display.set_caption(self.game_name)                              # Lector name
        self.icon = pygame.image.load("images/icon.png")                        # Game icon
        self.icon.set_colorkey((255, 255, 255))                                 # Remove white background
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)                                      # Lector icon
        # Gameplay data
        self.path = getcwd()
        self.horloge = pygame.time.Clock()                                      # Manage the fps
        self.pressed = pygame.key.get_pressed()
        self.fps = 20
        # Fonts
        self.font_name = "Fillaflow.ttf"
        self.title_font = pygame.font.Font(f"fonts/{self.font_name}", 100)
        self.text_font = pygame.font.Font(f"fonts/{self.font_name}", 25)
        # Main colors
        self.Color_names = ["blue", "green", "cyan", "orange", "red", "pink",
                            "purple", "nightblue", "black", "brown", "yellow", "white"]
        self.Color_value = [(0, 160, 225), (50, 250, 130), (55, 255, 255), (250, 140, 40), (255, 60, 50), (255, 110, 210),
                            (190, 80, 225), (100, 40, 255), (55, 25, 125), (155, 90, 30), (255, 250, 45), (240, 240, 220)]
        self.background_color_name = None
        self.bg_start_color = None
        self.bg_end_color = None
        self.color_white = (255, 255, 255, 255)
        self.color_black = (0, 0, 0, 0)
        # Main music
        self.song_name = f"musics/subnautica.mp3"
        self.play_mode = -1
        self.sound = 0.5
        # Screen data
        screen_info = pygame.display.Info()
        self.screen_height = screen_info.current_h                              # Hauteur de l'écran
        self.screen_width = screen_info.current_w                               # Longueur de l'écran
        self.size = [self.screen_width, self.screen_height]
        self.second_size = [int(self.screen_width * 0.5), int(self.screen_height * 0.5)]
        self.current_size = self.size
        self.screen = pygame.display.set_mode(self.current_size)                        # Display window with bg image size
        # Game timers
        self.time_now = time()
        self.last_time_change_screen_size = 0
        self.delay_change_screen_size = 0.5
        # Game variables
        self.player = Player()
        self.title_image = None
        self.background = None
        self.player_body = None
        self.Levels = []
        self.level_index = 0
        # Game main functions
        self.LoadComposants()
        self.Run()

    def LoadComposants(self):                                                   # Load the composants of the game
        print(f"Chargement des composants du jeu en cours...")
        self.title_image = pygame.image.load(f"images/title.png")
        title_size = self.title_image.get_size()
        new_title_height = int(self.current_size[0] * 0.25 / title_size[0] * title_size[1])
        self.title_image = pygame.transform.scale(self.title_image, (self.current_size[0] * 0.25, new_title_height))
        self.background = pygame.image.load(f"images/background.png")
        self.background = pygame.transform.scale(self.background, self.current_size)
        self.LoadLevel()
        self.background_color_name = self.Levels[self.level_index].color_name
        self.bg_start_color = self.Levels[self.level_index].start_color
        self.bg_end_color = self.Levels[self.level_index].end_color
        self.song_name = f"musics/{self.background_color_name}.mp3"
        print(f"Chargement des composants du jeu terminé !\n")

    def LoadLevel(self):                                                        # Load the level of the game
        print(f"Chargement des niveaux du jeu en cours...")
        for index, color_name in enumerate(self.Color_names):
            niveau = Level(index + 1, color_name, self.Color_value[index])
            self.Levels.append(niveau)
        print(f"Chargement des niveaux du jeu terminé !")

    def Run(self):                                                              # Manage the game
        while self.running:
            self.Update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.CloseGame()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:                             # ! [later] Replace by auto change level
                        self.ChangeLevel()

            self.pressed = pygame.key.get_pressed()
            if self.pressed[pygame.K_UP]:                                       # Player movements (with arrows)
                self.player.Move("up", self.current_size)
            elif self.pressed[pygame.K_DOWN]:
                self.player.Move("down", self.current_size)
            if self.pressed[pygame.K_LEFT]:
                self.player.Move("left", self.current_size)
            elif self.pressed[pygame.K_RIGHT]:
                self.player.Move("right", self.current_size)

            if self.pressed[pygame.K_LCTRL]:
                self.time_now = time()
                if self.time_now - self.last_time_change_screen_size > self.delay_change_screen_size:
                    if self.pressed[pygame.K_s]:                                # Change the size of the window
                        self.ChangeScreenSize()
                    self.last_time_change_screen_size = self.time_now

            if self.pressed[pygame.K_q]:                                        # Quit the game
                self.CloseGame()

    def Update(self):                                                           # Display all the moving things on screen
        pygame.display.init()
        self.SongManager()
        self.DisplayBackground()
        self.DisplayTitle()
        self.DisplayGameData()
        self.DisplayPlayer()
        self.DisplayUI()
        self.horloge.tick(self.fps)
        pygame.display.flip()

    def DisplayBackground(self):
        if self.background_color_name is not None:
            background = pygame.Surface(self.current_size)    # Création d'une surface pour le dégradé
            for y in range(int(self.current_size[1])):                                # Dessin du dégradé vertical
                color = (int(self.bg_start_color[0] + (self.bg_end_color[0] - self.bg_start_color[0]) * y / self.current_size[1]),
                         int(self.bg_start_color[1] + (self.bg_end_color[1] - self.bg_start_color[1]) * y / self.current_size[1]),
                         int(self.bg_start_color[2] + (self.bg_end_color[2] - self.bg_start_color[2]) * y / self.current_size[1]))
                pygame.draw.line(background, color, (0, y), (self.current_size[0], y))  # Dessin ligne
            self.screen.blit(background, (0, 0))                                # Affichage du dégradé sur la fenêtre
        else:
            self.screen.blit(self.background, (0, 0))

    def DisplayTitle(self):
        if self.title_image is None:
            title = self.title_font.render(f"{self.game_name}", True, self.color_white)
            height = self.current_size[1] * 0.02
        else:
            title = self.title_image
            height = 30
        size = title.get_size()
        self.screen.blit(title, (self.current_size[0] * 0.5 - size[0] * 0.5, height))

    def DisplayPlayer(self):
        if self.player_body is not None:
            self.screen.blit(self.player.image, (self.player.pos_x, self.player.pos_y))
        else:                                                                   # Affiche un anneau transparent au centre
            transparent = pygame.Surface(self.current_size, pygame.SRCALPHA)
            # Position de base du joueur + Influence la vitesse du joueur
            center = (self.player.pos_x + self.player.size[0] * 0.5, self.player.pos_y + self.player.size[1] * 0.5)
            pygame.draw.circle(transparent, self.player.color, center, int(self.player.size[0] * 0.5), self.player.width)
            pygame.draw.circle(transparent, self.color_black, center, int(self.player.size[1] * 0.5 - self.player.width), 0)
            self.screen.blit(transparent, (0, 0))                               # Zone d'affichage de l'anneau

    def DisplayUI(self):
        life_height = self.current_size[0] * 0.5
        life_width = 10
        life_surface_bg = (self.current_size[0] * 0.5 - life_height * 0.5, life_width, life_height, life_width)
        pygame.draw.rect(self.screen, self.player.life_color_bg, life_surface_bg, 0, life_width)    # Display bg life bar
        pourcent = self.player.life / self.player.life_max
        life_surface = (self.current_size[0] * 0.5 - life_height * 0.5, life_width, int(life_height * pourcent), life_width)
        pygame.draw.rect(self.screen, self.player.life_color, life_surface, 0, life_width)          # Display player life

    def DisplayGameData(self):
        version = self.text_font.render(f"{self.version}", True, self.color_white)  # Display version of the game
        size = version.get_size()
        self.screen.blit(version, (10, self.current_size[1] - size[1] - 10))
        creator = self.text_font.render(f"by {self.creator}", True, self.color_white)  # Display creator of the game
        size = creator.get_size()
        self.screen.blit(creator, (self.current_size[0] - size[0] - 10, self.current_size[1] - size[1] - 10))

    def ChangeScreenSize(self):                                                 # Change the size of the window
        if self.current_size == self.size:
            self.current_size = self.second_size
            self.screen = pygame.display.set_mode(self.current_size)
            title_size = self.title_image.get_size()
            new_title_height = int(self.current_size[0] * 0.25 / title_size[0] * title_size[1])
            self.title_image = pygame.transform.scale(self.title_image, (self.current_size[0] * 0.25, new_title_height))
            self.background = pygame.transform.scale(self.background, self.current_size)
            self.player.size[0] = int(self.player.size[0] / 2)
            self.player.size[1] = int(self.player.size[1] / 2)
            self.player.width = int(self.player.width / 2)
            self.player.speed = int(self.player.speed / 2)
            self.player.pos_x = int(self.player.pos_x / 2)
            self.player.pos_y = int(self.player.pos_y / 2)
        elif self.current_size == self.second_size:
            self.current_size = self.size
            self.screen = pygame.display.set_mode(self.current_size)
            title_size = self.title_image.get_size()
            self.title_image = pygame.image.load(f"images/title.png")
            new_title_height = int(self.current_size[0] * 0.25 / title_size[0] * title_size[1])
            self.title_image = pygame.transform.scale(self.title_image, (self.current_size[0] * 0.25, new_title_height))
            self.background = pygame.transform.scale(self.background, self.current_size)
            self.player.size[0] *= 2
            self.player.size[1] *= 2
            self.player.width *= 2
            self.player.speed *= 2
            self.player.pos_x *= 2
            self.player.pos_y *= 2

    def ChangeLevel(self):
        self.level_index += 1
        if self.level_index > len(self.Color_names) - 1:
            self.level_index = 0
        self.background_color_name = self.Color_names[self.level_index]
        self.bg_start_color = self.Levels[self.level_index].start_color
        self.bg_end_color = self.Levels[self.level_index].end_color
        self.song_name = f"musics/{self.background_color_name}.mp3"

    def SongManager(self):                                                      # Change music based on card
        pygame.mixer.music.load(self.song_name)
        pygame.mixer.music.play(self.play_mode)
        pygame.mixer.music.set_volume(self.sound)

    def CloseGame(self):
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jeu = Game()

quit()