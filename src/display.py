import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE, QUIT

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)


class Display:
    def __init__(self):
        pass

    def play(self, figure):

        slices = figure['slices']

        ##########################
        pygame.init()
        info_object = pygame.display.Info()
        screen_size = (info_object.current_w, info_object.current_h)
        screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

        surfaces = []
        for layer in slices:
            surface = pygame.Surface((figure['max']['x'], figure['max']['y']))
            surface.fill(BLACK)
            for pair in layer:
                pygame.draw.line(surface, WHITE, pair[0], pair[1], 5)
            surfaces.append(surface)

        # Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        cur_screen_size = screen.get_size()

        for surface in surfaces:
            pygame.event.pump()
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                cur_screen_size = event.dict['size']
                screen = pygame.display.set_mode(cur_screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)

            screen.blit(pygame.transform.scale(surface, cur_screen_size), (0, 0))
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == '__main__':
    import pickle
    slices_file = open('../outputs/pkl/slices.pkl', 'rb')
    model = pickle.load(slices_file)
    slices_file.close()

    # print model

    display = Display()
    display.play(model)
