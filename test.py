import pygame
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


# Classe du personnage
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self, keys):
        # Vecteurs de déplacement
        x_dir = 0
        y_dir = 0

        # Gestion des touches enfoncées
        if keys[pygame.K_LEFT]:
            x_dir -= 1
        if keys[pygame.K_RIGHT]:
            x_dir += 1
        if keys[pygame.K_UP]:
            y_dir -= 1
        if keys[pygame.K_DOWN]:
            y_dir += 1

        # Calcul de la distance à parcourir
        distance = math.sqrt(x_dir ** 2 + y_dir ** 2)
        if distance != 0:
            # Calcul de la direction de déplacement
            x_dir /= distance
            y_dir /= distance

            # Mise à jour de la position
            self.rect.x += x_dir * self.speed
            self.rect.y += y_dir * self.speed


# Création du joueur
player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Liste des sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Boucle de jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches enfoncées
    keys = pygame.key.get_pressed()

    # Mise à jour des sprites
    all_sprites.update(keys)

    # Affichage
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)

# Fermeture de Pygame
pygame.quit()
