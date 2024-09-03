# Conway's Game of Life
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

## Rules

- a cell is either alive or dead (filled or not)
- a cell interacts will all 8 surrounding neighbors
- the initial pattern is the "seed" of the system
- each step/generation is a "tick"
- ___births and deaths occur simultaneously___

1. a live cell with < 2 live neighbors dies
2. a live cell with two or three live neighbors lives on to next gen
3. a live cell with > 3 live neighbors dies, as if by overpopulation 
4. any dead cell with exactly 3 live neighbors becomes a live cell, as if by reproduction


## Pseudocode
```
create a grid of cells

loop:
    for each cell:
        count the number of live neighbors
        if cell is live:
            if live neighbors < 2: cell dies
            if live neighbors == 2 or 3 < : cell lives on
            if live neighbors > 3: cell dies 
        if cell is dead:
            if live neighbors == 3: cell lives
```


## Roadmap

- [x] create a grid on the screen
- [x] give life to cells (fill them)
- [x] kill living cells (clear them)
- [x] step the program (increase length of a tick)
- [x] move the seed out of the main loop
- [ ] start running on click anywhere in screen
- [ ] add start button
- [ ] seed the game by clicking / dragging over cells
- [ ] indicate when game has ended (all cells have died)
- [ ] add pause button