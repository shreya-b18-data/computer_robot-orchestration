"""Greedy baseline: always step to the free neighbour closest to the goal.

Grid convention matches astar.py: 0 = free cell, 1 = obstacle; cells are (row, col).
Unlike A*, it has no memory or lookahead, so it can get stuck behind obstacles.
"""
from src.astar import manhattan, neighbors


def greedy_path(grid, start, goal, max_steps=200):
    """Return the path taken, or None if the goal isn't reached within max_steps."""
    path = [start]
    current = start
    for _ in range(max_steps):
        if current == goal:
            return path
        options = list(neighbors(grid, current))
        if not options:
            return None
        current = min(options, key=lambda cell: manhattan(cell, goal))
        path.append(current)
    return path if current == goal else None