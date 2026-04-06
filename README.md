# Project Hail Mary Simulation
## CPS7004 – Artificial Intelligence – Assessment 1
**Student:** Prestha Khanal  
**Institution:** St Mary's University, Twickenham  
**Deadline:** 2nd June 2026

## Overview
A multi-agent AI simulation based on Andy Weir's Project Hail Mary.
Two intelligent agents — Dr. Ryland Grace and Rocky — cooperate to
save both their civilisations from extinction by Astrophage.

## How to Run

Install dependencies:
pip3.12 install matplotlib numpy --break-system-packages

Run the simulation:
python3.12 main.py

## Project Structure
hail-mary-simulation/
├── main.py
├── requirements.txt
├── results/
└── src/
    ├── environment.py
    ├── agents.py
    ├── experiments.py
    ├── simulation.py
    └── visualisation.py

## Key AI Features
- Q-Learning experiment strategy with epsilon-greedy Q-table
- Multi-agent cooperation between Grace and Rocky
- Xenonite tunnel travel between ships
- EVA mechanic with energy and health costs
- Astrophage resistance evolution
- Beetle probes John, Paul, George, Ringo
- Sonar chord progressive translation system
- Flashback events triggered by knowledge milestones
- Random equipment failure events

## Requirements Implemented
- a) Environment grid 25x25 with wrapping
- b) Grace agent with move, collect, experiment, EVA
- c) Rocky agent with sonar chords and tunnel
- d) Astrophage spreading and energy drain
- e) Taumoeba experimentation with Q-learning
- f) Beetle probes navigating the grid
- g) Resource constraints and equipment degradation
- h) Turn-based simulation with win and abort
- Expert: Q-learning, Astrophage resistance, procedural generation