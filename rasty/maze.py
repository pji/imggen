"""
maze
~~~~~~

Image data sources that create maze-like paths.
"""
from operator import itemgetter
from typing import Sequence

import numpy as np

from rasty import unitnoise as un
from rasty.rasty import X, Y, Z


# Public classes.
class Maze(un.UnitNoise):
    """A class to generate maze-like paths.

    :param unit: The number of pixels between vertices along an
        axis. The vertices are the locations where colors for
        the gradient are set.
    :param width: (Optional.) The width of the path. This is the
        percentage of the width of the X axis length of the size
        of the fill. Values over one will probably be weird, but
        not in a great way.
    :param inset: (Optional.) Sets how many units from the end of
        the image to draw the path. Units here refers to the unit
        parameter from the UnitNoise parent class.
    :param origin: (Optional.) Where in the grid to start the path.
        This can be either a descriptive string or a three-dimensional
        coordinate. It defaults to the top-left corner of the first
        three-dimensional slice of the data.
    :param min: (Optional.) The minimum value of a vertex of the unit
        grid. This is involved in setting the path through the maze.
    :param max: (Optional.) The maximum value of a vertex of the unit
        grid. This is involved in setting the path through the maze.
    :param repeats: (Optional.) The number of times each value can
        appear on the unit grid. This is involved in setting the 
        maximum size of noise that can be generated from the object.
    :param seed: (Optional.) An int, bytes, or string used to seed
        therandom number generator used to generate the image data.
        If no value is passed, the RNG will not be seeded, so
        serialized versions of this source will not product the
        same values. Note: strings that are passed to seed will
        be converted to UTF-8 bytes before being converted to
        integers for seeding.
    :return: :class:Maze object.
    :rtype: rasty.Maze

    Descriptive Origins
    -------------------
    The origin parameter can accept a description of the location
    instead of direct coordinates. This string must either be two
    words delimited by a hyphen or two letters. The first position
    sets the Y axis location can be one of the following options:

    *   top | t
    *   middle | m
    *   bottom | b

    The second position sets the X axis position and can be one of
    the following options:

    *   left | l
    *   middle | m
    *   bottom | b
    """
    def __init__(self, unit: Sequence[int], 
                 width: float = .2,
                 inset: Sequence[int] = (0, 1, 1),
                 origin: Sequence[int] = (0, 0, 0),
                 min: int = 0x00,
                 max: int = 0xff,
                 repeats: int = 1,
                 seed: un.Seed = None) -> None:
        """Initialize an instance of Maze."""
        super().__init__(unit, min, max, repeats, seed)
        self.width = width
        self.inset = inset
        self.origin = origin

    # Public methods.
    def fill(self, size: Sequence[int],
             loc: Sequence[int] = (0, 0, 0)) -> np.ndarray:
        """Fill a space with image data."""
        values, unit_dim = self._build_grid(size, loc)
        path = self._build_path(values, unit_dim)
        return self._draw_path(path, size)

    # Private methods.
    def _build_grid(self, size, loc):
        """Create a grid of values. This uses the same technique
        Perlin noise uses to add randomness to the noise. A table of
        values was shuffled, and we use the coordinate of each vertex
        within the grid as part of the process to lookup the table
        value for that vertex. This grid will be used to determine the
        route the path follows through the space.
        """
        unit_dim = [int(s / u) for s, u in zip(size, self.unit)]
        unit_dim = tuple(np.array(unit_dim) + np.array((0, 1, 1)))
        unit_dim = tuple(np.array(unit_dim) - np.array(self.inset) * 2)
        unit_indices = np.indices(unit_dim)
        for axis in X, Y:
            unit_indices[axis] += loc[axis]
        unit_indices[Z].fill(loc[Z])
        values = np.take(self._table, unit_indices[X])
        values += unit_indices[Y]
        values = np.take(self._table, values % len(self._table))
        values += unit_indices[Z]
        values = np.take(self._table, values & len(self._table))
        unit_dim = np.array(unit_dim)
        return values, unit_dim

    def _build_path(self, values: np.ndarray,
                    unit_dim: Sequence[int]) -> np.ndarray:
        """Create the steps in the path."""
        # The cursor will be used to determine our current position
        # on the grid as we create the path.
        cursor = self._calc_origin(self.origin, unit_dim)

        # This will be used to track the grid vertices we've already
        # been to as we create the path. It allows us to keep the
        # path from looping back into itself.
        been_there = np.zeros(unit_dim, bool)
        been_there[tuple(cursor)] = True

        # These are the positions of the vertices the cursor could
        # move to next as it creates the path.
        vertices = np.array([
            (0, 0, -1),
            (0, 0, 1),
            (0, -1, 0),
            (0, 1, 0),
        ])

        # The index tracks where we are along the path. This is used
        # to allow us to go back up the path and create a new branch
        # if we run into a dead end while creating the path. It also
        # is how we know we're done when creating the path.
        index = 0

        # Create the path.
        path = []
        while True:

            # Look at the options available for the direction the path
            # can take. Some of them won't be viable because they are
            # outside the bounds of the image or have already been
            # hit.
            cursor = np.array(cursor)
            options = [vertex + cursor for vertex in vertices]
            viable = [(o, values[tuple(o)]) for o in options
                      if self._is_viable_option(o, unit_dim, been_there)]

            # If there is a viable next step, take that step.
            if viable:
                cursor = tuple(cursor)
                viable = sorted(viable, key=itemgetter(1))
                newloc = tuple(viable[0][0])
                path.append((cursor, newloc))
                been_there[newloc] = True
                cursor = newloc
                index = len(path)

            # If there is not a viable next step, go back to the last
            # place you were, so to see if there are any viable steps
            # there. If this goes all the way back to the beginning
            # of the path and there are no viable paths, then the
            # path is complete.
            else:
                index -= 1
                if index < 0:
                    break
                cursor = path[index][0]

        return path

    def _calc_origin(self, origin, unit_dim):
        "Determine the starting location of the cursor."
        # If origin isn't a string, no further calculation is needed.
        if not isinstance(origin, str):
            return origin

        # Coordinates serialized as strings should be comma delimited.
        if ',' in origin:
            return c.text_to_int(origin)

        # If it's neither of the above, it's a descriptive string.
        result = [0, 0, 0]
        if '-' in origin:
            origin = origin.split('-')

        # Allow middle to be a shortcut for middle-middle.
        if origin == 'middle' or origin == 'm':
            origin = 'mm'

        # Set the Y axis coordinate.
        if origin[0] in ('top', 't'):
            result[Y] = 0
        if origin[0] in ('middle', 'm'):
            result[Y] = unit_dim[Y] // 2
        if origin[0] in ('bottom', 'b'):
            result[Y] = unit_dim[Y] - 1

        # Set the X axis coordinate.
        if origin[1] in ('left', 'l'):
            result[X] = 0
        if origin[1] in ('middle', 'm'):
            result[X] = unit_dim[X] // 2
        if origin[1] in ('right', 'r'):
            result[X] = unit_dim[X] - 1

        return result

    def _draw_path(self, path, size):
        """Turn the unit grid array into an array of image data."""
        a = np.zeros(size, dtype=float)
        width = int(self.unit[-1] * self.width)
        for step in path:
            start = self._unit_to_pixel(step[0])
            end = self._unit_to_pixel(step[1])
            slice_y = self._get_slice(start[Y], end[Y], width)
            slice_x = self._get_slice(start[X], end[X], width)
            a[:, slice_y, slice_x] = 1.0
        return a

    def _get_slice(self, start, end, width):
        """Get a slice of the array of image data of the given width."""
        if start > end:
            start, end = end, start
        start -= width
        end += width
        return slice(start, end)

    def _is_viable_option(self, option, unit_dim, been_there):
        loc = tuple(option)
        if (np.min(option) >= 0
                and all(unit_dim > option)
                and not been_there[loc]):
            return True
        return False

    def _unit_to_pixel(self, unit_loc: Sequence[int]) -> Sequence[int]:
        """Convert an index of the unit grid array into an index
        of the image data.
        """
        unit = np.array(self.unit)
        pixel_loc = np.array(unit_loc) * unit
        pixel_loc += np.array(self.inset) * unit
        return tuple(pixel_loc)


if __name__ == '__main__':
    import rasty.utility as u
    kwargs = {
        'width': .34,
        'inset': (0, 1, 1),
        'unit': (1, 3, 3),
        'seed': 'spam',
    }
    cls = Maze
    size = (2, 10, 10)
    obj = cls(**kwargs)
    a = obj.fill(size)
    u.print_array(a, 2)
