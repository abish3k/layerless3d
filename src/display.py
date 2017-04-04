import pygame

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)


class Display:
    def __init__(self):
        pass

    def play(self, figure):

        slices = figure['slices']

        ##########################
        pygame.init()
        size = [900, 600]
        info_object = pygame.display.Info()
        screen_size = (info_object.current_w, info_object.current_h)
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        # screen = pygame.display.set_mode(size)

        # Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        # while not done:

            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.


        # for event in pygame.event.get():  # User did something
        #     if event.type == pygame.QUIT:  # If user clicked close
        #         done = True  # Flag that we are done so we exit this loop

        for layer in slices:
            surface = pygame.Surface((figure['max']['x'], figure['max']['y']))
            surface.fill(BLACK)
            for pair in layer:
                pygame.draw.line(surface, WHITE, pair[0], pair[1], 5)
            scaled = pygame.transform.scale(surface, (int(figure['max']['x'] * 2), int(figure['max']['y'] * 2)))
            screen.blit(scaled, (int(screen_size[0]/6), int(screen_size[1]/8)))
            pygame.display.flip()
            clock.tick(30)

        print("Status: Finished Outputting Slices")
        pygame.quit()

if __name__ == '__main__':
    import pickle
    slices_file = open('../outputs/pkl/slices.pkl', 'rb')
    model = pickle.load(slices_file)
    slices_file.close()

    # print model

    display = Display()
    display.play(model)
