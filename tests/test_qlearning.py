from src.astar import astar
from src.qlearning import QLearningAgent

GRID = [[0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]]


def test_learns_to_reach_goal():
    agent = QLearningAgent(GRID, goal=(2, 3), seed=1)
    agent.train((0, 0), episodes=1000)
    path = agent.greedy_path((0, 0))
    assert path is not None and path[-1] == (2, 3)


def test_training_reduces_steps():
    agent = QLearningAgent(GRID, goal=(2, 3), seed=1)
    steps = agent.train((0, 0), episodes=1000)
    assert sum(steps[-50:]) < sum(steps[:50])


def test_learned_path_matches_astar_length():
    agent = QLearningAgent(GRID, goal=(2, 3), seed=1)
    agent.train((0, 0), episodes=1000)
    path = agent.greedy_path((0, 0))
    assert len(path) == len(astar(GRID, (0, 0), (2, 3)))


def test_bump_keeps_robot_in_place():
    agent = QLearningAgent(GRID, goal=(2, 3))
    state, reward, done = agent.step((0, 0), 1)  # up, out of bounds
    assert state == (0, 0) and reward < 0 and not done