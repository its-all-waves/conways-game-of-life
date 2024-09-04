from dataclasses import dataclass
import os
import random

import pygame


WINDOW_POS_X_PX = 0
WINDOW_POS_Y_PX = 0
SCREEN_W_PX = 900
SCREEN_H_PX = 900

TRUE_FPS = 5  # frames / sec
# TODO: APPARENT_FPS = 5  # the perceived FPS (we want fps to be slow, but setting it slow results in poor event processing performance / slooow response to user events)

GRID_BORDER_X_PX = 100
GRID_BORDER_Y_PX = 100
GRID_W_PX = SCREEN_W_PX - GRID_BORDER_X_PX
GRID_H_PX = SCREEN_H_PX - GRID_BORDER_Y_PX

CELL_COUNT_X = 150
CELL_COUNT_Y = 150
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
    def __init__(self, grid_x, grid_y):
        self.is_alive = False
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_pos = (grid_x, grid_y)
        self.pos_px = (grid_x * CELL_W_PX, grid_y * CELL_H_PX)
        self._surface = pygame.Surface((CELL_W_PX, CELL_H_PX), pygame.SRCALPHA)


    def __repr__(self):
        return f"Cell({'🔥' if self.is_alive else '💀'}, {self.grid_pos})"


    def draw(self, surface, *, shape='circle', grid_lines=False):
        if self.is_alive:
            if shape == 'rect' or shape == 'rectangle':
                pygame.draw.rect(
                    surface, 
                    WHITE,
                    self._surface.get_rect(topleft=self.pos_px)
                )
            elif shape == 'circle':
                x, y = self.pos_px
                x -= CELL_W_PX // 2
                y -= CELL_H_PX // 2
                pygame.draw.circle(
                    surface,
                    WHITE,
                    center=(x, y),
                    radius=CELL_W_PX // 2
                )
        elif not self.is_alive:
            if grid_lines:
                pygame.draw.rect(
                    surface, 
                    (50, 50, 50),
                    self._surface.get_rect(topleft=self.pos_px),
                    1  # border only
                )


    def enliven(self):
        self.is_alive = True


    def kill(self):
        self.is_alive = False


# END class Cell
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


cells = [
    [ Cell(x, y) for x in range(CELL_COUNT_X) ]
    for y in range(CELL_COUNT_Y)
]


def main():
    # pygame setup
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{WINDOW_POS_X_PX}, {WINDOW_POS_Y_PX}'
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W_PX, SCREEN_H_PX), 
                                     pygame.SRCALPHA)
    clock = pygame.time.Clock()
    
    running = False
    game_is_seeded = False

    selected_cell_coords: list[tuple[int,int]] = []
    cell_coords_to_seed: list[tuple[int,int]] = []

    # await user input to start the game
    while not running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_is_seeded:
                    # LEFT CLICK cells to select them for the seed
                    selected_cell_coords.append(
                        cell_grid_pos_at(event.pos)
                    )
                    cell = cell_at((cell_grid_pos_at(event.pos)))
                    cell.enliven()
                    print("\nSELECTING CELLS\n")

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    # R KEY randomizes the seed and immediately starts game
                    cell_coords_to_seed = random_coordinates()
                    game_is_seeded = True
                    running = True
                    
                elif event.key == pygame.K_RETURN and len(selected_cell_coords) > 0:
                    # ENTER KEY saves the selected cells
                    print("\nGAME IS SEEDED\n")
                    cell_coords_to_seed = selected_cell_coords
                    game_is_seeded = True

                elif event.key == pygame.K_SPACE and game_is_seeded:
                    # SPACE BAR starts game once cells are selected & saved
                    print("\nGAME STARTED\n")
                    running = True

        draw_cells(screen)
        pygame.display.flip()
        # clock.tick(FPS)  # causes problems when FPS is low -- processes events in a frame
        
    # seed the game with user's selection
    seed_cells(*cell_coords_to_seed)
    draw_cells(screen)
    pygame.display.flip()
    
    # hold the seed for a frame
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < TRUE_FPS / 5 * 1000:
        pygame.event.pump()

    # MAIN LOOP ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # TODO: add continue if timer is not what I want


        screen.fill("black")  # clear the last frame 

        # RENDER YOUR GAME HERE

        to_kill, to_enliven = conways_algo()
        kill(*to_kill)
        enliven(*to_enliven)

        draw_cells(screen)
        
        pygame.display.flip()   # put work on the screen
        clock.tick(TRUE_FPS)    # limit FPS

    # END MAIN LOOP ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    pygame.quit()

