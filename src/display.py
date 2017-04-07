import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE, QUIT, KEYDOWN, K_f, FULLSCREEN, NOFRAME

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
        screen = pygame.display.set_mode(screen_size, RESIZABLE)

        surfaces = []
        for layer in slices:
            surface = pygame.Surface((figure['max']['x'], figure['max']['y']))
            surface.fill(BLACK)
            for pair in layer:
                pygame.draw.line(surface, WHITE, pair[0], pair[1], 3)
            surfaces.append(surface)

        # Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()


        cur_screen_size = screen.get_size()

        while not done:
            for surface in surfaces:

                for event in pygame.event.get():  # User did something
                    if event.type == QUIT:  # If user clicked close
                        done = True  # Flag that we are done so we exit this loop
                        break
                    elif event.type == VIDEORESIZE:
                        cur_screen_size = event.dict['size']
                        screen = pygame.display.set_mode(cur_screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                    elif event.type == KEYDOWN and event.key == K_f:
                        if screen.get_flags() == NOFRAME:
                            screen = pygame.display.set_mode(cur_screen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
                        else:
                            screen = pygame.display.set_mode(cur_screen_size, HWSURFACE | DOUBLEBUF | NOFRAME)

                    if done:
                        break
                if done:
                    break

#<<<<<<< Updated upstream
                mod_surface = self.aspect_scale(surface, cur_screen_size)
                offset = self.center_surface(mod_surface, screen)
                screen.blit(mod_surface, offset)
                pygame.display.flip()
                clock.tick(0.3)
#=======
       #for layer in slices:
          # surface = pygame.Surface((figure['max']['x'], figure['max']['y']))
           #surface.fill(BLACK)
           #for pair in layer:
               #pygame.draw.line(surface, WHITE, pair[0], pair[1], 2)
          # scaled = pygame.transform.scale(surface, (int(figure['max']['x'] * 2), int(figure['max']['y'] * 2)))
           #screen.blit(scaled, (int(screen_size[0]/6), int(screen_size[1]/8)))
           #pygame.display.flip()
           #clock.tick(60)

       #pygame.quit()

    #>>>>>>> Stashed changes


    def aspect_scale(self, img, (bx, by)):
        """ Scales 'img' to fit into box bx/by.
         This method will retain the original image's aspect ratio """
        ix, iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx / float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by / float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx / float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by

        return pygame.transform.scale(img, (int(sx), int(sy)))

    def center_surface(self, surface, screen):
        screen_size = screen.get_size()
        surface_size = surface.get_size()

        pos_x = (screen_size[0] - surface_size[0]) / 2
        pos_y = (screen_size[1] - surface_size[1]) / 2

        return pos_x, pos_y


if __name__ == '__main__':
    import pickle
    slices_file = open('../outputs/pkl/slices.pkl', 'rb')
    model = pickle.load(slices_file)
    slices_file.close()

    #print model

    display = Display()
    display.play(model)
