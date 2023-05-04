import pygame
import pygame_gui

pygame.init()

width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Resizable Window Example')

manager = pygame_gui.UIManager((width, height))
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)), text='Click me!', manager=manager)

clock = pygame.time.Clock()

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    print('Button pressed!')

        manager.process_events(event)

    manager.update(time_delta)
    window_surface = pygame.display.get_surface()
    window_surface.fill(pygame.Color('#000000'))
    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
