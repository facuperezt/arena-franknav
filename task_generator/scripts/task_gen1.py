#%%
import numpy as np
from Grid import *
from matplotlib import pyplot as plt
from Crate import CrateStack


class TaskManager():
    def __init__(self, g: Grid, name: str = 'default'):
        self.g = g
        self.active_crates = CrateStack(name)
        self.nr_active_crates = 0 # obsolete
        self.nr_transit_crates = 0 # obsolete

    ## MANAGE QUADRANTS ##
    def _get_random_quadrant_of_type(self, quadrant_type, random=True):
        grid_inds = self._find(quadrant_type)
        if grid_inds.shape[0] <= 0:
            return np.array([])
        ind = np.random.randint(0, grid_inds.shape[0])
        return grid_inds[ind, :]

    def _get_quadrant_type(self, coords):
        return self.g.grid[coords[0], coords[1]]

    def _free_quadrant(self, coords, remove_crate= False):
        if remove_crate:
            self.active_crates.remove(coords)
        quadrant_type = self._get_quadrant_type(coords)
        self.g.grid[coords[0], coords[1]] = FREE_GOAL if quadrant_type == OCCUPIED_GOAL else FREE_SHELF

    def _occupy_quadrant(self, coords, goal= None, spawn_crate= False):
        if spawn_crate:
            self.active_crates.add(coords, goal)
        quadrant_type = self._get_quadrant_type(coords)
        self.g.grid[coords[0], coords[1]] = OCCUPIED_GOAL if quadrant_type == FREE_GOAL else OCCUPIED_SHELF

    def _find(self, quadrant_type):
        return np.argwhere(self.g.grid == quadrant_type)

    ## MOVE CRATES ##
    def _can_spawn_crate(self):
        return self._find(FREE_GOAL).size > 0 # True if there is a FREE_GOAL, False otherwise

    def _spawn_crates(self, nr_crates= 1, goals= None):
        grid_inds = self._find(FREE_GOAL)[:nr_crates,:] # Find free goals and restrict to however many crates we want to spawn
        if nr_crates > grid_inds.shape[0]:
            print(f"Can't spawn {nr_crates} because there are only {grid_inds.shape[0]} free Goals. Spawning {grid_inds.shape[0]} crates instead.")
            nr_crates = grid_inds.shape[0]
        
        if goals is None:
            goals = [self._get_random_quadrant_of_type(FREE_SHELF)]

        for start_coords, goal in zip(grid_inds, goals):
            self._occupy_quadrant(start_coords, goal, spawn_crate= True)


    def _pickup_crate(self, coords):
        assert self.nr_active_crates > 0, 'No active crates to pick up'
        quadrant_type = self._get_quadrant_type(coords)
        assert quadrant_type in [OCCUPIED_GOAL, OCCUPIED_SHELF], 'Quadrant must be occupied.'
        self._free_quadrant(coords)
        
        self.nr_transit_crates += 1

    def _set_crate(self, coords):
        assert self.nr_transit_crates > 0, 'No transit crates to set'
        quadrant_type = self._get_quadrant_type(coords)
        assert quadrant_type in [FREE_GOAL, FREE_SHELF], 'Can only set down crates in Goal or Shelf quadrant'
        self._occupy_quadrant(coords)

        self.nr_transit_crates -= 1
        if quadrant_type == FREE_GOAL:
            self.nr_active_crates -= 1

    ## BRAIN ##
    def _get_goal(self, quadrant_type):
        return self._get_random_quadrant_of_type(quadrant_type)


    ## EDGE CASE WRAPPERS ##
    def _generate_pack_task(self, goal= None):
        if not self._can_spawn_crate():
            print('No free goals to spawn crate in')

        else:
            self._spawn_crates(1, goal)


    def _generate_unpack_task(self):
        if self.active_crates.isempty():
            print('No stashed crates to unpack.')

        else:
            crate_location = self._get_random_quadrant_of_type(OCCUPIED_SHELF)
            goal = self._get_random_quadrant_of_type(FREE_GOAL)
            if not goal.size > 0:
                print('No free goals')
            else:
                crate = self.active_crates.get_crate_at_location(crate_location)
                crate.goal = goal

            
            

    ## PUBLIC FUNCTIONS ## 
    def generate_new_task(self, type):
        if type not in ['pack', 'unpack']:
            return ValueError('Assignment not implemented')
        if type == 'pack':
            return self._generate_pack_task()            
        if type == 'unpack':
            return self._generate_unpack_task()

    def move_from_to(self, current_location: np.ndarray, new_location: np.ndarray, remove_crate= False):
        self.active_crates.move_crate((current_location), new_location)
        self._free_quadrant(current_location)
        self._occupy_quadrant(new_location)
        if remove_crate:
            self._free_quadrant(new_location, remove_crate= True)
        



grid = np.load('wh1.npy')
g = Grid()
g.grid = grid

tm = TaskManager(g)
plt.imshow(g.grid)
tm.nr_active_crates
#%%
tm.generate_new_task('pack')
plt.imshow(g.grid)
tm.active_crates[0]
#%%
tm.move_from_to(tm.active_crates[0].current_location, tm.active_crates[0].goal)
plt.imshow(g.grid)
#%%
tm.generate_new_task('unpack')
plt.imshow(g.grid)
tm.active_crates.list
#%%
tm.move_from_to(tm.active_crates[0].current_location, tm.active_crates[0].goal, remove_crate= True)
plt.imshow(g.grid)
#%%
plt.imshow(g.grid)
tm.active_crates

