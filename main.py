import os
import sys
import random
import matplotlib
try:
    if sys.platform == 'darwin':
        matplotlib.use('MacOSX')
    else:
        matplotlib.use('Agg')
except Exception:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.simulation import Simulation
from src.visualisation import (
    plot_simulation_metrics,
    plot_multi_run_analysis,
    print_statistical_summary,
)


def run_single_simulation(run_number, seed=None, verbose=False):
    """Run one simulation and return results"""
    sim = Simulation(max_turns=150, seed=seed)
    results = sim.run(verbose=verbose)

    # Print chord log for first run to show Rocky communication
    if run_number == 1 and results.get("chord_log"):
        print("\n  --- Rocky's Sonar Chord Communication Log ---")
        for chord in results["chord_log"][:6]:
            print(f"  {chord}")
        print()

    print(
        f"Run {run_number:02d} | "
        f"Knowledge: {results['knowledge_score']:4d} | "
        f"Viability: {results['taumoeba_viability']:5.1f}% | "
        f"Probes: {results['probes_deployed']} | "
        f"Tunnel: {'YES' if results['tunnel_built'] else 'no ':3s} | "
        f"EVAs: {results['eva_count']} | "
        f"Success: {'YES ✓' if results['mission_success'] else 'no  '} | "
        f"Turns: {results['turns_survived']}"
    )
    return results, sim.metrics


def main():
    print("=" * 70)
    print("  PROJECT HAIL MARY SIMULATION - CPS7004")
    print("  Multi-Agent AI Simulation with Q-Learning")
    print("=" * 70)

    os.makedirs("results", exist_ok=True)

    NUM_RUNS = 20
    all_results = []
    all_metrics = []

    print(f"\nRunning {NUM_RUNS} simulation runs...\n")

    for i in range(1, NUM_RUNS + 1):
        results, metrics = run_single_simulation(
            run_number=i,
            seed=i * 42,
            verbose=False,
        )
        all_results.append(results)
        all_metrics.append(metrics)

    # Print full statistical summary
    print_statistical_summary(all_results)

    # Print Q-learning summary from last run
    last_exp = all_results[-1].get("experiment_stats", {})
    if last_exp.get("q_policy"):
        print(f"\n  Q-Learning Policy Summary:")
        print(f"  {last_exp['q_policy']}")
        print(f"  Q-Table States Explored: {last_exp.get('q_table_size', 0)}")
        print(f"  Final Epsilon: {last_exp.get('epsilon', 0):.3f}")

    # Save graphs automatically without needing to close
    best_run_idx = max(range(NUM_RUNS),
                       key=lambda i: all_results[i]["knowledge_score"])
    print(f"\nSaving graphs for best run (Run {best_run_idx + 1})...")
    plot_simulation_metrics(
        all_metrics[best_run_idx],
        run_number=best_run_idx + 1,
        save=True,
    )
    plt.close('all')

    print("Saving multi-run analysis...")
    plot_multi_run_analysis(all_results, save=True)
    plt.close('all')

    print(f"\nAll graphs saved to results/ folder.")
    print("Open the results/ folder on your Desktop to view them.")
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()

