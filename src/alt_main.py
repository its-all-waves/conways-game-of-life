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
        self.grid_pos = (grid_x, grid_y)
        self.pos_px = (grid_x * CELL_W_PX, grid_y * CELL_H_PX)
        self._surface = pygame.Surface((CELL_W_PX, CELL_H_PX), pygame.SRCALPHA)

    def __repr__(self):
        return f"Cell({'🔥' if self.is_alive else '💀'}, {self.grid_pos}, {self.pos_px})"

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


cells = [
    [ Cell(x, y) for x in range(CELL_COUNT_X) ]
    for y in range(CELL_COUNT_Y)
]

cells: list[list[Cell]]

living_cells: list[pygame.Rect] = []


def main():
    # pygame setup
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{WINDOW_POS_X_PX}, {WINDOW_POS_Y_PX}'
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W_PX, SCREEN_H_PX), 
                                     pygame.SRCALPHA)
    clock = pygame.time.Clock()
    running = True

    # seed the game
    seed_cells((0, 0), (1, 1), (1, 2), (2, 2))
    draw_cells(screen)
    pygame.display.flip()
    
    # hold the seed for a frame
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < FPS * 1000:
        pygame.event.pump()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER YOUR GAME HERE

        # births and deaths occur ___simultaneously___
        to_enliven: list[Cell] = []
        to_kill: list[Cell] = []

        def conways_algo():
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

        conways_algo()

        kill(*to_kill)
        enliven(*to_enliven)

        draw_cells(screen)
        
        pygame.display.flip()  # flip() the display to put your work on screen
        clock.tick(FPS)  # limit FPS

    pygame.quit()


def seed_cells(*cell_coords: tuple[int,int]):
    for coord in cell_coords:
        x, y = coord
        cell_at((x, y)).enliven()


def enliven(*cells: Cell):
    for cell in cells:
        cell.enliven()


def kill(*cells: Cell):
    for cell in cells:
        cell.kill()


def cell_at(grid_pos) -> Cell:
    x, y = grid_pos
    return cells[y][x]


def draw_cells(surface):
    for row in cells:
        for cell in row:
            cell.draw(surface)
        

if __name__ == "__main__":
    main()