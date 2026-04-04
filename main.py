import os
import random
from src.simulation import Simulation
from src.visualisation import (
    plot_simulation_metrics,
    plot_multi_run_analysis,
    print_statistical_summary
)

def run_single_simulation(run_number, seed=None, verbose=False):
    """Run one simulation and return results"""
    sim = Simulation(max_turns=100, seed=seed)
    results = sim.run(verbose=verbose)
    print(f"Run {run_number:02d} | "
          f"Knowledge: {results['knowledge_score']:4d} | "
          f"Viability: {results['taumoeba_viability']:5.1f}% | "
          f"Probes: {results['probes_deployed']} | "
          f"Success: {'YES' if results['mission_success'] else 'no ':3s} | "
          f"Turns: {results['turns_survived']}")
    return results, sim.metrics

def main():
    print("="*60)
    print("  PROJECT HAIL MARY SIMULATION - CPS7004")
    print("  Multi-Agent AI Simulation")
    print("="*60)

    # Create results directory
    os.makedirs("results", exist_ok=True)

    NUM_RUNS = 20
    all_results = []
    all_metrics = []

    print(f"\nRunning {NUM_RUNS} simulation runs...\n")

    for i in range(1, NUM_RUNS + 1):
        results, metrics = run_single_simulation(
            run_number=i,
            seed=i * 42,
            verbose=False
        )
        all_results.append(results)
        all_metrics.append(metrics)

    # Print full statistical summary
    print_statistical_summary(all_results)

    # Show detailed metrics for best run
    best_run_idx = max(range(NUM_RUNS),
                       key=lambda i: all_results[i]["knowledge_score"])
    print(f"\nShowing detailed graphs for best run (Run {best_run_idx+1})...")
    plot_simulation_metrics(all_metrics[best_run_idx],
                            run_number=best_run_idx+1,
                            save=True)

    # Show multi-run analysis
    print("Showing multi-run statistical analysis...")
    plot_multi_run_analysis(all_results, save=True)

    print("\nGraphs saved to results/ folder.")
    print("Simulation complete!")

if __name__ == "__main__":
    main()