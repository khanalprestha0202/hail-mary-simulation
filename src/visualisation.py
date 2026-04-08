import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import statistics

def plot_simulation_metrics(metrics, run_number=1, save=False):
    """Plot key metrics from a single simulation run"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"Project Hail Mary Simulation - Run {run_number}", fontsize=14, fontweight='bold')

    turns = metrics["turns"]

    # Plot 1: Health and Energy
    axes[0,0].plot(turns, metrics["grace_health"], 'r-', label="Health", linewidth=2)
    axes[0,0].plot(turns, metrics["grace_energy"], 'b-', label="Energy", linewidth=2)
    axes[0,0].set_title("Grace: Health & Energy")
    axes[0,0].set_xlabel("Turn")
    axes[0,0].set_ylabel("Value (0-100)")
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].set_ylim(0, 110)

    # Plot 2: Knowledge Score
    axes[0,1].plot(turns, metrics["knowledge_score"], 'g-', linewidth=2)
    axes[0,1].fill_between(turns, metrics["knowledge_score"], alpha=0.3, color='green')
    axes[0,1].set_title("Knowledge Score Progression")
    axes[0,1].set_xlabel("Turn")
    axes[0,1].set_ylabel("Knowledge Points")
    axes[0,1].grid(True, alpha=0.3)

    # Plot 3: Taumoeba Viability
    axes[0,2].plot(turns, metrics["taumoeba_viability"], 'purple', linewidth=2)
    axes[0,2].axhline(y=80, color='gold', linestyle='--', label="Success Threshold (80%)")
    axes[0,2].fill_between(turns, metrics["taumoeba_viability"], alpha=0.3, color='purple')
    axes[0,2].set_title("Taumoeba Viability (%)")
    axes[0,2].set_xlabel("Turn")
    axes[0,2].set_ylabel("Viability %")
    axes[0,2].legend()
    axes[0,2].grid(True, alpha=0.3)
    axes[0,2].set_ylim(0, 110)

    # Plot 4: Mission Progress
    axes[1,0].plot(turns, metrics["mission_progress"], 'orange', linewidth=2)
    axes[1,0].fill_between(turns, metrics["mission_progress"], alpha=0.3, color='orange')
    axes[1,0].set_title("Mission Progress")
    axes[1,0].set_xlabel("Turn")
    axes[1,0].set_ylabel("Progress Score")
    axes[1,0].grid(True, alpha=0.3)

    # Plot 5: Rocky Cooperation
    axes[1,1].plot(turns, metrics["rocky_cooperation"], 'cyan', linewidth=2)
    axes[1,1].set_title("Rocky Cooperation Level")
    axes[1,1].set_xlabel("Turn")
    axes[1,1].set_ylabel("Cooperation (0-100)")
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].set_ylim(0, 110)

    # Plot 6: Astrophage Spread
    axes[1,2].plot(turns, metrics["astrophage_spread"], 'red', linewidth=2)
    axes[1,2].set_title("Astrophage Spread (Cells)")
    axes[1,2].set_xlabel("Turn")
    axes[1,2].set_ylabel("Infected Cells")
    axes[1,2].grid(True, alpha=0.3)

    plt.tight_layout()
    if save:
        plt.savefig(f"results/run_{run_number}_metrics.png", dpi=150, bbox_inches='tight')
    plt.show()


def plot_multi_run_analysis(all_results, save=False):
    """Plot analysis across 20+ simulation runs"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle("Project Hail Mary - Multi-Run Statistical Analysis (20 Runs)",
                 fontsize=14, fontweight='bold')

    runs = list(range(1, len(all_results) + 1))
    knowledge_scores = [r["knowledge_score"] for r in all_results]
    viabilities = [r["taumoeba_viability"] for r in all_results]
    turns_survived = [r["turns_survived"] for r in all_results]
    probes = [r["probes_deployed"] for r in all_results]
    success_rates = [r["success_rate"] for r in all_results]
    cooperation = [r["rocky_cooperation"] for r in all_results]

    # Plot 1: Knowledge score per run with mean line
    axes[0,0].bar(runs, knowledge_scores, color='green', alpha=0.7)
    mean_k = statistics.mean(knowledge_scores)
    axes[0,0].axhline(y=mean_k, color='red', linestyle='--',
                      label=f"Mean: {mean_k:.1f}")
    axes[0,0].set_title("Knowledge Score per Run")
    axes[0,0].set_xlabel("Run")
    axes[0,0].set_ylabel("Score")
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)

    # Plot 2: Taumoeba viability per run
    colours = ['gold' if v >= 80 else 'purple' for v in viabilities]
    axes[0,1].bar(runs, viabilities, color=colours, alpha=0.8)
    axes[0,1].axhline(y=80, color='red', linestyle='--', label="Success Threshold")
    axes[0,1].set_title("Taumoeba Viability per Run")
    axes[0,1].set_xlabel("Run")
    axes[0,1].set_ylabel("Viability %")
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)

    # Plot 3: Survival turns distribution
    axes[0,2].hist(turns_survived, bins=10, color='blue', alpha=0.7, edgecolor='black')
    axes[0,2].axvline(x=statistics.mean(turns_survived), color='red',
                      linestyle='--', label=f"Mean: {statistics.mean(turns_survived):.1f}")
    axes[0,2].set_title("Survival Turns Distribution")
    axes[0,2].set_xlabel("Turns Survived")
    axes[0,2].set_ylabel("Frequency")
    axes[0,2].legend()
    axes[0,2].grid(True, alpha=0.3)

    # Plot 4: Beetle probes deployed
    probe_counts = [0,0,0,0,0]
    for p in probes:
        probe_counts[min(p,4)] += 1
    axes[1,0].bar(range(5), probe_counts, color='orange', alpha=0.8, edgecolor='black')
    axes[1,0].set_title("Beetle Probes Deployed Distribution")
    axes[1,0].set_xlabel("Probes Deployed")
    axes[1,0].set_ylabel("Number of Runs")
    axes[1,0].set_xticks(range(5))
    axes[1,0].grid(True, alpha=0.3)

    # Plot 5: Experiment success rate per run
    axes[1,1].plot(runs, success_rates, 'g-o', linewidth=2, markersize=5)
    mean_sr = statistics.mean(success_rates)
    axes[1,1].axhline(y=mean_sr, color='red', linestyle='--',
                      label=f"Mean: {mean_sr:.1f}%")
    axes[1,1].set_title("Experiment Success Rate per Run")
    axes[1,1].set_xlabel("Run")
    axes[1,1].set_ylabel("Success Rate %")
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)

    # Plot 6: Rocky cooperation per run
    axes[1,2].plot(runs, cooperation, 'c-o', linewidth=2, markersize=5)
    axes[1,2].fill_between(runs, cooperation, alpha=0.3, color='cyan')
    axes[1,2].set_title("Rocky Cooperation Level per Run")
    axes[1,2].set_xlabel("Run")
    axes[1,2].set_ylabel("Cooperation (0-100)")
    axes[1,2].grid(True, alpha=0.3)

    plt.tight_layout()
    if save:
        plt.savefig("results/multi_run_analysis.png", dpi=150, bbox_inches='tight')
    plt.show()


