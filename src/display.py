import pygame

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)


class Display:
    def __init__(self):
        pass

    def play(self, slices):
        ##########################
        pygame.init()
        size = [900, 600]
        screen = pygame.display.set_mode(size)

        # Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        while not done:

            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.


            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            for layer in slices:
                screen.fill(BLACK)
                for pair in layer:
                    pygame.draw.line(screen, WHITE, pair[0], pair[1], 5)
                pygame.display.flip()
                clock.tick(30)

        print("Status: Finished Outputting Slices")
        pygame.quit()


if __name__ == '__main__':
    import pickle
    slices_file = open('outputs/pkl/slices.pkl', 'rb')
    slices = pickle.load(slices_file)
    slices_file.close()

    display = Display()
    display.play(slices)
