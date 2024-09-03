from dataclasses import dataclass
import os
import pygame


# constants
WINDOW_POS_X_PX = 0
WINDOW_POS_Y_PX = 0
SCREEN_W_PX = 400
SCREEN_H_PX = 400

FPS = 1  # frames / sec

GRID_BORDER_X_PX = 100
GRID_BORDER_Y_PX = 100
GRID_W_PX = SCREEN_W_PX - GRID_BORDER_X_PX
GRID_H_PX = SCREEN_H_PX - GRID_BORDER_Y_PX

CELL_COUNT_X = 4
CELL_COUNT_Y = 4
CELL_W_PX = SCREEN_W_PX // CELL_COUNT_X
CELL_H_PX = SCREEN_H_PX // CELL_COUNT_Y

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRID_COLOR = WHITE
CELL_COLOR = WHITE
BG_COLOR = BLACK

@dataclass
class Cell:
    def __init__(
        self, 
        grid_x, 
        grid_y
    ):
        self.is_alive = False
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_px = (grid_x * CELL_W_PX, grid_y * CELL_H_PX)
        self._surface = pygame.Surface((CELL_W_PX, CELL_H_PX), pygame.SRCALPHA)

    def __repr__(self):
        return f"Cell({self.grid_x, self.grid_y}, {self.pos_px})"

    def draw(self, surface):
        if self.is_alive:
            pygame.draw.rect(surface, 
                             WHITE,
                             self._surface.get_rect(topleft=self.pos_px))
        else:
            pygame.draw.rect(surface, 
                             GREEN,
                             self._surface.get_rect(topleft=self.pos_px),
                             1)  # border only


    def enliven(self):
        self.is_alive = True


    def kill(self):
        self.is_alive = False


# END class Cell
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# cells: list[list[bool]] = [
#     [ False for _ in range(CELL_COUNT_X) ]
#     for _ in range(CELL_COUNT_Y)
# ]

cells = [
    [ Cell(x, y) for x in range(CELL_COUNT_X) ]
    for y in range(CELL_COUNT_Y)
]

living_cells: list[pygame.Rect] = []

def main():
    # pygame setup
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{WINDOW_POS_X_PX}, {WINDOW_POS_Y_PX}'
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W_PX, SCREEN_H_PX), 
                                     pygame.SRCALPHA)
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER YOUR GAME HERE
        
        
        for row in cells:
            for cell in row:
                cell.draw(screen)




        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()