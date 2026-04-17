# Project Hail Mary Simulation
## CPS7004 - Artificial Intelligence Assessment

A multi-agent simulation based on Andy Weir's "Project Hail Mary" novel.

## Overview
This simulation models the Hail Mary mission near the Tau Ceti system, featuring:
- Dr. Ryland Grace (human agent)
- Rocky (Eridian alien agent)
- Astrophage threat spreading across space
- Taumoeba breeding experiments
- Beetle probe deployments to Earth

## How to Run
python main.py

## Project Structure
hail_mary_simulation/
├── main.py              - Entry point
├── simulation.py        - Main simulation loop
├── environment.py       - 20x20 space grid
├── agents/
│   ├── grace.py         - Dr. Grace agent
│   └── rocky.py         - Rocky alien agent
├── entities/
│   ├── taumoeba.py      - Taumoeba organism
│   └── beetle_probe.py  - Autonomous probes

## Requirements
- Python 3.13
- matplotlib

## Author
CPS7004 Artificial Intelligence Assessment