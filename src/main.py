# Example file showing a circle moving on screen
from ast import Tuple
import enum
from time import sleep
from typing import Literal
from venv import create
import pygame
import pygame.gfxdraw

# constants
SCREEN_W_PX = 900
SCREEN_H_PX = 900
CELL_COUNT_X = 9
CELL_COUNT_Y = 9
CELL_WIDTH = SCREEN_W_PX // CELL_COUNT_X
CELL_HEIGHT = SCREEN_H_PX // CELL_COUNT_Y
GRID_COLOR = (255, 255, 255)
CELL_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

cells: list[list[bool]] = [
    [ False for _ in range(CELL_COUNT_X) ]
    for _ in range(CELL_COUNT_Y)
]

living_cells: list[pygame.Rect] = []


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W_PX, SCREEN_H_PX))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # seed the game
    enliven_cells(screen, 
                  (0, 0), 
                  (CELL_COUNT_X - 1, CELL_COUNT_Y - 1))

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        clear_screen(screen)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # MY CODE



        draw_grid(screen)

        draw_living_cells(screen)

        kill_cells((0, 0))



        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


def clear_screen(screen):
    screen.fill(BG_COLOR)


def draw_grid(screen):
    for i_row in range(len(cells)):
        pygame.gfxdraw.hline(
                screen, 
                0, SCREEN_W_PX, 
                (i_row + 1) *  CELL_HEIGHT, 
                GRID_COLOR
            ) 
        for i_col in range(i_row):
            pygame.gfxdraw.vline(
                    screen, 
                    (i_col + 1) * CELL_WIDTH, 
                    0, SCREEN_H_PX, 
                    GRID_COLOR
                )


def enliven_cells(screen, *cell_coords):
    for x, y in cell_coords:
        cells[y][x] = True


def kill_cells(*cell_coords):
    for x, y in cell_coords:
        cells[y][x] = False


def draw_living_cells(screen):
    for y, row in enumerate(cells):
        for x, cell_alive in enumerate(row):
            if not cell_alive: continue
            living_cells.append(
                pygame.draw.rect(
                    screen, CELL_COLOR, 
                    pygame.Rect(
                        x * CELL_WIDTH, y * CELL_HEIGHT, 
                        CELL_WIDTH, CELL_HEIGHT
                    )
            ))


if __name__ == "__main__":
    main()