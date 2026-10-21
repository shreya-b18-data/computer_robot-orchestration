from src.astar import astar


def test_straight_path():
    grid = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    path = astar(grid, (0, 0), (0, 2))
    assert path == [(0, 0), (0, 1), (0, 2)]


def test_path_around_obstacle():
    grid = [[0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]]
    path = astar(grid, (0, 0), (0, 2))
    assert path is not None
    assert len(path) == 7  # must go down, across, and back up
    assert path[0] == (0, 0) and path[-1] == (0, 2)


def test_no_path():
    grid = [[0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]]
    assert astar(grid, (0, 0), (0, 2)) is None


def test_start_equals_goal():
    grid = [[0]]
    assert astar(grid, (0, 0), (0, 0)) == [(0, 0)]


def test_blocked_goal():
    grid = [[0, 1]]
    assert astar(grid, (0, 0), (0, 1)) is None