def print_statistical_summary(all_results):
    """Print a full statistical summary of all runs"""
    knowledge = [r["knowledge_score"] for r in all_results]
    viability = [r["taumoeba_viability"] for r in all_results]
    turns = [r["turns_survived"] for r in all_results]
    probes = [r["probes_deployed"] for r in all_results]
    successes = sum(1 for r in all_results if r["mission_success"])
    success_rates = [r["success_rate"] for r in all_results]
    cooperation = [r["rocky_cooperation"] for r in all_results]

    print("\n" + "="*60)
    print("   PROJECT HAIL MARY - FULL STATISTICAL ANALYSIS")
    print("   CPS7004 Artificial Intelligence - Assessment 1")
    print("="*60)
    print(f"  Total Runs:               {len(all_results)}")
    print(f"  Mission Successes:        {successes}/{len(all_results)} "
          f"({successes/len(all_results)*100:.1f}%)")
    print(f"")
    print(f"  Knowledge Score:")
    print(f"    Mean:                   {statistics.mean(knowledge):.2f}")
    print(f"    Std Dev:                {statistics.stdev(knowledge):.2f}")
    print(f"    Min:                    {min(knowledge)}")
    print(f"    Max:                    {max(knowledge)}")
    print(f"")
    print(f"  Taumoeba Viability (%):")
    print(f"    Mean:                   {statistics.mean(viability):.2f}%")
    print(f"    Std Dev:                {statistics.stdev(viability):.2f}%")
    print(f"    Min:                    {min(viability):.2f}%")
    print(f"    Max:                    {max(viability):.2f}%")
    print(f"")
    print(f"  Survival Turns:")
    print(f"    Mean:                   {statistics.mean(turns):.2f}")
    print(f"    Std Dev:                {statistics.stdev(turns):.2f}")
    print(f"")
    print(f"  Avg Beetle Probes/Run:    {statistics.mean(probes):.2f}")
    print(f"  Avg Experiment Success:   {statistics.mean(success_rates):.1f}%")
    print(f"  Avg Rocky Cooperation:    {statistics.mean(cooperation):.1f}")
    print("="*60)

