# Example file showing a circle moving on screen
import pygame
import pygame.gfxdraw

# constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
CELLS_X = 9
CELLS_Y = 9
CELL_WIDTH = SCREEN_WIDTH // CELLS_X
CELL_HEIGHT = SCREEN_HEIGHT // CELLS_Y

cells = [
    [ False for _ in range(CELLS_X) ]
    for _ in range(CELLS_Y)
]


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw the grid -- can i move this outside the main loop?
        for i_row in range(len(cells)):
            pygame.gfxdraw.hline(
                screen, 
                0, SCREEN_WIDTH, 
                (i_row + 1) *  CELL_HEIGHT, 
                (255, 255, 255)
            ) 
            for i_col in range(i_row):
                pygame.gfxdraw.vline(
                    screen, 
                    (i_col + 1) * CELL_WIDTH, 
                    0, SCREEN_HEIGHT, 
                    (255, 255, 255)
                )


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
 

if __name__ == "__main__":
    main()