# END MAIN() +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def seed_cells(*cell_coords: tuple[int,int]):
    for coord in cell_coords:
        x, y = coord
        cell_at((x, y)).enliven()


def conways_algo():
    # births and deaths occur ___simultaneously___
    to_enliven: list[Cell] = []
    to_kill: list[Cell] = []
    
    # compute living cells
    for row in cells:
        for cell in row:
            # count the living cells in the surrounding 8
            x, y = cell.grid_pos

            top_left    =   (x - 1, y - 1)
            top_mid     =   (x,     y - 1)
            top_right   =   (x + 1, y - 1)
            mid_left    =   (x - 1, y    )
            
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

            neighbor_grid_coords: list[tuple[int,int] | None] = [
                top_left,   top_mid,    top_right,
                mid_left,   None,       mid_right,  # None -> don't count this cell
                bot_left,   bot_mid,    bot_right
            ]

            living_neighbors = []
            for coords in neighbor_grid_coords:
                if not coords: continue
                neighbor = cell_at(coords)
                if not neighbor.is_alive: continue
                living_neighbors.append(neighbor)

            living_neighbors_count = len(living_neighbors)

            if not cell.is_alive:
                # RULE: any dead cell with exactly 3 live neighbors becomes a live cell, as if by reproduction
                if living_neighbors_count == 3: 
                    to_enliven.append(cell)

            elif cell.is_alive:
                # RULE: a live cell with < 2 live neighbors dies
                if living_neighbors_count < 2: 
                    to_kill.append(cell) 
                    
                # RULE: a live cell with two or three live neighbors lives on to next gen 
                elif living_neighbors_count in (2, 3): 
                    continue

                # RULE: a live cell with > 3 live neighbors dies, as if by overpopulation
                elif living_neighbors_count > 3: 
                    to_kill.append(cell)
        
    return to_kill, to_enliven


def enliven(*cells: Cell):
    for cell in cells:
        cell.enliven()


def kill(*cells: Cell):
    for cell in cells:
        cell.kill()


def cell_at(grid_pos: tuple[int,int]) -> Cell:
    x, y = grid_pos
    return cells[y][x]


def draw_cells(surface, *, shape='circle', grid_lines=False):
    for row in cells:
        for cell in row:
            cell.draw(surface, shape=shape, grid_lines=grid_lines)


def cell_grid_pos_at(pos_px):
    x, y = pos_px
    cell_x = x // CELL_W_PX
    cell_y = y // CELL_H_PX
    return cell_x, cell_y


def random_coordinates():
    # get a rand int bt 0 and total cell count - this is number of rand coords to return
    rand_count = random.randint(0, CELL_COUNT_X * CELL_COUNT_Y)

    # get populations to pick from 
    x_choices = tuple(range(CELL_COUNT_X))
    y_choices = tuple(range(CELL_COUNT_Y))

    # get random choices from these using the random count above
    
    x_choices_random = random.choices(population=x_choices, k=rand_count) 
    y_choices_random = random.choices(population=y_choices, k=rand_count) 


    # x_choices_random = random.sample(population=x_choices, k=CELL_COUNT_X)
    # y_choices_random = random.sample(population=y_choices, k=CELL_COUNT_Y)


    return list(zip(x_choices_random, y_choices_random))


if __name__ == "__main__":
    main()