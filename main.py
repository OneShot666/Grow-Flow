from math import sqrt, atan2, cos, sin
from random import choice
from time import time, strftime, gmtime
from os import getcwd, listdir
from mutagen.mp3 import MP3
from player import Player
from level import Level
from bubble import Bubble, LifeBubble, Enemy, CellEaten
import pygame
import sys


# !!! 01/08: Eval Système Exploitation, Chp 1 & 2 (faire Xmind + watch vidéos) + réviser et faire marcher MV [Linux]

""" Documentation
creator : One Shot
name : Grow Flow
year of creation : 2023
version : 1.0.0
language : python
purpose : A little relaxation game where you play a cell in an underwater world.
          Grow by feeding on the cells and smaller creatures around you and discover the world of Grow Flow.
arguments : None
requirements : libraries 'math', 'random', 'time', 'os', 'mutagen', 'pygame' and 'sys'.
"""


# ! [later: 1.5.0] Add effects (flou, rayons, bulles, creatures au fond ?)
# ! [later: 1.5.0] Add menus + parameters (choose manière de bouger, de changer fond, Commandes, Credits, ...)
# ! Add star (buts) pour les levels + load player game when launching level
# ! [later: 1.5.0] Make player move in circles if player afk
# ! [later: 1.5.0] Add tutorials + transparences (add to UI)
# ! [later: 2.0.0] Add respawn if player dies (mini-save + gain de vie si blessé)
# ! [later: 2.0.0] Secure game (boucles, fichiers chiffrés pour data, ...)
# ! [later: 2.0.0] Add upgrades (player stats + skins)
# ! [later: 2.0.0] Add player attack + power (in certain level)
class Game:                                                                     # Main class of the game
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()
        # Booleans data
        self.running = True
        self.menuing = True                                                     # ! [later] Add in menu
        self.playing = False                                                    # ! [later] Use when playing (with menu)
        self.asking_name = True
        self.play_pausing = False
        self.music_pausing = False
        self.muting = False
        # Game data
        self.game_name = "Grow Flow"
        self.creator = "One Shot"
        self.version = "v1.0.0"
        self.description = "A relaxing underwater fantasy game where you play as a small water creature. " \
                           "Survive and explore this fantasy world. Grow and develop your abilities to " \
                           "go ever deeper into the adventure!"
        print(f"Bienvenue sur {self.game_name} ! ({self.version})\n")
        # Icons data
        pygame.display.set_caption(self.game_name)                              # Game name
        self.icon = pygame.image.load("images/icon.png")                        # Game icon
        self.icon.set_colorkey((255, 255, 255))                                 # Remove white background
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)                                      # Set icon
        # Gameplay data
        self.path = getcwd()                                                    # Current path
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
        self.Fonts = [_ for _ in listdir(f"{self.path}/fonts") if _.endswith(".ttf")]  # Get fonts
        self.font_name = choice(self.Fonts)
        print(self.font_name)
        self.giant_font_size = 100
        self.big_font_size = 50
        self.middle_font_size = 25
        self.small_font_size = 20
        self.mini_font_size = 10
        self.giant_font = pygame.font.Font(f"fonts/{self.font_name}", self.giant_font_size)
        self.big_font = pygame.font.Font(f"fonts/{self.font_name}", self.big_font_size)
        self.middle_font = pygame.font.Font(f"fonts/{self.font_name}", self.middle_font_size)
        self.small_font = pygame.font.Font(f"fonts/{self.font_name}", self.small_font_size)
        self.mini_font = pygame.font.Font(f"fonts/{self.font_name}", self.mini_font_size)
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
        self.music_name = f"musics/subnautica.mp3"
        self.music_pos = 0
        self.music_lenght = 0
        self.play_mode = -1
        self.sound_min = 0
        self.sound_max = 1
        self.current_sound = round(self.sound_max / 2, 2)
        self.old_sound = self.current_sound
        self.sound_gap = round(self.sound_max / 20, 2)
        self.sound_bar_height_percent = 0.15                                    # In percent
        self.sound_bar_width = 5                                                # In pixels
        # Sounds data
        self.bg_sound = pygame.mixer.Sound(f"sounds/deep_bubbles.mp3")
        self.bg_sound.set_volume(0.1)
        self.bubbling_sound = pygame.mixer.Sound(f"sounds/bubbling.mp3")
        self.bubbling_sound.set_volume(0.2)
        self.low_bubbling_sound = pygame.mixer.Sound(f"sounds/low_bubbling.mp3")
        self.low_bubbling_sound.set_volume(0.3)
        # Timers data
        self.time_playing = time()
        self.time_now = time()
        self.last_time_something = 0                                            # [later] Keep for possible timer
        self.delay_something = 5                                                # [later] //
        # Menu pause data
        self.paused_glass = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        pygame.draw.rect(self.paused_glass, self.color_white, self.paused_glass.get_rect())
        self.paused_glass.set_alpha(120)
        # Ask Name UI Data
        self.ask_box_size = [320, 200]
        self.ask_box_width = 20
        self.ask_box_title_percent = 0.3
        self.ask_box_entry_percent = 0.4
        self.ask_box_bg_color = (96, 235, 249)                                  # Light blue
        self.ask_box_title_color = (24, 237, 202)                               # Cyan
        self.ask_box_title_text_color = (137, 255, 187)                         # Light cyan
        self.ask_box_entry_color = (55, 211, 242)                               # Turquoise
        self.ask_box_entry_text_color = (73, 168, 252)                          # Light turquoise
        self.Unwanted_pseudo = ["", "\\", None]
        self.pseudonyme = ""
        # Levels data
        self.Levels = []
        self.level_index = 0
        self.map_size = self.screen_size                                        # Where bubbles can move
        self.background = None                                                  # Surface for the background
        self.background_size = self.screen_size                                 # Background size (oceans)
        self.map_borders = None                                                 # Surface for the borders
        self.map_borders_pos = (0, 0, self.screen_size[0], self.screen_size[1])     # Map borders' position
        self.map_borders_width = 4
        self.map_borders_color = (222, 222, 222)
        # Player data
        self.player = None
        self.player_life_bar_height = 10
        self.player_life_bar_width_percent = 0.5
        self.player_cell_bar_height = 5
        self.player_cell_bar_width_percent = 0.4
        # CellsFinder data
        self.cellsFinder_start_helping_count = 10                               # Help player find cells from 10 or less
        self.cellsFinder_bar_color = (175, 205, 205)                            # Light grey
        self.cellsFinder_bar_height = 11                                        # In pixels
        self.cellsFinder_bar_width = 3                                          # In pixels
        self.cellsFinder_gap = 8                                                # In pixels
        # Bubbles data
        self.Cells = pygame.sprite.Group()
        self.Life_bubbles = pygame.sprite.Group()
        self.Enemies = pygame.sprite.Group()
        self.nb_life_bubbles_max = 0
        self.nb_enemies_max = 0
        # Main functions
        self.LoadComposants()                                                   # Set None variables and stuff
        self.Run()

    def LoadComposants(self):                                                   # Load the composants of the game
        print(f"Chargement des composants du jeu en cours...")
        start_load_time = time()
        self.title_image = pygame.image.load(f"images/title.png")
        title_size = self.title_image.get_size()
        new_title_height = int(self.screen_size[0] * 0.25 / title_size[0] * title_size[1])
        self.title_image = pygame.transform.scale(self.title_image, (self.screen_size[0] * 0.25, new_title_height))
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
        self.music_name = f"musics/{self.color_name_bg}.mp3"
        self.LoadMapBorders()
        self.player = Player(map_borders=self.map_borders_pos, screen_size=self.screen_size)
        self.pseudonyme = self.player.name
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
        self.background = pygame.Surface(self.background_size)                  # Create Gradient Fill
        for y in range(int(self.background_size[1])):                           # Drawing the vertical gradient
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

        self.Life_bubbles.empty()
        for _ in range(self.Levels[self.level_index].nb_life_max):
            self.Life_bubbles.add(LifeBubble(map_borders=self.map_borders_pos))
        self.nb_life_bubbles_max = len(self.Life_bubbles)

        self.Enemies.empty()
        for _ in range(self.Levels[self.level_index].nb_enemy_max):
            self.Enemies.add(Enemy(map_borders=self.map_borders_pos))
        self.nb_enemies_max = len(self.Enemies)
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

                if self.asking_name:                                            # ! [later] Move in menu
                    self.TextManager(event)
                else:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:                         # Pause the game
                            self.ChangePausing()

                        if not self.play_pausing:                               # If game isn't paused
                            if event.key == pygame.K_UP:                        # Up music sound
                                self.ChangeSound(1)
                            elif event.key == pygame.K_DOWN:                    # Down music sound
                                self.ChangeSound(-1)

                            if event.key == pygame.K_k:                         # Pause / unpause the music
                                self.PauseMusic()

                            if event.key == pygame.K_m:                         # Mute / vocal the music
                                self.Mute()

                        if event.key == pygame.K_c:                             # Change player movement type
                            self.player.ChangeMovementMethod()

            self.pressed = pygame.key.get_pressed()                             # For functions that allowed continuous pressing
            if not self.play_pausing:
                self.player.MovementManager(self.map_borders_pos, self.screen_size, self.pressed,
                                            self.Cells, self.Life_bubbles, self.Enemies)
                if self.player.is_dead:
                    self.CloseGame()

            if self.pressed[pygame.K_LCTRL]:                                    # Two pressed functions
                self.time_now = time()
                if self.time_now - self.last_time_something > self.delay_something:
                    if self.pressed[pygame.K_s]:
                        self.SaveGame()                                         # May be replaced by something else
                    self.last_time_something = self.time_now

            if self.pressed[pygame.K_ESCAPE]:                                   # Quit the game
                self.CloseGame()

    def DisplayManager(self):                                                   # Manage the sprites displayed in game
        self.CalculCameraPos()
        # self.window.fill(self.color_black)                                    # ! For tests
        self.DisplayBackground()
        # self.DisplayMapBorders()                                                # ! [reuse later]
        self.DisplayArtefacts()                                                 # ! [later]
        self.DisplayBubbles()
        self.DisplayPlayer()
        self.CellsFinder()
        self.MusicManager()
        self.DisplayMusicData()
        self.DisplayUI()
        self.DisplayLevelData()
        self.CheckNextLevel()
        if self.play_pausing:
            self.DisplayPause()
        self.CheckAskPlayerName()                                               # ! [later] Move in menu ?
        pygame.display.flip()
        self.horloge.tick(self.fps)

    # ! Add cursor + maintain backspace
    def CheckAskPlayerName(self):                                               # Set player's name (interface)
        if self.player.name == "Player" and self.asking_name:
            self.play_pausing = True
            self.music_pausing = True
            ask_name_box = pygame.Surface(self.ask_box_size, pygame.SRCALPHA)
            pygame.draw.rect(ask_name_box, self.ask_box_bg_color,
                             (0, 0, ask_name_box.get_width(), ask_name_box.get_height()), 0, self.ask_box_width)
            # Draw title box + text
            pygame.draw.rect(ask_name_box, self.ask_box_title_color,
                             (0, 0, ask_name_box.get_width(), ask_name_box.get_height() * self.ask_box_title_percent),
                             border_top_left_radius=self.ask_box_width, border_top_right_radius=self.ask_box_width)
            title_text = self.middle_font.render(f"Entrez votre nom", True, self.ask_box_title_text_color)
            title_size = title_text.get_size()
            ask_name_box.blit(title_text, (int(ask_name_box.get_width() * 0.5 - title_size[0] * 0.5),
                                           int((ask_name_box.get_height() * self.ask_box_title_percent - title_size[1]) * 0.5)))
            # Draw entry box + text
            gap_x = ask_name_box.get_height() * round((1 - self.ask_box_title_percent - self.ask_box_entry_percent) / 2, 3)
            gap_y = ask_name_box.get_height() * self.ask_box_title_percent + gap_x
            box_width = ask_name_box.get_width() - gap_x * 2
            box_height = ask_name_box.get_height() * self.ask_box_entry_percent
            pygame.draw.rect(ask_name_box, self.ask_box_entry_color, (gap_x, gap_y, box_width, box_height),
                             0, self.ask_box_width)
            entry_text = self.middle_font.render(f"{self.pseudonyme}", True, self.ask_box_entry_text_color)
            entry_size = entry_text.get_size()
            ask_name_box.blit(entry_text, (gap_x + box_width * 0.5 - entry_size[0] * 0.5,
                                           gap_y + box_height * 0.5 - entry_size[1] * 0.5))

            rect_pos = (self.screen_size[0] * 0.5 - self.ask_box_size[0] * 0.5,
                        self.screen_size[1] * 0.5 - self.ask_box_size[1] * 0.5)
            self.window.blit(ask_name_box, rect_pos)

    def TextManager(self, event):                                               # Act like a text editor
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.asking_name = False
            if event.key == pygame.K_RETURN:
                self.player.setName(self.pseudonyme)
                self.asking_name = False
                self.play_pausing = False
                self.music_pausing = False
            elif event.key == pygame.K_BACKSPACE:
                self.pseudonyme = self.pseudonyme[:-1]
            elif event.key == pygame.K_DELETE:
                self.pseudonyme = ""
            elif event.key == pygame.K_TAB:
                self.pseudonyme += " " * 4
            else:
                self.pseudonyme += event.unicode

    def CalculCameraPos(self):
        self.camera_pos = [- (self.player.rect.x - self.screen_size[0] // 2 + self.player.current_radius),
                           - (self.player.rect.y - self.screen_size[1] // 2 + self.player.current_radius)]

    def DisplayBackground(self):
        self.window.fill(self.color_black)
        if self.color_name_bg is not None:                                      # Display gradient bg
            self.window.blit(self.background, self.camera_pos)                  # Viewport gradient display
        else:                                                                   # Display default image
            self.window.blit(self.background_image, self.camera_pos)

    def DisplayMapBorders(self):                                                # Display borders of the map
        self.window.blit(self.map_borders, self.camera_pos)

    def DisplayArtefacts(self):                                                 # Display the artefacts
        self.DisplayGiant()
        self.DisplayWaveEffect()
        self.DisplayWaterThread()

    def DisplayGiant(self):                                                     # Display the current giant of the level
        pass

    def DisplayWaveEffect(self):                                                # Display some wave effects
        pass

    def DisplayWaterThread(self):                                               # Display the water thread
        pass

    def DisplayBubbles(self):                                                   # Display different bubbles in the level
        self.DisplayCells()
        self.DisplayLifeBubbles()
        self.DisplayEnemies()

    def DisplayCells(self):                                                     # Display the small cells (food)
        if len(self.Cells) > 0:
            for cell in self.Cells:
                if self.check_bubble_on_screen(cell):
                    self.window.blit(cell.image, cell.rect.move(self.camera_pos))
                if not self.play_pausing:
                    cell.Update(self.Cells, self.player)

    def DisplayLifeBubbles(self):                                               # Display the life bubbles
        if len(self.Life_bubbles) > 0:
            for life_bubble in self.Life_bubbles:
                if self.check_bubble_on_screen(life_bubble):
                    self.window.blit(life_bubble.image, life_bubble.rect.move(self.camera_pos))
                if not self.play_pausing:
                    life_bubble.Update(self.Life_bubbles, self.player)

    def DisplayEnemies(self):                                                   # Display the enemies
        if len(self.Enemies) > 0:
            for enemy in self.Enemies:
                if self.check_bubble_on_screen(enemy):
                    self.window.blit(enemy.image, enemy.rect.move(self.camera_pos))
                if not self.play_pausing:
                    enemy.Update(self.Enemies, self.player)

    def DisplayPlayer(self):                                                    # Display the player
        for meal in self.player.Stomach:                                        # Display eaten cells in the player
            meal.Update()
            self.window.blit(meal.image, meal.screen_pos)

        self.window.blit(self.player.image, self.player.screen_pos)
        # Display name
        name_text = self.small_font.render(f"{self.player.name}", True, self.color_bg_start)
        name_size = name_text.get_size()
        self.window.blit(name_text, (int(self.screen_size[0] * 0.5 - name_size[0] * 0.5),
                                     int(self.screen_size[1] * 0.5 - self.player.current_radius - name_size[1] - 5)))

    def CellsFinder(self):                                                      # Help player find remaining cells
        if len(self.Cells) <= self.cellsFinder_start_helping_count:             # If there are few cells left
            for cell in self.Cells:
                # Calculate stroke coordinates
                position = [int(self.screen_size[0] * 0.5), int(self.screen_size[1] * 0.5)]
                angle = atan2(cell.rect.y - self.player.rect.y, cell.rect.x - self.player.rect.x)
                gap = self.player.current_radius + self.cellsFinder_gap
                start_x = position[0] + int(cos(angle) * gap)
                start_y = position[1] + int(sin(angle) * gap)
                end_x = position[0] + int(cos(angle) * (gap + self.cellsFinder_bar_height))
                end_y = position[1] + int(sin(angle) * (gap + self.cellsFinder_bar_height))
                # Draw line in the direction of the cell
                pygame.draw.line(self.window, self.cellsFinder_bar_color, (start_x, start_y), (end_x, end_y),
                                 self.cellsFinder_bar_width)

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
        # Display the current number of cells eaten
        percent = self.player.cells_eaten / self.player.cells_eaten_max if self.player.cells_eaten_max != 0 else 0
        nb_cells_surface = (self.screen_size[0] * 0.5 - nb_cells_width * 0.5, screen_gap,
                            int(nb_cells_width * percent), nb_cells_height)
        pygame.draw.rect(self.window, self.player.cell_color, nb_cells_surface, 0, nb_cells_height)

    # ! Add small image of bubbles + add vars in the main class
    def DisplayLevelData(self):                                                 # Display nb of remaining bubbles
        gap = 20
        bar_height = 5
        bar_width = int(self.screen_size[0] * 0.125)
        bg_enemies_bar_pos = (gap, gap, bar_width, bar_height)                  # Display bg enns bar (up-left)
        pygame.draw.rect(self.window, self.set_bg_color((250, 60, 60)), bg_enemies_bar_pos, 0, bar_height)
        percent = len(self.Enemies) / self.nb_enemies_max                       # Display enns bar
        enemies_bar_pos = (gap, gap, int(bar_width * percent), bar_height)
        pygame.draw.rect(self.window, (250, 60, 60), enemies_bar_pos, 0, bar_height)
        bg_life_bar_pos = (gap, gap * 2 + bar_height, bar_width, bar_height)    # Display bg life bar (up-left)
        pygame.draw.rect(self.window, self.set_bg_color((120, 250, 30)), bg_life_bar_pos, 0, bar_height)
        percent = len(self.Life_bubbles) / self.nb_life_bubbles_max             # Display life bar
        life_bar_pos = (gap, gap * 2 + bar_height, int(bar_width * percent), bar_height)
        pygame.draw.rect(self.window, (120, 250, 30), life_bar_pos, 0, bar_height)

    def DisplayPause(self):                                                     # Display pause menu
        self.window.blit(self.paused_glass, (0, 0))                             # Semi-transparent background
        pause_text = self.big_font.render(f"Pause", True, self.color_black)
        pause_size = pause_text.get_size()
        self.window.blit(pause_text, ((self.screen_size[0] - pause_size[0]) * 0.5, (self.screen_size[1] - pause_size[1]) * 0.5))
        self.DisplayTitle()
        self.DisplayGameData()

    def DisplayTitle(self):                                                     # Display game name
        if self.title_image is None:
            title = self.giant_font.render(f"{self.game_name}", True, self.color_black)
            height = self.screen_size[1] * 0.02
        else:
            title = self.title_image
            height = 30
        size = title.get_size()
        self.window.blit(title, (self.screen_size[0] * 0.5 - size[0] * 0.5, height))

    def DisplayGameData(self):                                                  # Display version and creator name
        version = self.middle_font.render(f"{self.version}", True, self.color_black)
        size = version.get_size()
        self.window.blit(version, (10, self.screen_size[1] - size[1] - 10))
        creator = self.middle_font.render(f"by {self.creator}", True, self.color_black)
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
        self.play_pausing = not self.play_pausing
        if self.play_pausing and not self.music_pausing or not self.play_pausing and self.music_pausing:
            self.PauseMusic()
            self.PauseSounds()

    @staticmethod
    def IsClose(coord1, coord2, limit=10):                                      # Check if two objects are too close
        distance = sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
        return distance <= limit

    def CheckNextLevel(self):                                                   # Update level (bubbles, bg, music...)
        if self.player.cells_eaten >= self.player.cells_eaten_max:
            self.level_index += 1
            if self.level_index > len(self.Color_names) - 1:
                self.level_index = 0
            self.color_name_bg = self.Color_names[self.level_index]             # Update Colors
            self.color_bg_start = self.Levels[self.level_index].start_color
            self.color_bg_end = self.Levels[self.level_index].end_color
            self.map_size = self.Levels[self.level_index].map_size
            NO_pos = (int(self.screen_size[0] * 0.5), int(self.screen_size[1] * 0.5))
            self.map_borders_pos = (NO_pos[0], NO_pos[1], NO_pos[0] + self.map_size[0], NO_pos[1] + self.map_size[1])
            self.background_size = [self.map_size[0] + self.screen_size[0], self.map_size[1] + self.screen_size[1]]
            self.set_background()                                               # Update gradient bg
            self.music_name = f"musics/{self.color_name_bg}.mp3"
            pygame.mixer.music.load(self.music_name)                            # Update music
            pygame.mixer.music.rewind()                                         # Change current played music
            self.LoadMapBorders()                                               # Update map borders
            self.LoadBubbles()                                                  # Update bubbles
            self.player.map_borders = self.map_borders_pos
            self.player.ChangeLevel()

    def MusicManager(self):                                                     # Change music based on card
        if not self.music_pausing:
            song_mutagen = MP3(self.music_name)                                 # Load current music data
            self.music_lenght = song_mutagen.info.length                        # Get song lenght (in sec)
            if pygame.mixer.music.get_busy():
                self.music_pos = pygame.mixer.music.get_pos() // 1000

            # If music end OR current pos is greater than music lenght
            if not pygame.mixer.music.get_busy() or self.music_pos >= self.music_lenght:
                pygame.mixer.music.load(self.music_name)
                pygame.mixer.music.play(self.play_mode)
                self.music_pos = 0

            pygame.mixer.music.set_volume(self.current_sound)

            if not self.play_pausing:
                self.bg_sound.play(-1)

    def DisplayMusicData(self):                                                 # Display title, position and sound in music
        song_lenght_format = strftime('%M:%S', gmtime(self.music_lenght))
        song_position_format = strftime('%M:%S', gmtime(self.music_pos))
        song_duration_text = self.middle_font.render(f"{song_position_format} / {song_lenght_format}", True, self.color_white)
        duration_size = song_duration_text.get_size()
        # Song name
        song_name = self.music_name.replace(".mp3", "").replace("musics/", "").capitalize()
        song_title_text = self.middle_font.render(f"{song_name}", True, self.color_white)
        title_size = song_title_text.get_size()
        gap = 15
        self.window.blit(song_title_text, (self.screen_size[0] - duration_size[0] * 0.5 - title_size[0] * 0.5 - gap, gap))
        self.window.blit(song_duration_text, (self.screen_size[0] - duration_size[0] - gap, title_size[1] + gap))
        # Sound bar
        sound_height = int(self.screen_size[1] * self.sound_bar_height_percent)
        sound_surface_bg = (self.screen_size[0] - self.sound_bar_width * 3, sound_height, self.sound_bar_width, sound_height)
        pygame.draw.rect(self.window, self.color_grey, sound_surface_bg, 0, sound_height)       # Display bg sound bar
        percent = self.current_sound / self.sound_max
        sound_surface = (self.screen_size[0] - self.sound_bar_width * 3, sound_height * 2 - int(sound_height * percent),
                         self.sound_bar_width, int(sound_height * percent))
        pygame.draw.rect(self.window, self.color_lightgrey, sound_surface, 0, sound_height)     # Display current sound

    def Mute(self):                                                             # Mute the music of the level
        self.muting = not self.muting
        self.current_sound = 0 if self.muting else self.old_sound

    def ChangeSound(self, direction=0):                                         # Change sound of music
        if direction > 0:
            self.current_sound += self.sound_gap
            self.old_sound += self.sound_gap
        elif direction < 0:
            self.current_sound -= self.sound_gap
            self.old_sound -= self.sound_gap
        self.current_sound = 0 if self.current_sound < 0 else 1 if self.current_sound > 1 else self.current_sound
        self.old_sound = 0 if self.old_sound < 0 else 1 if self.old_sound > 1 else self.old_sound

    def PauseMusic(self):                                                       # Pause the music in the game
        self.music_pausing = not self.music_pausing
        if self.music_pausing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def PauseSounds(self):                                                      # Stop the sounds in the game
        if self.play_pausing:
            self.bg_sound.stop()
        else:
            self.bg_sound.play(-1)

    def LoadGame(self):                                                         # Load last played game
        save = open(f"saves/{self.player.name}.txt", "r")
        lines = save.readlines()

        # Load player's game data
        self.level_index = int(lines[0])
        self.color_name_bg = str(lines[1]).replace("\n", "")
        self.color_bg_start = tuple(lines[2])
        self.color_bg_end = tuple(lines[3])
        self.Cells.empty()
        for _ in range(int(lines[4])):
            self.Cells.add(Bubble(map_borders=self.map_borders_pos))
        self.player.set_cells_eaten_max(len(self.Cells))
        self.Life_bubbles.empty()
        for _ in range(int(lines[5])):
            self.Life_bubbles.add(Bubble(map_borders=self.map_borders_pos))
        self.player.set_cells_eaten_max(len(self.Life_bubbles))
        self.Enemies.empty()
        for _ in range(int(lines[6])):
            self.Enemies.add(Bubble(map_borders=self.map_borders_pos))
        self.player.set_cells_eaten_max(len(self.Enemies))

        # Load player's data
        # self.player.name = datas[7]                                           # ! Add check ? (already in filename)
        self.player.rect.x = int(lines[8])
        self.player.rect.y = int(lines[9])
        self.player.life = int(lines[10])
        self.player.evolution = int(lines[11])
        self.player.length = int(lines[12])
        self.player.current_radius = float(lines[13])
        self.player.current_diameter = self.player.current_radius * 2
        self.player.membrane_width = int(self.player.current_radius * 0.1)
        self.player.cells_eaten = int(lines[14])
        self.player.Stomach = []
        for _ in range(self.player.cells_eaten):
            self.player.Stomach.append(CellEaten(player=self.player))

        save.close()

    def SaveGame(self):                                                         # Save/update current game
        save = open(f"saves/{self.player.name}.txt", "w")

        # Save current game data
        save.write(f"{self.level_index}\n")
        save.write(f"{self.color_name_bg}\n")
        save.write(f"{self.color_bg_start}\n")
        save.write(f"{self.color_bg_end}\n")
        save.write(f"{len(self.Cells)}\n")
        save.write(f"{len(self.Life_bubbles)}\n")
        save.write(f"{len(self.Enemies)}\n")
        # Save current player data
        save.write(f"{self.player.name}\n")
        save.write(f"{self.player.rect.x}\n")
        save.write(f"{self.player.rect.y}\n")
        save.write(f"{self.player.life}\n")
        save.write(f"{self.player.evolution}\n")
        save.write(f"{self.player.length}\n")
        save.write(f"{self.player.cells_eaten}\n")

        save.close()

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
