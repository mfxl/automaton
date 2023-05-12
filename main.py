import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import rule_book
np.set_printoptions(threshold=sys.maxsize)

def apply_rule(rule: dict, grid: np.ndarray, steps=40) -> np.ndarray:
    """
    Executes the automaton for a given rule
    :param rule: dict, dictionary containing the rule for the automaton
    :param grid: np.ndarray, initial grid on which the automaton runs
    :param steps: int, number of evolutionary steps > 0
    :return grid: np.ndarray, final grid containing all states
    """
    _dim = grid.shape[0] - 1

    if rule["scan"] == 3:
        _start_column, _end_column, up_search, down_search = 1, _dim, 1, 1
    elif rule["scan"] == 5:
        _start_column, _end_column, up_search, down_search = 2, _dim - 1, 2, 2
    else:
        raise()

    # Set genesis state
    genesis_col = int(_dim * rule["genesis"])
    grid[0, genesis_col] = 1

    if rule["type"] == "state":  # takes the original state of the scanned cells
        for r in np.arange(1, steps + 1):
            for c in range(_start_column, _end_column):
                scanned_states = grid[r - 1, c - down_search: c + up_search + 1]
                grid[r, c] = rule[str(scanned_states)]
    elif rule["type"] == "avg": # calculates the avg state of the scanned cells
        for r in np.arange(1, steps + 1):
            for c in range(_start_column, _end_column):
                scanned_states = grid[r - 1, c - down_search: c + up_search + 1]
                grid[r, c] = rule[round(scanned_states.mean(), 1)]

    return grid

class Grid():

    def __init__(self, dim=100, grid=np.array(0), grid_name=None):
        self._grid = grid
        self._dim = dim
        self.grid_name = grid_name

    def init_grid(self):
        self._grid = np.array(np.zeros([self._dim + 1, self._dim + 1]))

    def visualize(self):
        fig = plt.figure(figsize=(32, 32))
        im = plt.imshow(self._grid, interpolation='none', cmap="Greys")
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.title(self.grid_name, loc='right')
        if 0.03 <= self.density <= 0.9:  #and 0.02 <= self.std_col:
            path = ""
            file_name = self.grid_name.lower().replace(" ", "_").replace("(", "").replace(")", "")
            fig.savefig(f"data/{path}{file_name}.png", dpi=fig.dpi)
        #plt.show()

    @property
    def density(self):
        area = self._grid.shape[0] ** 2
        info = sum(sum(self._grid))
        return round(info / area, 2)

    @property
    def std_col(self):
        """
        The column standard deviation
        :return:
        """
        v = np.std(np.std(self._grid[1:, 1:-1], axis=0))
        return round(v, 2)

    def get_grid(self):
        return self._grid

if __name__ == '__main__':
    rule = rule_book.code1635_7bits
    g = Grid(dim=1000, grid_name=rule["title"])  # Create grid instance
    g.init_grid()  # Initialize a plain grid
    grid = apply_rule(rule=rule, grid=g.get_grid(), steps=1000)
    g.visualize()
    0