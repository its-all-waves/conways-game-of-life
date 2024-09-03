# Example file showing a circle moving on screen
import os

import pygame
import pygame.gfxdraw

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


START_BUTTON_DIM_PX = (GRID_BORDER_X_PX, 100)
START_BUTTON_POS_PX = (SCREEN_W_PX-1 - START_BUTTON_DIM_PX[0] , 0)
START_BUTTON_COLOR = GREEN


cells: list[list[bool]] = [
    [ False for _ in range(CELL_COUNT_X) ]
    for _ in range(CELL_COUNT_Y)
]

living_cells: list[pygame.Rect] = []


def main():
    # set window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{WINDOW_POS_X_PX}, {WINDOW_POS_Y_PX}'

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W_PX, SCREEN_H_PX))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # # seed the game
    # enliven_cells((0, 0), (1, 1), (1, 2), (2, 2))
    # draw_grid(screen)
    # draw_living_cells(screen)
    # pygame.display.flip()
    
    # # hold the first frame
    # start_time = pygame.time.get_ticks()
    # while pygame.time.get_ticks() - start_time < FPS * 1000:
    #     pygame.event.pump()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # fill the screen with a color to wipe away anything from last frame
        clear_screen(screen)

        # draw start button
        start_button_surface = pygame.Surface(START_BUTTON_POS_PX)
        start_button = pygame.draw.rect(
            screen,
            START_BUTTON_COLOR, 
            pygame.Rect(START_BUTTON_POS_PX, START_BUTTON_DIM_PX),
        )
        font = pygame.font.SysFont(None, 24)
        img = font.render('hello', True, BLACK)
        start_button_surface.blit(img, start_button.center)




        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # MY CODE

        # births and deaths occur ___simultaneously___
        to_enliven = set()
        to_kill = set()

        # compute the living cells based on current state
        for y, row in enumerate(cells):
            for x, cell_alive in enumerate(row):
                # check the surrounding 8 cells
                top_left    =   (x - 1, y - 1)
                top_mid     =   (x,     y - 1)
                top_right   =   (x + 1, y - 1)
                mid_left    =   (x - 1, y    )
                this_cell   =   None            # don't count this cell
                mid_right   =   (x + 1, y    )
                bot_left    =   (x - 1, y + 1)
                bot_mid     =   (x,     y + 1)
                bot_right   =   (x + 1, y + 1)

                if x == 0:
                    top_left = mid_left = bot_left = None
                elif x == CELL_COUNT_X - 1:
                    top_right = mid_right = bot_right = None
                if y == 0:
                    top_left = top_mid = top_right = None
                elif y == CELL_COUNT_Y - 1:
                    bot_left = bot_mid = bot_right = None

                neighbors: list[tuple[int,int] | None] = [
                    top_left,   top_mid,    top_right,
                    mid_left,   this_cell,  mid_right,
                    bot_left,   bot_mid,    bot_right
                ]

                living_neighbors = [
                    (coords[0], coords[1]) 
                    for coords in neighbors
                    if coords is not None
                    and cells[coords[1]][coords[0]] == True
                ]

                living_neighbors_count = len(living_neighbors)

                this_cell = (x, y)
                
                if not cell_alive: 
                    # 4. any dead cell with exactly 3 live neighbors becomes a live cell, as if by reproduction
                    if living_neighbors_count == 3: 
                        to_enliven.add(this_cell)
                
                elif cell_alive:
                    # 1. a live cell with < 2 live neighbors dies
                    if living_neighbors_count < 2: 
                        to_kill.add(this_cell) 
                         
                    # 2. a live cell with two or three live neighbors lives on to next gen 
                    elif living_neighbors_count in (2, 3): 
                        continue

                    # 3. a live cell with > 3 live neighbors dies, as if by overpopulation
                    elif living_neighbors_count > 3: 
                        to_kill.add(this_cell)

        kill_cells(*to_kill)
        enliven_cells(*to_enliven)
        
        draw_grid(screen)
        draw_living_cells(screen)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(FPS) / 1000

    pygame.quit()


def clear_screen(screen):
    screen.fill(BG_COLOR)


def draw_grid(screen):
    for i_row in range(len(cells)):
        pygame.gfxdraw.hline(
                screen, 
                0, GRID_W_PX, 
                (i_row + 1) * CELL_H_PX, 
                GRID_COLOR
            ) 
        for i_col in range(i_row):
            pygame.gfxdraw.vline(
                    screen, 
                    (i_col + 1) * CELL_W_PX, 
                    0, GRID_H_PX, 
                    GRID_COLOR
                )


def draw_living_cells(screen):
    for y, row in enumerate(cells):
        for x, cell_alive in enumerate(row):
            if not cell_alive: continue
            living_cells.append(
                pygame.draw.rect(
                    screen, CELL_COLOR, 
                    pygame.Rect(
                        x * CELL_W_PX, y * CELL_H_PX, 
                        CELL_W_PX, CELL_H_PX
                    )
            ))


def enliven_cells(*cell_coords):
    for x, y in cell_coords:
        cells[y][x] = True


def kill_cells(*cell_coords):
    for x, y in cell_coords:
        cells[y][x] = False


if __name__ == "__main__":
    main()