# Architecture Notes

## Current implementation

The supplied prototype is a single HTML document containing:

- CSS for the dark dashboard, controls, grid, status cards, and logs.
- JavaScript state for the environment, robots, tasks, obstacles, and communication counters.
- An `Orchestrator` class for merging robot Q-table entries and dispatching tasks.
- A `Robot` class with Q-value lookup, action selection, and Q-learning updates.
- A* pathfinding.
- PC-zone synchronization and peer-to-peer Q-table sharing.
- Simulation stepping, rendering, status updates, and UI controls.

## Communication channels

### PC ↔ Robot

Robots inside the configured PC radius can upload selected Q-table entries. The orchestrator blends received values into its master table and sends selected values back to robots. Task assignments are also represented as PC-to-robot commands.

### Robot ↔ Robot

Robots within the configured peer radius can exchange selected Q-table entries in both directions. Sharing can be triggered after a task completion or periodically.

## Navigation and learning

- **A\*:** searches the grid for a path while avoiding obstacle cells.
- **Q-learning:** updates action values using a reward, learning rate, discount factor, and estimated next-state value.
- **Exploration:** epsilon controls the action-selection exploration behavior.
- **Battery behavior:** robots can return to the base when energy is low.

## Limitations and validation

This prototype is a visualization/simulation, not a validated multi-robot deployment stack. Before real-world use, test collision handling, unreachable tasks, battery edge cases, task allocation fairness, communication loss, and safety stops. Real hardware integration requires actual communication, localization, motor control, and sensor interfaces.