def plot_grid(environment, grace, rocky, beetle_probes=None, turn=0):
    """Real-time colour-coded grid visualisation"""
    import numpy as np
    from src.environment import EMPTY, ASTROPHAGE, ADRIAN, HAIL_MARY, BLIP_A, RADIATION, TAUMOEBA

    colour_map = {
        EMPTY:      [15,  15,  35],
        ASTROPHAGE: [220, 60,  20],
        ADRIAN:     [30,  160, 80],
        HAIL_MARY:  [80,  180, 255],
        BLIP_A:     [255, 200, 50],
        RADIATION:  [180, 50,  180],
        TAUMOEBA:   [50,  220, 150],
        RELATIVISTIC: [100, 100, 200],  # Blue warp zones
    }

    h, w = environment.height, environment.width
    img = np.zeros((h, w, 3), dtype=np.uint8)

    for r in range(h):
        for c in range(w):
            cell = environment.grid[r][c]
            img[r, c] = colour_map.get(cell, [100, 100, 100])

    img[grace.row % h, grace.col % w] = [255, 255, 255]
    img[rocky.row % h, rocky.col % w] = [255, 230, 100]

    if beetle_probes:
        for probe in beetle_probes:
            img[probe.row % h, probe.col % w] = [200, 255, 200]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.imshow(img, interpolation='nearest')
    ax.set_title(f"Tau Ceti System — Turn {turn} | Knowledge: {grace.knowledge_score} | "
                 f"Viability: {grace.taumoeba_viability*100:.1f}%", fontsize=11)

    from matplotlib.patches import Patch
    legend = [
        Patch(color=[c/255 for c in colour_map[EMPTY]],     label="Empty space"),
        Patch(color=[c/255 for c in colour_map[ASTROPHAGE]], label="Astrophage"),
        Patch(color=[c/255 for c in colour_map[ADRIAN]],    label="Planet Adrian"),
        Patch(color=[c/255 for c in colour_map[RADIATION]], label="Radiation zone"),
        Patch(color=[c/255 for c in colour_map[TAUMOEBA]],  label="Taumoeba"),
        Patch(color=[1,1,1],     label="Grace (Hail Mary)"),
        Patch(color=[1,0.9,0.4], label="Rocky (Blip-A)"),
    ]
    ax.legend(handles=legend, loc='upper right', fontsize=8,
              framealpha=0.85, facecolor='#111122', labelcolor='white')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"results/grid_turn_{turn:03d}.png", dpi=120, bbox_inches='tight')
    plt.show(block=False)
    plt.pause(0.1)