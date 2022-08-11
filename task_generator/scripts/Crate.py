#%%
import numpy as np

class Crate:
    def __init__(self, start_location: np.ndarray, end_goal: np.ndarray, index: int):
        self.current_location = start_location
        self.goal = end_goal
        self.index = index
        self.delivered = False

    def __repr__(self):
        return f'Crate index: {self.index}\n\tcurrent location: {self.current_location} | goal: {self.goal} | delivered: {self.delivered}'

    def __call__(self):
        return self.start_location, self.goal, self.index

    def __eq__(self, other):
        if not isinstance(other, Crate):
            return False
        else:
            return other.index == self.index \
                and other.current_location == self.current_location \
                    and other.goal == self.goal

    def move(self, new_location):
        self.current_location = new_location

class CrateStack:
    
    
    def __init__(self, name):
        self.name = name
        self.index = 0
        self.list = []
        self._crate_map = {} # maps current_coords to crate object

    def __repr__(self):
        return f'Crate Stack "{self.name}"\n\tActive Crates: {len(self.list)}'
    
    def __iter__(self):
        return iter(self.list)

    def __bool__(self):
        return bool(self.list)
    __nonzero__ = __bool__ # python2 backwards compatibility cause we can
    
    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        return self.list[index]

    def _crate_locations_sanity_check(self):
        locs_from_list = [crate.current_location for crate in self.list]
        locs_from_map = [np.frombuffer(key, dtype= int) for key in self._crate_map]
        assert (np.sort(locs_from_list) == np.sort(locs_from_map)).all()

    def get_crate_locations(self, sanity_check=True):
        if sanity_check:
            self._crate_locations_sanity_check()
        return [crate.current_location for crate in self.list]

    def isempty(self):
        return not self.__bool__()

    def append(self, start_location: np.ndarray, end_goal: np.ndarray):
        if start_location.tobytes() in self._crate_map:
            raise ValueError('Can\'t spawn crates on top of eachother')
        crate = Crate(start_location, end_goal, self.index)
        self.list.append(crate)
        self._crate_map[start_location.tobytes()] = crate
        self.index += 1

    def remove(self, location: np.ndarray):
        crate = self._crate_map.pop(location.tobytes())
        self.list.remove(crate)

    def move_crate(self, old_location: np.ndarray, new_location: np.ndarray):
        if new_location.tobytes() in self._crate_map:
            print(f'Can\'t move crate to {new_location} because there already is one there.')
            return False
        else:
            crate = self._crate_map.pop(old_location.tobytes()) # np.ndarray.tobytes() makes array hashable
            self._crate_map[new_location.tobytes()] = crate # update map
            crate.move(new_location) # update crate object
            return True

    def get_crate_at_location(self, location: np.ndarray):
        crate = self._crate_map.get(location.tobytes(), None)
        if crate is None:
            print(f'No crate found at location {location}')
        return crate




# %%
if __name__ == '__main__':
    cs = CrateStack('One')
    crate_1 = cs.spawn_crate(np.array([0,0]), np.array([1,1]))
    cs.list
    # %%
    cs.despawn_crate(crate_1)
    cs.list

# %%
