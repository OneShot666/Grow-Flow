import pygame

pygame.init()

# Obtenir la liste des polices disponibles
polices = pygame.font.get_fonts()

# Afficher la liste des polices
for police in polices:
    print(police)

pygame.quit()
