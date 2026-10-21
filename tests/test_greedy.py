from src.greedy import greedy_path


def test_open_grid_reaches_goal():
    grid = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    path = greedy_path(grid, (0, 0), (2, 2))
    assert path[0] == (0, 0) and path[-1] == (2, 2)
    assert len(path) == 5  # shortest possible on an open grid


def test_start_equals_goal():
    assert greedy_path([[0]], (0, 0), (0, 0)) == [(0, 0)]


def test_gets_stuck_behind_wall():
    # Greedy keeps pushing toward the goal and oscillates at the wall; A* would find the way.
    grid = [[0, 0, 0],
            [1, 1, 0],
            [0, 0, 0]]
    assert greedy_path(grid, (2, 0), (0, 0)) is None