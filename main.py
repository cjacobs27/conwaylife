import curses
import time

# TODO: tests!
def main(stdscr):
    # Intro screen
    # TODO: Add input for grid size here
    stdscr.clear()
    # NOTE: curses co-ordinates are Y, X!
    stdscr.addstr(8, 12, "Conway's Game of Life")
    stdscr.addstr(10, 10, "Hit ENTER to start, Q to exit, WASD to move")
    # Dev only:
    stdscr.addstr(12, 8, f"Window size: X: {curses.COLS}, Y: {curses.LINES}")

    
    keypress = stdscr.getch()

    if keypress == ord('\n'):
        stdscr.clear()

        ### Initialize game ###

        # live cell coordinates are stored in this defaultdict, dead ones are not
        # TODO: make these user inputtable to adjust board size?
        max_y, max_x = stdscr.getmaxyx()

        # TODO: make relative to board size/in central position using max x and y
        live_cells = Life(
            {
                (45, 5): 1,
                (46, 5): 1,
                (45, 6): 1,
                (44, 6): 1,
                (45, 7): 1,
            }
        )

        # The starting coordinates for the viewport position
        adjust_x, adjust_y = 0, 0
        stdscr.nodelay(True)
        
        while True:
            # TODO: this viewport moving code won't be useful once the board is restricted
            # in size, so this can be modified into a cursor for the user to draw
            # starting shapes in a later version.
            # move = stdscr.getch()
            # if move == ord("a"):
            #     adjust_x += -1
            # elif move == ord("d"):
            #     adjust_x += 1
            # elif move == ord("s"):
            #     adjust_y += -1
            # elif move == ord("w"):
            #     adjust_y += 1
            # elif move == ord("q"):
            #     exit(0)
            # else:
            #     pass

            move = stdscr.getch()
            if move == ord("q"):
                exit(0)

            stdscr.clear()

            ### Draw border ###
            # TODO: separate method

            y_border_coords = {}
            x_border_coords = {}
            for i in range(0,max_x):
                # curses coords are Y, X
                x_border_coords[(0,i)] = '--'
                x_border_coords[(max_y-1, i)] = '--'

            for i in range(0,max_y):
                y_border_coords[(i, 0)] = '!'
                y_border_coords[(i, max_x - 1)] = '!'

            border_coords = x_border_coords | y_border_coords
            print(f'border_coords: {border_coords}')
            for coords in border_coords.keys():
                try:   
                    stdscr.addstr(coords[0], coords[1], border_coords.get(coords))
                except curses.error as ex:
                    pass
            ###################


            # TODO: store border on the Life obj to avoid passing in here
            live_cells.play_game(border_coords)
            
            for x, y in live_cells.keys():
                # 'adjust' vars are to do with viewport moving code above
                visible_x = (0 + adjust_x) < x < (max_x + adjust_x)
                visible_y = (0 + adjust_y) < y < (max_y + adjust_y)
                if visible_x and visible_y:
                    # The try/except here catches an error from printing
                    # at the bottom right corner.
                    try:
                        stdscr.addstr(y - adjust_y, x - adjust_x, '██')
                    except curses.error:
                        pass
            curses.curs_set(0)    
            stdscr.refresh()
            time.sleep(0.2)

    elif keypress == ord("q"):
        stdscr.clear()
        exit(0)
    #####

    return

# TODO: move to another file?
class Life(dict):
    """Conway's Game of Life."""
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__(*args, **kwargs)

    # The value of any unrecorded (dead) cells is automatically set to 0 if requested
    def __missing__(self, *args):
        return 0

    def find_cells_to_check(self):
        """Build a list of all cells that need to be status-checked this generation."""
        cells = []
        for x, y in self.keys():
            # The X and Y next door neighbours of each LIVE cell
            x_coords = (x-1, x, x+1)
            y_coords = (y-1, y, y+1)
            for x_coord in x_coords:
                for y_coord in y_coords:
                    cells.append((x_coord, y_coord))
        return cells

    def check_cell_liveness(self, x: int, y: int):
        """Generation step for a cell. Determine if it lives or dies."""
        x_coords = (x-1, x, x+1)
        y_coords = (y-1, y, y+1)
        total = 0

        for x_coord in x_coords:
            for y_coord in y_coords:
                total += self[x_coord, y_coord]

        live, dead = [], []

        # 'self' is the list of dict entries representing cells that have been
        # identified as needing to be checked by the find_cells_to_check method:
        cell = self[x, y]
        if total == 3 and not cell:
            # Dead cell (cell value is 0) with three neighbors becomes alive.
            live.append((x, y))
        elif total < 3 or total > 4 and cell:
            # Live cell with too many or too few neigbours dies.
            dead.append((x, y))
        elif cell:
            # Cell has right number of neighbours, it continues to live.
            pass
        return live, dead
    
    def play_game(self, border_coords):
        """Play one generation in Life."""
        live, dead = [], []

        for x, y in self.find_cells_to_check():
            step_live, step_dead = self.check_cell_liveness(x, y)
            live += step_live
            dead += step_dead
        # Apply all changes.
        for x, y in dead:
            if self[x, y]:
                # We can delete rather than just change value to 0,
                # thanks to the __missing__ method on Life()
                del self[x, y]
        for x, y in live:
            if (y, x) not in border_coords:
                self[x, y] = 1


if __name__ == "__main__":
    curses.wrapper(main)
