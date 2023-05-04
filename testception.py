import pygame

pygame.init()

width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Resizable Window Example')

clock = pygame.time.Clock()

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            width, height = event.size

    window.fill(pygame.Color('#000000'))
    pygame.draw.rect(window, pygame.Color('#FFFFFF'), pygame.Rect(100, 100, 200, 200))
    pygame.display.update()

pygame.quit()
