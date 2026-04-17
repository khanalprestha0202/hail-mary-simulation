import matplotlib.pyplot as plt
import numpy as np
from simulation import Simulation


def run_multiple_simulations(num_runs=20):
    """Run simulation multiple times and collect statistics"""
    print(f"Running {num_runs} simulation runs...")
    print("Please wait...\n")

    results = {
        "success_count": 0,
        "turns_list": [],
        "knowledge_list": [],
        "probes_list": [],
        "survival_rates": [],
        "outcomes": []
    }

    for i in range(num_runs):
        print(f"Run {i + 1}/{num_runs}...", end=" ")
        sim = Simulation()

        # Run silently
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        sim.run(max_turns=100)

        sys.stdout = old_stdout

        # Collect results
        results["turns_list"].append(sim.turn)
        results["knowledge_list"].append(sim.grace.knowledge)
        results["probes_list"].append(sim.probe_counter)
        results["survival_rates"].append(
            sim.taumoeba.survival_rate_earth
        )

        if sim.mission_success:
            results["success_count"] += 1
            results["outcomes"].append("Success")
            print("✅ Success")
        else:
            results["outcomes"].append("Failed")
            print("❌ Failed")

    return results


def print_statistics(results, num_runs):
    """Print statistical summary"""
    print("\n" + "=" * 55)
    print("         SIMULATION STATISTICS REPORT")
    print("=" * 55)

    success_rate = results["success_count"] / num_runs * 100
    print(f"\nTotal Runs:          {num_runs}")
    print(f"Successful Missions: {results['success_count']}")
    print(f"Failed Missions:     {num_runs - results['success_count']}")
    print(f"Success Rate:        {success_rate:.1f}%")

    print(f"\n--- Turns to Complete ---")
    print(f"Average: {np.mean(results['turns_list']):.1f}")
    print(f"Min:     {np.min(results['turns_list'])}")
    print(f"Max:     {np.max(results['turns_list'])}")
    print(f"Std Dev: {np.std(results['turns_list']):.1f}")

    print(f"\n--- Knowledge Score ---")
    print(f"Average: {np.mean(results['knowledge_list']):.1f}")
    print(f"Min:     {np.min(results['knowledge_list']):.0f}")
    print(f"Max:     {np.max(results['knowledge_list']):.0f}")
    print(f"Std Dev: {np.std(results['knowledge_list']):.1f}")

    print(f"\n--- Probes Deployed ---")
    print(f"Average: {np.mean(results['probes_list']):.1f}")
    print(f"Min:     {np.min(results['probes_list'])}")
    print(f"Max:     {np.max(results['probes_list'])}")

    print(f"\n--- Taumoeba Earth Survival Rate ---")
    print(f"Average: {np.mean(results['survival_rates']):.1%}")
    print(f"Min:     {np.min(results['survival_rates']):.1%}")
    print(f"Max:     {np.max(results['survival_rates']):.1%}")
    print("=" * 55)


