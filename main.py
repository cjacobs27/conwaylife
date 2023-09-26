import curses
import time

def main(stdscr):
    # Intro screen
    # TODO: Add input for grid size here
    stdscr.clear()
    stdscr.addstr(8, 12, "Conway's Game of Life")
    stdscr.addstr(10, 10, "Hit ENTER to start, Q to exit")
    keypress = stdscr.getch()

    if keypress == ord('\n'):
        stdscr.clear()
        # live cell coordinates are stored in this defaultdict, dead ones are not
        live_cells = Life(
            {
                (2, 3): 1,
                (3, 3): 1,
                (3, 4): 1
            }
        )

        grid = render_grid(live_cells, (10, 10))
        
        for key, value in grid.items():
            value = '░' if value == 0 else '■'
            stdscr.addstr(key[0], key[1], value)

        # stdscr.nodelay(True)
        # The starting coordinates for the viewport position
        adjust_x, adjust_y = 0, 0

        stdscr.refresh()
        stdscr.getch()
        
        return grid
    elif keypress == ord("q"):
        exit(0)
    #####

def render_grid(live_cells, size):
    grid = {}
    for x in range (1, size[0]):
        for y in range (1, size[1]):
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
    curses.wrapper(main)
    # main()