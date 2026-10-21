"""A* pathfinding on a 2D grid (4-connected).

Grid convention: 0 = free cell, 1 = obstacle. Cells are (row, col) tuples.
"""
import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(grid, cell):
    rows, cols = len(grid), len(grid[0])
    r, c = cell
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            yield (nr, nc)


def astar(grid, start, goal):
    """Return the shortest path as a list of cells, or None if unreachable."""
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return None

    open_heap = [(manhattan(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_heap:
        _, g, current = heapq.heappop(open_heap)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        if g > g_score.get(current, float("inf")):
            continue  # stale heap entry
        for nxt in neighbors(grid, current):
            new_g = g + 1
            if new_g < g_score.get(nxt, float("inf")):
                g_score[nxt] = new_g
                came_from[nxt] = current
                heapq.heappush(open_heap, (new_g + manhattan(nxt, goal), new_g, nxt))
    return None