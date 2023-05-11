import pygame

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLAYER_COLOR = (255, 0, 0)  # Rouge

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Déplacement du personnage avec la souris")
clock = pygame.time.Clock()


# Définition de la classe Player
class Player:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def move_towards(self, x, y, speed):
        # Calcul de la distance en x et y entre le joueur et la position de la souris
        dx = x - self.x
        dy = y - self.y
        distance = max(abs(dx), abs(dy))

        # Si la distance est inférieure à la vitesse, on déplace le joueur directement sur la position de la souris
        if distance <= speed:
            self.x = x
            self.y = y
        else:
            # Sinon, on déplace le joueur vers la position de la souris à une vitesse donnée
            direction_x = dx / distance
            direction_y = dy / distance
            self.x += direction_x * speed
            self.y += direction_y * speed


# Création du joueur
player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_COLOR)

# Boucle de jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement du joueur vers la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.move_towards(mouse_x - PLAYER_SIZE // 2, mouse_y - PLAYER_SIZE // 2, 5)

    # Effacement de l'écran
    screen.fill((255, 255, 255))

    # Dessin du joueur
    player.draw(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(50)

# Fermeture de Pygame
pygame.quit()
