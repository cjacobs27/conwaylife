import curses
import time

def main():
    # live cell coordinates are stored in this defaultdict, dead ones are not
    live_cells = Life(
        {
            (3, 3): 1
        }
    )

    game = render_grid(live_cells, (6, 6))
    
    print(game)
    return game

def render_grid(live_cells, size):
    grid = {}
    for x in range (0, size[0]):
        for y in range (0, size[1]):
            grid[(x, y)] = live_cells[(x, y)]
    
    return grid




class Life(dict):
    """Conway's Game of Life."""
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__(*args, **kwargs)

    # The value of any unrecorded (dead) cells is automatically set to 0 if requested
    def __missing__(self, *args):
        return 0

if __name__ == "__main__":
    # curses.wrapper(main)
    main()