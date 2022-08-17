#%%
import numpy as np
import numpy.ma as ma
from Grid import *
import matplotlib.pyplot as plt

# configs

import numpy as np
pixels_per_meter = 100
resolution = 1/pixels_per_meter
grid_cell_size = 1 # in meters
min_shelf_separation = 2 # in meters
clearing_for_goal = 4
shelf_size = 1
possible_layouts = ['horizontal', 'vertical']
possible_separations = ['max', 'center', 'near', 'far']


# hyper-parameters

size = (10, 10) # meters
size_pixels = tuple(a/resolution for a in size)
layout = 'vertical'  
nr_shelf_groups = 2
separation = 'center'
nr_goals = 5

# functions

def add_walls(grid):
    grid.has_walls = True
    grid.grid = np.pad(grid.grid, pad_width=((1,1), (1,1)), mode='constant', constant_values=WALL)
    
    return grid

def remove_walls(grid):
    grid.has_walls = False
    grid.grid = grid.grid[1:-1, 1:-1]

    return grid

def add_goals(grid):
    if layout == 'vertical':
        return _add_goals_vertical(grid)
    else:
        return NotImplementedError

def _add_goals_vertical(grid):
    row = -2 if grid.has_walls else -1

    m = grid.grid.shape[1]//2 # middle
    if grid.grid.shape[1] % 2 == 0:
        grid.grid[row, m-1:m+1] = FREE_GOAL
    else:
        grid.grid[row, m-1:m+2] = FREE_GOAL


    return grid

def add_shelves(grid):
    if layout == 'vertical':
        return _add_shelves_vertical(grid)
    else:
        return NotImplementedError

def _add_shelves_vertical(grid):
    if separation == 'center':
        return _add_shelves_vertical_center(grid)
    else:
        return NotImplementedError

def _add_shelves_vertical_center(grid):
    nr_rows = size[0] - clearing_for_goal # 3 meter clearing from wall
    row_min = 0 # start from other wall
    nr_cols = (nr_shelf_groups * shelf_size) + (nr_shelf_groups - 1)*min_shelf_separation
    col_min = (size[1] - nr_cols)//2

    if grid.has_walls:
        cols = np.arange(col_min+1, col_min + 1 + nr_cols + 1, 1 + min_shelf_separation)
        rows = slice(row_min+1, row_min + 1 + nr_rows + 1, 1)
    else:
        cols = np.arange(col_min, col_min + nr_cols + 1, 1 + min_shelf_separation)
        rows = slice(row_min, row_min + 1 + nr_rows, 1)

    m = grid.grid.shape[1]//2 # middle
    if grid.grid.shape[1] % 2 == 0:
        grid.grid[rows, tuple(cols)] = FREE_SHELF
    else:
        grid.grid[rows, tuple(cols)] = FREE_SHELF

    return grid

def upscale_grid(grid, n = pixels_per_meter):

    grid.grid = np.kron(grid.grid, np.ones((n,n)))

    return grid

# script

grid_size = np.array(size)/grid_cell_size
g = Grid()
g.grid = np.zeros(grid_size.astype(np.int32))

#g = add_walls(g)
g = add_goals(g)
g = add_shelves(g)


plt.imshow(g.grid)

np.save('wh1', g.grid)




# %%
plt.imshow(upscale_grid(g, 100))

# %%
