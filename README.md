# Dual-Channel Computer–Robot Orchestration Simulation

A browser-based simulation concept for coordinating robots through two communication channels:

- **PC ↔ Robot:** a central orchestrator exchanges task commands and Q-table information with robots near the PC upload zone.
- **Robot ↔ Robot:** nearby robots share learned Q-values with peers, including after completing tasks and during periodic communication rounds.

The supplied prototype is a single HTML file with embedded CSS and JavaScript. This repository starter keeps that original prototype intact and adds project documentation and setup files. The modular `js/` files mentioned in the planned architecture are not created here because the supplied source has not yet been refactored into separate modules.

## Features represented in the prototype

- Configurable grid size, robot count, tasks, obstacles, exploration rate, and simulation speed.
- A* path planning on a grid.
- Q-learning updates for robot actions.
- Central orchestration and task dispatch.
- PC-to-robot synchronization and robot-to-robot Q-table sharing.
- Battery tracking and return-to-base behavior.
- Wi-Fi, tether, and BLE mode labels in the simulation UI.
- Mission counters, activity log, and Q-table export control.

> **Important:** This is a browser simulation. The communication modes are represented in the UI and simulation logic; they do not by themselves establish a real Wi-Fi, BLE, MQTT, or ROS 2 connection to physical robots.

## Getting started

1. Keep the supplied HTML file as `index.html` in the project root.
2. Open `index.html` in a modern browser.
3. Use **Initialize** to start the simulation.
4. Adjust the sliders and communication mode to explore different configurations.
5. Use **Reset Env** to rebuild the environment.

No package installation is required for the current single-file prototype.

## Project structure

```text
computer-robot-orchestration/
├── index.html                 # Original browser simulation (add supplied HTML here)
├── README.md
├── requirements.txt
├── package.json
├── .gitignore
├── LICENSE
└── docs/
    └── ARCHITECTURE.md
```

## Configuration

The interface exposes settings for grid size, robot count, number of tasks, obstacle count, epsilon exploration, speed, PC upload radius, peer-sharing radius, synchronization interval, and communication mode.

## Future improvements

- Refactor the embedded CSS and JavaScript into separate files.
- Add automated tests for path planning, task allocation, and Q-table synchronization.
- Add reproducible random seeds and benchmark scenarios.
- Implement real robot transport adapters (for example, MQTT or ROS 2) separately from the browser simulation.
- Document measured performance and known limitations.

## License

See `LICENSE`.
