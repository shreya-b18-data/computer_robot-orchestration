"""Tabular Q-learning for a single robot on a 2D grid.

Grid convention matches astar.py: 0 = free cell, 1 = obstacle.
Cells are (row, col) tuples. State = the robot's cell; the goal is fixed per agent.
"""
import random

ACTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # down, up, right, left


class QLearningAgent:
    def __init__(self, grid, goal, alpha=0.1, gamma=0.95, epsilon=0.2, seed=0):
        self.grid = grid
        self.goal = goal
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = random.Random(seed)
        self.q = {}

    def _q(self, state):
        return self.q.setdefault(state, [0.0] * len(ACTIONS))

    def step(self, state, action_idx):
        """Apply an action. Returns (next_state, reward, done)."""
        dr, dc = ACTIONS[action_idx]
        nr, nc = state[0] + dr, state[1] + dc
        rows, cols = len(self.grid), len(self.grid[0])
        if not (0 <= nr < rows and 0 <= nc < cols) or self.grid[nr][nc] == 1:
            return state, -5.0, False  # bumped into a wall/obstacle: stay put
        nxt = (nr, nc)
        if nxt == self.goal:
            return nxt, 100.0, True
        return nxt, -1.0, False

    def choose_action(self, state, explore=True):
        if explore and self.rng.random() < self.epsilon:
            return self.rng.randrange(len(ACTIONS))
        values = self._q(state)
        best = max(values)
        return self.rng.choice([i for i, v in enumerate(values) if v == best])

    def train(self, start, episodes=500, max_steps=200):
        """Train from `start`. Returns the number of steps taken in each episode."""
        steps_per_episode = []
        for _ in range(episodes):
            state = start
            for t in range(max_steps):
                a = self.choose_action(state)
                nxt, reward, done = self.step(state, a)
                target = reward if done else reward + self.gamma * max(self._q(nxt))
                self._q(state)[a] += self.alpha * (target - self._q(state)[a])
                state = nxt
                if done:
                    break
            steps_per_episode.append(t + 1)
        return steps_per_episode

    def greedy_path(self, start, max_steps=200):
        """Follow the learned policy without exploring. None if the goal isn't reached."""
        path = [start]
        state = start
        for _ in range(max_steps):
            a = self.choose_action(state, explore=False)
            state, _, done = self.step(state, a)
            path.append(state)
            if done:
                return path
        return None
