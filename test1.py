import pygame
import pygame_menu
import math

""" Menus Pygame (ne pas utilisé pour le jeu) """


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.level_difficulty = "Middle"
        self.level_index = 1
        self.bg_color = (84, 210, 250)  # Couleur de fond
        self.border_color = (216, 160, 255)  # Couleur des rebords
        self.bubble_color = (193, 136, 251)  # Couleur de la bulle
        self.reflection_color = (200, 200, 255, 100)  # Couleur du reflet
        self.clock = pygame.time.Clock()
        self.launch_game()

    def launch_game(self):
        menu = pygame_menu.Menu('Game name', self.width * 0.5, self.height * 0.75, theme=pygame_menu.themes.THEME_DARK)

        menu.add.text_input('Name : ', default='Player name')
        menu.add.button('Play', self.manage_summary)
        menu.add.selector('Difficulty : ', [('Easy', 0), ('Middle', 1), ('Hard', 2), ('Impossible', 3)], default=1,
                          onchange=self.set_difficulty)
        menu.add.selector('Select level : ', [('1', 0), ('2', 1)], default=0, onchange=self.set_level_index)
        menu.add.button('Check level', self.show_level_data)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        # widget = menu.get_widget('MyWidgetID')
        # selected = menu.get_selected_widget()

        menu.mainloop(self.screen)

    def set_difficulty(self, difficulty, *args):
        self.level_difficulty = difficulty[0][0]
        if args:
            pass

    def set_level_index(self, level_index, *args):
        self.level_index = int(level_index[0][0])
        if args:
            pass

    def manage_summary(self):
        if self.level_index == 1:
            self.launch_level_1()
        elif self.level_index == 2:
            self.launch_level_2()

    def launch_level_1(self):                               # Bubble bumping at the edges of the window
        # Chargement de l'image
        player_size = 100
        image = pygame.image.load(f"images/player1.png")  # Remplacez "image.png" par le chemin de votre image
        image = pygame.transform.scale(image, (player_size, player_size))
        # image_mask = pygame.mask.from_surface(image)

        rect = image.get_rect()
        rect.x = (self.width - player_size) // 2
        rect.y = (self.height - player_size) // 2
        direction_x = 1
        direction_y = 1
        player_speed = 5

        # Création de la surface circulaire
        circle_surface = pygame.Surface((rect.x, rect.y), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (255, 255, 255), (player_size // 2, player_size // 2), player_size // 2)

        # Application du masque à la surface circulaire
        circle_surface.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Boucle principale du jeu
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("lightblue")

            self.screen.blit(circle_surface, (rect.x, rect.y))

            # Vérifier les collisions avec les bords de la fenêtre
            if rect.x <= 0 or rect.x >= self.width - player_size:
                direction_x *= -1
            if rect.y <= 0 or rect.y >= self.height - player_size:
                direction_y *= -1

            rect.x += direction_x * player_speed
            rect.y += direction_y * player_speed

            pygame.display.flip()

            self.clock.tick(20)

    def launch_level_2(self):                               # Fake turning moonlight
        min_fps = 5
        fps = min_fps

        BLANC = (255, 255, 255)
        NOIR = (0, 0, 0)

        # Position et taille du croissant de lune
        x = 400
        y = 300
        rayon_exterieur = 200
        rayon_interieur = 100
        angle_rotation = 0

        # Boucle de jeu
        self.running = True
        while self.running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Effacer l'écran avec un fond transparent
            self.screen.fill((0, 0, 0, 0))

            # Calculer les coordonnées des points du croissant de lune
            angle = math.radians(angle_rotation)
            x_exterieur = x + rayon_exterieur * math.cos(angle)
            y_exterieur = y + rayon_exterieur * math.sin(angle)
            x_interieur = x + rayon_interieur * math.cos(angle)
            y_interieur = y + rayon_interieur * math.sin(angle)

            # Dessiner le croissant de lune
            pygame.draw.ellipse(self.screen, BLANC, (
                x_exterieur - rayon_exterieur, y_exterieur - rayon_exterieur, rayon_exterieur * 2, rayon_exterieur * 2))
            pygame.draw.ellipse(self.screen, NOIR, (
                x_interieur - rayon_interieur, y_interieur - rayon_interieur, rayon_interieur * 2, rayon_interieur * 2))

            # Rotation de l'angle
            angle_rotation += 1

            pygame.display.flip()

            fps += 1 if angle_rotation % 361 < 180 else -1
            fps = min_fps if fps < min_fps else fps
            self.clock.tick(fps)

    def show_level_data(self):
        print(f"Level {self.level_index} : difficulty '{self.level_difficulty}'")


if __name__ == "__main__":
    Game()
