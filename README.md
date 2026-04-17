# Project Hail Mary Simulation
## CPS7004 - Artificial Intelligence

**Author:** Prestha Khanal

**GitHub:** https://github.com/khanalprestha0202/hail-mary-simulation

---

## Overview

A multi-agent AI simulation based on Andy Weir's *Project Hail Mary* novel. Two autonomous agents — Dr. Ryland Grace (human) and Rocky (Eridian alien) — cooperate to save Earth from extinction caused by a microscopic organism called Astrophage.

---

## Features

- 20x20 procedurally generated space grid with wrapping edges
- Grace agent with health, energy, knowledge, EVA and tunnel travel
- Rocky alien agent with movement, trust system and sonar communication
- Astrophage spreading threat with resistance mechanic
- Taumoeba breeding for Earth AND Erid atmospheres
- Beetle probe deployment (John, Paul, George, Ringo)
- Equipment failures and repair mechanics
- Online learning with reinforcement-based strategy weights
- Rocky reconnaissance system
- Live matplotlib visualisation with real-time grid
- 20 simulation runs with full statistical analysis

---

## How to Run

**1. Clone the repository**

    git clone https://github.com/khanalprestha0202/hail-mary-simulation.git
    cd hail-mary-simulation

**2. Install dependencies**

    pip install matplotlib

**3. Run the simulation**

    python main.py

**4. Choose a mode when prompted**

    1. Run with live visualisation
    2. Run statistics (20 runs)
    3. Single run text only

---

## Project Structure

    hail_mary_simulation/
    ├── main.py              Entry point and menu
    ├── simulation.py        Main simulation loop
    ├── environment.py       20x20 space grid
    ├── visualiser.py        Live matplotlib visuals
    ├── run_statistics.py    Statistical analysis
    ├── agents/
    │   ├── grace.py         Dr. Grace agent
    │   └── rocky.py         Rocky alien agent
    └── entities/
        ├── taumoeba.py      Taumoeba breeding
        └── beetle_probe.py  Beetle probes

---

## Simulation Results (20 runs)

| Metric | Result |
|--------|--------|
| Success Rate | 100% |
| Average Turns | 24.4 |
| Average Knowledge | 755 |
| Earth Survival Rate | 88.4% |
| Probes Deployed | 4.0 |

---

## Requirements

- Python 3.13+
- matplotlib