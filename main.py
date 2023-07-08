from math import sqrt
# from random import randint
from time import time, strftime, gmtime
from os import getcwd
from mutagen.mp3 import MP3
from player import Player
from level import Level
from bubble import Bubble, LifeBubble, Enemy
import pygame
import sys


# ! [later: 0.5.0] Add centrer camera sur player [check]
# ! [later: 0.5.0] Add function grow player (food_counter: level)
# ! [later: 0.5.0] Add condition pour accéder aux autres musiques / level (taille)
# ! [later: 0.5.0] Add eaten cells move in player (max increase with size / lenght ?)
# ! [later: 1.0.0] Add enemies + dégâts + bulle de vie [semi-check]
# ! [later: 1.0.0] Add saves + ask name player + display name
# ! [later: 1.0.0] Add comms en anglais + documentation
# ! [later: 1.5.0] Add effects (flou, rayons, bulles, creatures au fond ?)
# ! [later: 1.5.0] Add parameter (choose manière de bouger, de changer fond, Commandes, Credits, ...)
# ! [later: 1.5.0] Make player move in circles if player afk
# ! [later: 1.5.0] Add tutorials + transparences (add to UI)
# ! [later: 2.0.0] Add respawn if player die (mini-save + gain de vie si blessé)
# ! [later: 2.0.0] Secure game (boucles, fichiers chiffrés pour data, ...)
# ! [later: 2.0.0] Add upgrades (player stats + skins)
# ! [later: 2.0.0] Add player attack + power (in certain level)
class Game:                                                                     # Main class of the game
    def __init__(self):
        pygame.init()
        pygame.display.init()
        # Booleans data
        self.running = True
        self.full_screening = True
        self.pausing = False
        self.music_pausing = False
        self.muting = False
        self.going_home = False                                                 # !! Not available now
        # Game data
        self.game_name = "Grow Flow"
        self.creator = "One Shot"
        self.version = "v0.4.5"
        self.description = "A relaxing underwater fantasy game where you play as a small water creature. " \
                           "Grow by feeding on the cells and smaller creatures around you and discover the world of Grow Flow."
        print(f"Bienvenue sur {self.game_name} ! ({self.version})\n")
        # Icons data
        pygame.display.set_caption(self.game_name)                              # Game name
        self.icon = pygame.image.load("images/icon.png")                        # Game icon
        self.icon.set_colorkey((255, 255, 255))                                 # Remove white background
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)                                      # Set icon
        # Gameplay data
        self.path = getcwd()                                                    # ! [later] Use for saves
        self.horloge = pygame.time.Clock()                                      # Manage the fps
        self.pressed = pygame.key.get_pressed()
        self.camera_pos = [0, 0]
        self.fps = 30                                                           # Image per second
        # Screen data
        screen_info = pygame.display.Info()
        self.screen_size = [screen_info.current_w, screen_info.current_h]       # Default : full screen
        self.window = pygame.display.set_mode(self.screen_size)                 # Display window with chosen size
        # Images data
        self.title_image = None
        self.background_image = None                                            # ! Modify for unique color by level ?
        # Fonts data
        self.font_name = "Fillaflow.ttf"
        self.title_font_size = 100
        self.middle_font_size = 50
        self.text_font_size = 25
        self.title_font = pygame.font.Font(f"fonts/{self.font_name}", self.title_font_size)
        self.middle_font = pygame.font.Font(f"fonts/{self.font_name}", self.middle_font_size)
        self.text_font = pygame.font.Font(f"fonts/{self.font_name}", self.text_font_size)
        # Colors data
        self.Color_names = ["blue", "green", "cyan", "orange", "red", "pink",
                            "purple", "nightblue", "black", "brown", "yellow", "white"]
        self.Color_value = [(0, 160, 225), (50, 250, 130), (55, 255, 255), (250, 140, 40), (255, 60, 50), (255, 110, 210),
                            (190, 80, 225), (100, 40, 255), (55, 25, 125), (155, 90, 30), (255, 250, 45), (240, 240, 220)]
        self.color_name_bg = None                                               # Also full music name
        self.color_bg_start = None
        self.color_bg_end = None
        self.color_white = (250, 250, 250)
        self.color_lightgrey = (200, 200, 200)
        self.color_grey = (100, 100, 100)
        self.color_darkgrey = (50, 50, 50)
        self.color_black = (0, 0, 0)
        self.color_transparent = (0, 0, 0, 0)
        # Musics data
        self.song_name = f"musics/subnautica.mp3"
        self.music_pos = None
        self.music_lenght = None
        self.play_mode = -1
        self.sound_min = 0
        self.sound_max = 1
        self.current_sound = round(self.sound_max / 2, 2)
        self.old_sound = self.current_sound
        self.sound_gap = round(self.sound_max / 20, 2)
        self.sound_bar_height_percent = 0.15                                    # In percent
        self.sound_bar_width = 5                                                # In pixels
        # Timers data
        self.time_playing = time()
        self.time_now = time()
        self.last_time_change_screen_size = 0
        self.delay_change_screen_size = 0.5                                     # In seconds
        # Menu pause data
        self.paused_glass = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        pygame.draw.rect(self.paused_glass, self.color_white, self.paused_glass.get_rect())
        self.paused_glass.set_alpha(120)
        # Levels data
        self.Levels = []
        self.level_index = 0
        self.map_size = self.screen_size                                        # Place where player can move
        self.background_size = self.screen_size                                 # Background size (not all accessible to player)
        self.background = None                                                  # Surface pour les bords
        self.map_borders_pos = (0, 0, self.screen_size[0], self.screen_size[1])     # Borders of the map
        self.map_borders_width = 4
        self.map_borders_color = (222, 222, 222)
        self.map_borders = None                                                 # Store surface to display
        # Player data
        self.player = Player()
        self.player_home_position = None
        self.player_body = None                                                 # !! Unused (yet ?)
        self.player_life_bar_height = 10
        self.player_life_bar_width_percent = 0.5
        self.player_cell_bar_height = 5
        self.player_cell_bar_width_percent = 0.4
        # Bubbles data
        self.eaten_life_bubbles = 0
        self.eaten_enemies = 0
        self.Cells = pygame.sprite.Group()
        self.Life_bubbles = pygame.sprite.Group()
        self.Enemies = pygame.sprite.Group()
        # Main functions
        self.LoadComposants()                                                   # Set most of None variables
        self.Run()

    def LoadComposants(self):                                                   # Load the composants of the game
        print(f"Chargement des composants du jeu en cours...")
        start_load_time = time()
        self.title_image = pygame.image.load(f"images/title.png")
        title_size = self.title_image.get_size()
        new_title_height = int(self.screen_size[0] * 0.25 / title_size[0] * title_size[1])
        self.title_image = pygame.transform.scale(self.title_image, (self.screen_size[0] * 0.25, new_title_height))
        height = self.screen_size[1] * 0.02
        self.player_home_position = [self.screen_size[0] * 0.5 - 5, height + new_title_height * 0.6 - 1]    # !! Unused
        self.CreateLevels()
        self.color_name_bg = self.Levels[self.level_index].color_name
        self.color_bg_start = self.Levels[self.level_index].start_color
        self.color_bg_end = self.Levels[self.level_index].end_color
        self.map_size = self.Levels[self.level_index].map_size
        NO_pos = (int(self.screen_size[0] * 0.5), int(self.screen_size[1] * 0.5))
        self.map_borders_pos = (NO_pos[0], NO_pos[1], NO_pos[0] + self.map_size[0], NO_pos[1] + self.map_size[1])
        self.background_image = pygame.image.load(f"images/background.png")
        self.background_image = pygame.transform.scale(self.background_image, self.map_size)
        self.background_size = [self.map_size[0] + self.screen_size[0], self.map_size[1] + self.screen_size[1]]
        self.set_background()
        self.player = Player(map_borders=self.map_borders_pos, bg_size=self.background_size)
        self.song_name = f"musics/{self.color_name_bg}.mp3"
        self.LoadMapBorders()
        self.LoadBubbles()
        self.LoadArtefacts()
        end_load_time = time()
        loading_time = round(end_load_time - start_load_time, 3)
        print(f"Chargement des composants du jeu terminé ! ({loading_time} sec)\n")

    def CreateLevels(self):                                                     # Create the levels in the game
        print(f"Chargement des niveaux du jeu en cours...")
        for index, color_name in enumerate(self.Color_names):
            niveau = Level(index + 1, color_name, self.Color_value[index])
            self.Levels.append(niveau)
        print(f"Chargement des niveaux du jeu terminé !")

    def set_background(self):
        self.background = pygame.Surface(self.background_size)                  # Créer surface pour dégradé
        for y in range(int(self.background_size[1])):                           # Dessin du dégradé vertical
            red = int(self.color_bg_start[0] + (self.color_bg_end[0] - self.color_bg_start[0]) * y / self.background_size[1])
            red = 255 if red > 255 else red
            green = int(self.color_bg_start[1] + (self.color_bg_end[1] - self.color_bg_start[1]) * y / self.background_size[1])
            green = 255 if green > 255 else green
            blue = int(self.color_bg_start[2] + (self.color_bg_end[2] - self.color_bg_start[2]) * y / self.background_size[1])
            blue = 255 if blue > 255 else blue
            pygame.draw.line(self.background, (red, green, blue), (0, y), (self.background_size[0], y))     # Draw line

    def LoadMapBorders(self):                                                   # ! Move in Level ?
        print(f"Chargement des bords de la carte en cours...")
        border_surface = pygame.Surface(self.background_size)
        NO_pos = (int(self.screen_size[0] * 0.5) - self.map_borders_width,
                  int(self.screen_size[1] * 0.5) - self.map_borders_width)
        SE_pos = (int(self.screen_size[0] * 0.5) + self.map_size[0],
                  int(self.screen_size[1] * 0.5) + self.map_size[1])

        up_border_coords = (NO_pos[0], NO_pos[1], self.map_size[0] + self.map_borders_width * 2, self.map_borders_width)
        down_border_coords = (NO_pos[0], SE_pos[1], self.map_size[0] + self.map_borders_width * 2, self.map_borders_width)
        left_border_coords = (NO_pos[0], NO_pos[1], self.map_borders_width, self.map_size[1] + self.map_borders_width * 2)
        right_border_coords = (SE_pos[0], NO_pos[1], self.map_borders_width, self.map_size[1] + self.map_borders_width * 2)

        pygame.draw.rect(border_surface, self.map_borders_color, up_border_coords, 0, self.map_borders_width)
        pygame.draw.rect(border_surface, self.map_borders_color, down_border_coords, 0, self.map_borders_width)
        pygame.draw.rect(border_surface, self.map_borders_color, left_border_coords, 0, self.map_borders_width)
        pygame.draw.rect(border_surface, self.map_borders_color, right_border_coords, 0, self.map_borders_width)
        self.map_borders = border_surface
        print(f"Chargement des bords de la carte terminé !")

    def LoadBubbles(self):                                                      # Create Cells, Life bubbles and Enemies
        print(f"Chargement des bulles en cours...")
        self.Cells.empty()
        for _ in range(self.Levels[self.level_index].nb_cells_max):
            self.Cells.add(Bubble(map_borders=self.map_borders_pos))
        self.player.set_cells_eaten_max(len(self.Cells))

        self.eaten_life_bubbles = 0
        self.Life_bubbles.empty()
        for _ in range(self.Levels[self.level_index].nb_life_max):
            self.Life_bubbles.add(LifeBubble(map_borders=self.map_borders_pos))

        self.eaten_enemies = 0
        self.Enemies.empty()
        for _ in range(self.Levels[self.level_index].nb_enemy_max):
            self.Enemies.add(Enemy(map_borders=self.map_borders_pos))
        print(f"Chargement des bulles terminé !")

    @staticmethod
    def LoadArtefacts():                                                        # ! Animations, blur, waves, etc
        print(f"Chargement des artéfacts en cours...")
        print(f"Chargement des artéfacts terminé !")

    def Run(self):                                                              # Manage the game
        while self.running:
            self.DisplayManager()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.CloseGame()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:                             # Pause the game
                        self.ChangePausing()

                    if not self.pausing:                                        # If game not paused
                        if event.key == pygame.K_LEFT:                          # Change the level (precedent)
                            self.ChangeLevel(-1)
                        if event.key == pygame.K_RIGHT:                         # Change the level (next)
                            self.ChangeLevel(1)

                        if event.key == pygame.K_UP:                            # Up music sound
                            self.ChangeSound(1)
                        elif event.key == pygame.K_DOWN:                        # down music sound
                            self.ChangeSound(-1)

                        if event.key == pygame.K_k:                             # Pause / unpause the music
                            self.Pause_music()

                        if event.key == pygame.K_m:                             # Mute / vocal the music
                            self.Mute()

                    if event.key == pygame.K_c:                                 # Change player movement type
                        self.player.ChangeMovementMethod()

            self.pressed = pygame.key.get_pressed()                             # For functions that allowed continuous pressing
            if not self.pausing:
                self.player.MovementManager(self.map_borders_pos, self.screen_size, self.pressed)

            # if self.pressed[pygame.K_h]:                                      # !! [unused] Hide player in title
            #     self.going_home = True

            if self.pressed[pygame.K_LCTRL]:                                    # Two pressed functions
                self.time_now = time()
                if self.time_now - self.last_time_change_screen_size > self.delay_change_screen_size:
                    if self.pressed[pygame.K_s]:                                # Change the size of the window
                        self.ChangeScreenSize()
                    self.last_time_change_screen_size = self.time_now

            if self.pressed[pygame.K_ESCAPE]:                                   # Quit the game
                self.CloseGame()

    def DisplayManager(self):                                                   # Manage the sprites displayed in game
        self.CalculCameraPos()
        # self.window.fill(self.color_black)
        self.DisplayBackground()
        # self.DisplayMapBorders()                                                # ! [reuse later]
        self.DisplayArtefacts()                                                 # ! [later]
        self.DisplayBubbles()
        self.DisplayPlayer()
        self.SongManager()
        self.DisplaySongData()
        self.DisplayUI()
        self.DisplayLevelData()
        # self.CheckGoingHome()                                                 # !! Not available now
        if self.pausing:
            self.DisplayPause()
        pygame.display.flip()
        self.horloge.tick(self.fps)

    def CalculCameraPos(self):
        self.camera_pos = [- (self.player.rect.x - self.screen_size[0] // 2 + self.player.radius),
                           - (self.player.rect.y - self.screen_size[1] // 2 + self.player.radius)]

    def DisplayBackground(self):
        self.window.fill(self.color_black)
        if self.color_name_bg is not None:                                      # Display gradient bg
            self.window.blit(self.background, self.camera_pos)                  # Affichage du dégradé sur la fenêtre
        else:                                                                   # Display default image
            self.window.blit(self.background_image, self.camera_pos)

    def DisplayMapBorders(self):
        self.window.blit(self.map_borders, self.camera_pos)

    def DisplayArtefacts(self):
        self.DisplayGiant()
        self.DisplayWaveEffect()
        self.DisplayWaterThread()

    def DisplayGiant(self):
        pass

    def DisplayWaveEffect(self):
        pass

    def DisplayWaterThread(self):
        pass

    def DisplayBubbles(self):
        self.DisplayCells()
        self.DisplayLifeBubbles()
        self.DisplayEnemies()

    def DisplayCells(self):
        if len(self.Cells) > 0:
            for cell in self.Cells:
                if self.check_bubble_on_screen(cell):
                    self.window.blit(cell.image, cell.rect.move(self.camera_pos))
            if not self.pausing:
                self.Cells.update(self.Cells)

    def DisplayLifeBubbles(self):
        if len(self.Life_bubbles) > 0:
            for life_bubble in self.Life_bubbles:
                if self.check_bubble_on_screen(life_bubble):
                    self.window.blit(life_bubble.image, life_bubble.rect.move(self.camera_pos))
            if not self.pausing:
                self.Life_bubbles.update(self.Life_bubbles)

    def DisplayEnemies(self):
        if len(self.Enemies) > 0:
            for enemy in self.Enemies:
                if self.check_bubble_on_screen(enemy):
                    self.window.blit(enemy.image, enemy.rect.move(self.camera_pos))
            if not self.pausing:
                self.Enemies.update(self.Enemies)

    def DisplayPlayer(self):                                                    # Display player
        player = self.player_body if self.player_body is not None else self.player.image
        position = (int(self.screen_size[0] * 0.5 - self.player.radius), int(self.screen_size[1] * 0.5 - self.player.radius))
        self.window.blit(player, position)

    def DisplayUI(self):
        life_height = self.player_life_bar_height                               # Display bg life bar (up-middle)
        life_width = self.screen_size[0] * self.player_life_bar_width_percent
        life_surface_bg = (self.screen_size[0] * 0.5 - life_width * 0.5, life_height, life_width, life_height)
        pygame.draw.rect(self.window, self.player.life_color_bg, life_surface_bg, 0, life_height)
        percent = self.player.life / self.player.life_max                       # Display player life
        life_surface = (self.screen_size[0] * 0.5 - life_width * 0.5, life_height, int(life_width * percent), life_height)
        pygame.draw.rect(self.window, self.player.life_color, life_surface, 0, life_height)

        nb_cells_height = self.player_cell_bar_height                           # Display bg cell bar (up-middle)
        nb_cells_width = self.screen_size[0] * self.player_cell_bar_width_percent
        screen_gap = life_height * 3 + nb_cells_height
        nb_cells_surface_bg = (self.screen_size[0] * 0.5 - nb_cells_width * 0.5, screen_gap,
                               nb_cells_width, nb_cells_height)
        pygame.draw.rect(self.window, self.player.cell_color_bg, nb_cells_surface_bg, 0, nb_cells_height)
        percent = self.player.cells_eaten / self.player.cells_eaten_max         # Display current number of cells eaten
        nb_cells_surface = (self.screen_size[0] * 0.5 - nb_cells_width * 0.5, screen_gap,
                            int(nb_cells_width * percent), nb_cells_height)
        pygame.draw.rect(self.window, self.player.cell_color, nb_cells_surface, 0, nb_cells_height)

    def DisplayLevelData(self):                                                 # ! Add visu bulle + vars in main class
        gap = 20
        bar_height = 5
        bar_width = int(self.screen_size[0] * 0.125)
        bg_enemies_bar_pos = (gap, gap, bar_width, bar_height)                  # Display bg enns bar (up-left)
        pygame.draw.rect(self.window, self.set_bg_color((250, 60, 60)), bg_enemies_bar_pos, 0, bar_height)
        percent = self.eaten_enemies / len(self.Enemies)                        # Display enns bar
        enemies_bar_pos = (gap, gap, int(bar_width * percent), bar_height)
        pygame.draw.rect(self.window, (250, 60, 60), enemies_bar_pos, 0, bar_height)
        bg_life_bar_pos = (gap, gap * 2 + bar_height, bar_width, bar_height)    # Display bg life bar (up-left)
        pygame.draw.rect(self.window, self.set_bg_color((120, 250, 30)), bg_life_bar_pos, 0, bar_height)
        percent = self.eaten_life_bubbles / len(self.Life_bubbles)              # Display life bar
        life_bar_pos = (gap, gap * 2 + bar_height, int(bar_width * percent), bar_height)
        pygame.draw.rect(self.window, (120, 250, 30), life_bar_pos, 0, bar_height)

        """                                                 # !!!
        player_text = self.text_font.render(f"P: ({self.player.rect.x}, {self.player.rect.y})", True, self.color_white)
        self.window.blit(player_text, (10, 100))
        """

    def DisplayPause(self):
        self.window.blit(self.paused_glass, (0, 0))                             # Fond semi-transparent
        pause_text = self.middle_font.render(f"Pause", True, self.color_black)
        pause_size = pause_text.get_size()
        self.window.blit(pause_text, ((self.screen_size[0] - pause_size[0]) * 0.5, (self.screen_size[1] - pause_size[1]) * 0.5))
        self.DisplayTitle()
        self.DisplayGameData()

    def DisplayTitle(self):                                                     # Display game name
        if self.title_image is None:
            title = self.title_font.render(f"{self.game_name}", True, self.color_black)
            height = self.screen_size[1] * 0.02
        else:
            title = self.title_image
            height = 30
        size = title.get_size()
        self.window.blit(title, (self.screen_size[0] * 0.5 - size[0] * 0.5, height))

    def DisplayGameData(self):                                                  # Display version and creator name
        version = self.text_font.render(f"{self.version}", True, self.color_black)
        size = version.get_size()
        self.window.blit(version, (10, self.screen_size[1] - size[1] - 10))
        creator = self.text_font.render(f"by {self.creator}", True, self.color_black)
        size = creator.get_size()
        self.window.blit(creator, (self.screen_size[0] - size[0] - 10, self.screen_size[1] - size[1] - 10))

    @staticmethod
    def set_bg_color(color):                                                    # Set background color
        color = list(color)
        for i in range(3):
            color[i] = int(color[i] * 0.75)
        return tuple(color)

    def check_bubble_on_screen(self, bubble):                                   # Check if the bubble must be display
        return abs(self.camera_pos[0]) - bubble.diameter - bubble.speed <= bubble.rect.x <= \
            abs(self.camera_pos[0]) + self.screen_size[0] + bubble.speed and \
            abs(self.camera_pos[1]) - bubble.diameter - bubble.speed <= bubble.rect.y <= \
            abs(self.camera_pos[1]) + self.screen_size[1] + bubble.speed

    def ChangePausing(self):                                                    # Pause or unpause game + music
        self.pausing = not self.pausing
        if self.pausing and not self.music_pausing or not self.pausing and self.music_pausing:
            self.Pause_music()

    def CheckGoingHome(self):                                                   # Check if player go home position
        if self.going_home:
            if self.player.move_method == self.player.Methods[0]:
                self.player.ChangeMovementMethod()
            self.player.MoveWithMouse(goal_pos=self.player_home_position)

            player_center = [self.player.rect.x + self.player.radius, self.player.rect.y + self.player.radius]
            if self.IsClose(player_center, self.player_home_position, 0):       # self.player.size * 0.1):
                self.going_home = False

    @staticmethod
    def IsClose(coord1, coord2, limit=10):
        distance = sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
        return distance <= limit

    def ChangeScreenSize(self):                                                 # Change the size of the window
        self.full_screening = not self.full_screening
        if self.full_screening:
            self.screen_size = [self.screen_size[0] * 2, self.screen_size[1] * 2]
            self.map_size = [self.map_size[0] * 2, self.map_size[1] * 2]
            self.window = pygame.display.set_mode(self.screen_size)
            self.background_image = pygame.transform.scale(self.background_image, self.map_size)
            self.background_size = [self.background_size[0] * 2, self.background_size[1] * 2]
            title_size = self.title_image.get_size()
            self.title_image = pygame.image.load(f"images/title.png")
            new_title_height = int(self.screen_size[0] * 0.25 / title_size[0] * title_size[1])
            self.title_image = pygame.transform.scale(self.title_image, (self.screen_size[0] * 0.25, new_title_height))
            height = self.screen_size[1] * 0.02
            self.player_home_position = [self.screen_size[0] * 0.5 - 5, height + new_title_height * 0.6 - 2]
            self.title_font_size *= 2
            self.title_font = pygame.font.Font(f"fonts/{self.font_name}", self.title_font_size)
            self.text_font_size *= 2
            self.text_font = pygame.font.Font(f"fonts/{self.font_name}", self.text_font_size)
            self.player.diameter *= 2
            self.player.radius *= 2
            self.player.width *= 2
            self.player.speed *= 2
            self.player.rect.x *= 2
            self.player.rect.y *= 2
            for cell in self.Cells:
                cell.size *= 2
                cell.rect.x *= 2
                cell.rect.y *= 2
                cell.speed *= 2
            for life_bubble in self.Life_bubbles:
                life_bubble.size *= 2
                life_bubble.rect.x *= 2
                life_bubble.rect.y *= 2
                life_bubble.speed *= 2
            for enemy in self.Enemies:
                enemy.size *= 2
                enemy.rect.x *= 2
                enemy.rect.y *= 2
                enemy.speed *= 2
        else:
            self.screen_size = [int(self.screen_size[0] * 0.5), int(self.screen_size[1] * 0.5)]
            self.map_size = [int(self.map_size[0] * 0.5), int(self.map_size[1] * 0.5)]
            self.window = pygame.display.set_mode(self.screen_size)
            self.background_image = pygame.transform.scale(self.background_image, self.map_size)
            self.background_size = [int(self.background_size[0] * 0.5), int(self.background_size[1] * 0.5)]
            title_size = self.title_image.get_size()
            new_title_height = int(self.screen_size[0] * 0.25 / title_size[0] * title_size[1])
            self.title_image = pygame.transform.scale(self.title_image, (self.screen_size[0] * 0.25, new_title_height))
            height = self.screen_size[1] * 0.02
            self.player_home_position = [self.screen_size[0] * 0.5 - 2, height + new_title_height * 0.6 + 15]
            self.title_font_size = int(self.title_font_size * 0.5)
            self.title_font = pygame.font.Font(f"fonts/{self.font_name}", self.title_font_size)
            self.text_font_size = int(self.text_font_size * 0.5)
            self.text_font = pygame.font.Font(f"fonts/{self.font_name}", self.text_font_size)
            self.player.diameter = int(self.player.diameter * 0.5)
            self.player.radius = int(self.player.radius * 0.5)
            self.player.width = int(self.player.width * 0.5)
            self.player.speed = int(self.player.speed * 0.5)
            self.player.rect.x = int(self.player.rect.x * 0.5)
            self.player.rect.y = int(self.player.rect.y * 0.5)
            for cell in self.Cells:
                cell.size = int(cell.size * 0.5)
                cell.rect.x = int(cell.rect.x * 0.5)
                cell.rect.y = int(cell.rect.y * 0.5)
                cell.speed = int(cell.speed * 0.5)
            for life_bubble in self.Life_bubbles:
                life_bubble.size = int(life_bubble.size * 0.5)
                life_bubble.rect.x = int(life_bubble.rect.x * 0.5)
                life_bubble.rect.y = int(life_bubble.rect.y * 0.5)
                life_bubble.speed = int(life_bubble.speed * 0.5)
            for enemy in self.Enemies:
                enemy.size = int(enemy.size * 0.5)
                enemy.rect.x = int(enemy.rect.x * 0.5)
                enemy.rect.y = int(enemy.rect.y * 0.5)
                enemy.speed = int(enemy.speed * 0.5)

    # ! Add respawn player in map center
    def ChangeLevel(self, direction=1):                                         # Update level (bubbles, bg, music...)
        if direction > 0:
            self.level_index += 1
        elif direction < 0:
            self.level_index -= 1
        if self.level_index > len(self.Color_names) - 1:
            self.level_index = 0
        elif self.level_index < 0:
            self.level_index = len(self.Color_names) - 1
        self.color_name_bg = self.Color_names[self.level_index]                 # Update Colors
        self.color_bg_start = self.Levels[self.level_index].start_color
        self.color_bg_end = self.Levels[self.level_index].end_color
        full_map_size = self.Levels[self.level_index].map_size
        second_map_size = [int(full_map_size[0] * 0.5), int(full_map_size[1] * 0.5)]
        self.map_size = full_map_size if self.full_screening else second_map_size                   # Update map size
        NO_pos = (int(self.screen_size[0] * 0.5), int(self.screen_size[1] * 0.5))
        self.map_borders_pos = (NO_pos[0], NO_pos[1], NO_pos[0] + self.map_size[0], NO_pos[1] + self.map_size[1])
        full_bg_size = [self.map_size[0] + self.screen_size[0], self.map_size[1] + self.screen_size[1]]
        second_bg_size = [int(full_bg_size[0] * 0.5), int(full_bg_size[1] * 0.5)]
        self.background_size = full_bg_size if self.full_screening else second_bg_size              # Update bg size
        self.set_background()                                                   # Update gradient bg
        self.song_name = f"musics/{self.color_name_bg}.mp3"
        pygame.mixer.music.load(self.song_name)                                 # Update music
        pygame.mixer.music.rewind()                                             # Change current played music
        self.LoadMapBorders()                                                   # Update map borders
        self.LoadBubbles()                                                      # Update bubbles
        self.player.map_borders = self.map_borders_pos
        self.player.ChangeLevel()

    def SongManager(self):                                                      # Change music based on card
        if not pygame.mixer.music.get_busy() and not self.music_pausing or self.music_pos >= self.music_lenght:
            pygame.mixer.music.load(self.song_name)
            pygame.mixer.music.play(self.play_mode)
            self.music_pos = 0

        song_mutagen = MP3(self.song_name)                                      # Load le format
        self.music_lenght = song_mutagen.info.length                            # Get song lenght (in sec)
        self.music_pos = pygame.mixer.music.get_pos() // 1000

        pygame.mixer.music.set_volume(self.current_sound)

    def DisplaySongData(self):
        song_lenght_format = strftime('%M:%S', gmtime(self.music_lenght))
        song_position_format = strftime('%M:%S', gmtime(self.music_pos))
        song_duration_text = self.text_font.render(f"{song_position_format} / {song_lenght_format}", True, self.color_white)
        duration_size = song_duration_text.get_size()
        # Song name
        song_name = self.song_name.replace(".mp3", "").replace("musics/", "").capitalize()
        song_title_text = self.text_font.render(f"{song_name}", True, self.color_white)
        title_size = song_title_text.get_size()
        self.window.blit(song_title_text, (self.screen_size[0] - duration_size[0] * 0.5 - title_size[0] * 0.5 - 10, 10))
        self.window.blit(song_duration_text, (self.screen_size[0] - duration_size[0] - 10, title_size[1]))
        # Sound bar
        sound_height = int(self.screen_size[1] * self.sound_bar_height_percent)
        sound_width = self.sound_bar_width
        sound_surface_bg = (self.screen_size[0] - sound_width * 3, sound_height, sound_width, sound_height)
        pygame.draw.rect(self.window, self.color_grey, sound_surface_bg, 0, sound_height)       # Display bg sound bar
        percent = self.current_sound / self.sound_max
        sound_surface = (self.screen_size[0] - sound_width * 3, sound_height * 2 - int(sound_height * percent),
                         sound_width, int(sound_height * percent))
        pygame.draw.rect(self.window, self.color_lightgrey, sound_surface, 0, sound_height)     # Display current sound

    def Mute(self):                                                             # Mute the music of the level
        self.muting = not self.muting
        self.current_sound = 0 if self.muting else self.old_sound

    def ChangeSound(self, direction=0):
        if direction > 0:
            self.current_sound += self.sound_gap
            self.old_sound += self.sound_gap
        elif direction < 0:
            self.current_sound -= self.sound_gap
            self.old_sound -= self.sound_gap
        self.current_sound = 0 if self.current_sound < 0 else 1 if self.current_sound > 1 else self.current_sound
        self.old_sound = 0 if self.old_sound < 0 else 1 if self.old_sound > 1 else self.old_sound

    def Pause_music(self):                                                      # Pause the music
        self.music_pausing = not self.music_pausing
        if self.music_pausing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def LoadGame(self):                                                         # ! [later]
        pass

    def SaveGame(self):                                                         # ! [later]
        pass

    def CloseGame(self):                                                        # Close the game
        end_playing = time()
        self.SaveGame()
        played_time = end_playing - self.time_playing
        if played_time < 60:
            played_time = strftime('%S', gmtime(played_time))
            time_unite = "sec"
        elif played_time < 3600:
            played_time = strftime('%M:%S', gmtime(played_time))
            time_unite = "min"
        else:
            played_time = strftime('%H:%M:%S', gmtime(played_time))
            time_unite = "h"
        print(f"Temps joué : {played_time} {time_unite}")
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jeu = Game()

quit()
