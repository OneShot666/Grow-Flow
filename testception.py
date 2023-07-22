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
