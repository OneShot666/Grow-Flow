<<<<<<< HEAD
from math import sqrt
import pygame
import sys

""" Make static object collide with player """

# Initialize Pygame
pygame.init()

# Window dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Circle and Rectangle Collision")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player properties
player_radius = 20
player_x, player_y = width // 2, height // 2
player_speed = 5

# Rectangle properties
rect_width, rect_height = 100, 50
rect_x, rect_y = 300, 200
rect_speed = 1


def getMinDistance(objet1, objet2):
    minDist1 = sqrt((objet1.x - objet2.x) ** 2 + (objet1.y - objet2.y) ** 2)
    minDist2 = sqrt((objet1.x - objet2.x) ** 2 + (objet1.height - objet2.height) ** 2)
    minDist3 = sqrt((objet1.width - objet2.width) ** 2 + (objet1.y - objet2.y) ** 2)
    minDist4 = sqrt((objet1.width - objet2.width) ** 2 + (objet1.height - objet2.height) ** 2)
    return min(minDist1, minDist2, minDist3, minDist4)


def CheckCollision(objet1, objet2):
    if getMinDistance(objet1, objet2) <= 0:
        return True
    return False


# Player class
class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.width = radius
        self.height = radius
        self.radius = radius
        self.image = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= player_speed
        if keys[pygame.K_RIGHT]:
            self.x += player_speed
        if keys[pygame.K_UP]:
            self.y -= player_speed
        if keys[pygame.K_DOWN]:
            self.y += player_speed

    def draw(self, surface):
        self.image = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        pygame.draw.rect(surface, RED, self.image)


# Rectangle class
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dir_x = 1
        self.dir_y = 1

    def move(self):
        self.x += self.dir_x * rect_speed
        self.y += self.dir_y * rect_speed

    def reverse_direction(self):
        self.dir_x *= -1
        self.dir_y *= -1

    def draw(self, surface):
        self.image = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, BLUE, self.image)


# Create player and rectangle objects
player = Player(player_x, player_y, player_radius)
rectangle = Rectangle(rect_x, rect_y, rect_width, rect_height)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
        break
    player.move(keys)

    # Rectangle movement
    rectangle.move()

    # Check collision between player and rectangle
    if CheckCollision(player, rectangle):
        rectangle.reverse_direction()

    """ Collisions
    if player.y + player.radius > rectangle.rect.y and player.y - player.radius < rectangle.rect.y + rectangle.rect.height:
        if player.x + player.radius > rectangle.rect.x and player.x - player.radius < rectangle.rect.x + rectangle.rect.width:
            rectangle.reverse_direction_y()  # Reverse the direction of the rectangle
    """

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player and rectangle
    player.draw(screen)
    rectangle.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)
=======
import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width = 800
height = 600

# Création de la fenêtre
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cercles qui fuient")

# Couleurs
black = (0, 0, 0)
white = (255, 255, 255)

# Position et rayon du cercle qui bouge
circle_x = random.randint(100, width-100)
circle_y = random.randint(100, height-100)
circle_radius = 50

# Position et rayon du cercle fixe
target_x = width // 2
target_y = height // 2
target_radius = 100

# Vitesse de déplacement du cercle
speed = 2

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement du cercle de manière aléatoire
    circle_x += random.randint(-speed, speed)
    circle_y += random.randint(-speed, speed)

    # Vérifier les limites de l'écran pour le cercle
    if circle_x - circle_radius < 0:
        circle_x = circle_radius
    elif circle_x + circle_radius > width:
        circle_x = width - circle_radius
    if circle_y - circle_radius < 0:
        circle_y = circle_radius
    elif circle_y + circle_radius > height:
        circle_y = height - circle_radius

    # Calculer la distance entre les cercles
    distance = math.sqrt((circle_x - target_x)**2 + (circle_y - target_y)**2)

    # Vérifier si les cercles se rapprochent trop
    if distance < target_radius + circle_radius:
        # Inverser la direction du cercle
        circle_x -= 2 * (circle_x - target_x)
        circle_y -= 2 * (circle_y - target_y)

    # Effacer l'écran
    window.fill(black)

    # Tracer le cercle qui bouge
    pygame.draw.circle(window, white, (circle_x, circle_y), circle_radius)

    # Tracer le cercle fixe
    pygame.draw.circle(window, white, (target_x, target_y), target_radius, 2)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
>>>>>>> ed9edcda081085d7d4b5b6daa23dc070c32dbaaa
