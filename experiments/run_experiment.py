"""Compare greedy vs Q-learning (with A* as the optimal reference) on random grids.

Usage (from the project root):
    python experiments/run_experiment.py
    python experiments/run_experiment.py --trials 100 --size 8 --density 0.2 --episodes 500

Writes one row per trial to results/results.csv.
"""
import argparse
import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.astar import astar  # noqa: E402
from src.greedy import greedy_path  # noqa: E402
from src.qlearning import QLearningAgent  # noqa: E402


def random_grid(size, density, rng):
    """Random obstacle grid whose start (0,0) and goal (size-1,size-1) are connected."""
    start, goal = (0, 0), (size - 1, size - 1)
    while True:
        grid = [[1 if rng.random() < density else 0 for _ in range(size)] for _ in range(size)]
        grid[start[0]][start[1]] = 0
        grid[goal[0]][goal[1]] = 0
        if astar(grid, start, goal) is not None:
            return grid, start, goal


def steps(path):
    return None if path is None else len(path) - 1


def run(trials, size, density, episodes, seed):
    rows = []
    for trial in range(trials):
        rng = random.Random(seed + trial)
        grid, start, goal = random_grid(size, density, rng)
        optimal = steps(astar(grid, start, goal))
        greedy = steps(greedy_path(grid, start, goal))
        agent = QLearningAgent(grid, goal, seed=seed + trial)
        agent.train(start, episodes=episodes)
        q = steps(agent.greedy_path(start))
        rows.append({
            "trial": trial,
            "optimal_steps": optimal,
            "greedy_steps": greedy,
            "greedy_success": int(greedy is not None),
            "q_steps": q,
            "q_success": int(q is not None),
        })
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trials", type=int, default=100)
    p.add_argument("--size", type=int, default=8)
    p.add_argument("--density", type=float, default=0.25)
    p.add_argument("--episodes", type=int, default=500)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    rows = run(args.trials, args.size, args.density, args.episodes, args.seed)
    out = ROOT / "results" / "results.csv"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    n = len(rows)
    print(f"{n} trials -> {out}")
    print(f"greedy success: {sum(r['greedy_success'] for r in rows) / n:.0%}")
    print(f"q-learning success: {sum(r['q_success'] for r in rows) / n:.0%}")


if __name__ == "__main__":
    main()