def plot_statistics(results, num_runs):
    """Create statistical graphs"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.patch.set_facecolor('#0a0a2e')
    fig.suptitle(
        'Project Hail Mary - Simulation Statistics\n'
        f'({num_runs} runs)',
        color='white', fontsize=16, fontweight='bold'
    )

    plot_style = {
        'facecolor': '#0a0a2e',
        'title_color': 'white',
        'label_color': 'white',
        'tick_color': 'white'
    }

    def style_ax(ax, title, xlabel, ylabel):
        ax.set_facecolor('#1a1a3e')
        ax.set_title(title, color=plot_style['title_color'],
                     fontsize=11, fontweight='bold')
        ax.set_xlabel(xlabel, color=plot_style['label_color'])
        ax.set_ylabel(ylabel, color=plot_style['label_color'])
        ax.tick_params(colors=plot_style['tick_color'])
        for spine in ax.spines.values():
            spine.set_edgecolor('#444444')

    # 1. Success vs Failure pie chart
    ax1 = axes[0, 0]
    success = results["success_count"]
    failure = num_runs - success
    colors = ['#00FF00', '#FF0000']
    ax1.pie(
        [success, failure],
        labels=['Success', 'Failed'],
        colors=colors,
        autopct='%1.1f%%',
        textprops={'color': 'white'}
    )
    ax1.set_facecolor('#0a0a2e')
    ax1.set_title('Mission Outcomes',
                  color='white', fontsize=11, fontweight='bold')

    # 2. Turns histogram
    ax2 = axes[0, 1]
    ax2.hist(results["turns_list"], bins=10,
             color='#4169E1', edgecolor='white', alpha=0.8)
    style_ax(ax2, 'Turns to Complete',
             'Number of Turns', 'Frequency')
    ax2.axvline(np.mean(results["turns_list"]),
                color='#00FFFF', linestyle='--',
                label=f'Mean: {np.mean(results["turns_list"]):.1f}')
    ax2.legend(facecolor='#1a1a3e', labelcolor='white')

    # 3. Knowledge scores
    ax3 = axes[0, 2]
    run_numbers = list(range(1, num_runs + 1))
    colors_scatter = ['#00FF00' if o == 'Success' else '#FF0000'
                      for o in results["outcomes"]]
    ax3.scatter(run_numbers, results["knowledge_list"],
                c=colors_scatter, s=80, alpha=0.8)
    ax3.axhline(np.mean(results["knowledge_list"]),
                color='#00FFFF', linestyle='--',
                label=f'Mean: {np.mean(results["knowledge_list"]):.0f}')
    style_ax(ax3, 'Knowledge Score Per Run',
             'Run Number', 'Knowledge Score')
    ax3.legend(facecolor='#1a1a3e', labelcolor='white')

    # 4. Taumoeba survival rates
    ax4 = axes[1, 0]
    ax4.bar(run_numbers, results["survival_rates"],
            color='#228B22', edgecolor='white', alpha=0.8)
    ax4.axhline(0.8, color='#00FFFF', linestyle='--',
                label='Viability threshold (80%)')
    ax4.axhline(np.mean(results["survival_rates"]),
                color='yellow', linestyle=':',
                label=f'Mean: {np.mean(results["survival_rates"]):.1%}')
    style_ax(ax4, 'Taumoeba Earth Survival Rate',
             'Run Number', 'Survival Rate')
    ax4.set_ylim(0, 1.1)
    ax4.legend(facecolor='#1a1a3e', labelcolor='white', fontsize=8)

    # 5. Probes deployed
    ax5 = axes[1, 1]
    probe_counts = [0, 1, 2, 3, 4]
    probe_freq = [results["probes_list"].count(p)
                  for p in probe_counts]
    ax5.bar(probe_counts, probe_freq,
            color='#9400D3', edgecolor='white', alpha=0.8)
    style_ax(ax5, 'Beetle Probes Deployed',
             'Probes Deployed', 'Frequency')
    ax5.set_xticks(probe_counts)

    # 6. Turns boxplot
    ax6 = axes[1, 2]
    bp = ax6.boxplot(
        results["turns_list"],
        patch_artist=True,
        boxprops=dict(facecolor='#4169E1', color='white'),
        medianprops=dict(color='#00FFFF', linewidth=2),
        whiskerprops=dict(color='white'),
        capprops=dict(color='white'),
        flierprops=dict(color='white', markeredgecolor='white')
    )
    style_ax(ax6, 'Turns Distribution',
             'Simulation', 'Turns')
    ax6.set_xticks([])

    plt.tight_layout()
    plt.savefig('simulation_statistics.png',
                facecolor='#0a0a2e', bbox_inches='tight',
                dpi=150)
    print("\nStatistics graph saved as 'simulation_statistics.png'")
    plt.show()


if __name__ == "__main__":
    NUM_RUNS = 20
    results = run_multiple_simulations(NUM_RUNS)
    print_statistics(results, NUM_RUNS)
    plot_statistics(results, NUM_RUNS)