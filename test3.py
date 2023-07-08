import pygame
from math import *
from random import *

""" [later] Bulles dans player """

pygame.init()
largeur = 800
hauteur = 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Rebond de cercle à l'intérieur d'un autre cercle")
clock = pygame.time.Clock()

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

# Grand cercle
grand_rayon = 200
grand_cercle_pos = [largeur // 2, hauteur // 2]

# Petit cercle
petit_rayon = 50
petit_cercle_pos = [grand_cercle_pos[0], grand_cercle_pos[1]]
petit_cercle_vit = 2                                        # Pixel by frame
direction = randint(0, 360)
dispersion = 30


def calculer_vitesse(angle):                                # Calcul vitesse avec direction (en degré)
    angle_radians = radians(angle)
    vx = petit_cercle_vit * cos(angle_radians)
    vy = petit_cercle_vit * sin(angle_radians)
    return vx, vy


# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la position du cercle 2
    vx, vy = calculer_vitesse(direction)
    petit_cercle_pos[0] += vx
    petit_cercle_pos[1] += vy

    # Distance entre les centres des cercles
    distance = int(sqrt((petit_cercle_pos[0] - grand_cercle_pos[0]) ** 2 + (petit_cercle_pos[1] - grand_cercle_pos[1]) ** 2))

    if distance + petit_rayon > grand_rayon:                # Si cercles se touchent
        direction = direction % 360 if direction > 360 else direction % -360 if direction < -360 else direction
        direction = - abs(direction - randint(180 - dispersion, 180 + dispersion))
        print(f"{direction}°")

    # Effacement de l'écran
    fenetre.fill((0, 0, 0))

    # Dessin des cercles
    pygame.draw.circle(fenetre, BLANC, grand_cercle_pos, grand_rayon)
    pygame.draw.circle(fenetre, ROUGE, petit_cercle_pos, petit_rayon)

    # Mise à jour de l'affichage
    pygame.display.flip()

    clock.tick(100)

pygame.quit()
