# Example file showing a basic pygame "game loop"
import pygame
import os

# pygame setup
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0}, {0}'

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
running = False

# await user input
while not running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: 
            # right click starts the game
            print("\nGAME STARTED\n")
            running = True



while running: 
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()