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

        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        sim.run_text_only(max_turns=100)

        sys.stdout = old_stdout

        results["turns_list"].append(sim.turn)
        results["knowledge_list"].append(sim.grace.knowledge)
        results["probes_list"].append(sim.probe_counter)
        results["survival_rates"].append(
            sim.taumoeba.survival_rate_earth
        )

        if sim.mission_success:
            results["success_count"] += 1
            results["outcomes"].append("Success")
            print("SUCCESS")
        else:
            results["outcomes"].append("Failed")
            print("Failed")

    return results


def print_statistics(results, num_runs):
    """Print statistical summary"""
    print("\n" + "=" * 55)
    print("      SIMULATION STATISTICS REPORT")
    print("=" * 55)

    success_rate = results["success_count"] / num_runs * 100
    print(f"\nTotal Runs:          {num_runs}")
    print(f"Successful Missions: {results['success_count']}")
    print(f"Failed Missions:     "
          f"{num_runs - results['success_count']}")
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
    """Create clean professional statistical graphs"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.patch.set_facecolor('#0d1117')
    fig.suptitle(
        'Project Hail Mary — Simulation Statistics',
        color='white', fontsize=16,
        fontweight='bold', y=0.98
    )

    def style_ax(ax, title, xlabel, ylabel):
        ax.set_facecolor('#161b22')
        ax.set_title(
            title, color='#58a6ff',
            fontsize=11, fontweight='bold', pad=10
        )
        ax.set_xlabel(xlabel, color='#8b949e', fontsize=9)
        ax.set_ylabel(ylabel, color='#8b949e', fontsize=9)
        ax.tick_params(colors='#8b949e', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        ax.grid(
            True, color='#21262d',
            linewidth=0.5, alpha=0.7
        )

    run_numbers = list(range(1, num_runs + 1))

    # 1. Pie chart - clean donut style
    ax1 = axes[0, 0]
    ax1.set_facecolor('#161b22')
    success = results["success_count"]
    failure = num_runs - success

    if failure == 0:
        pie_values = [success, 0.0001]
        pie_labels = ['Success', '']
    else:
        pie_values = [success, failure]
        pie_labels = ['Success', 'Failed']

    wedges, texts, autotexts = ax1.pie(
        pie_values,
        labels=pie_labels,
        colors=['#3fb950', '#f85149'],
        autopct=lambda p: f'{p:.0f}%' if p > 1 else '',
        startangle=90,
        wedgeprops=dict(
            width=0.6,
            edgecolor='#0d1117',
            linewidth=2
        ),
        textprops={
            'color': '#c9d1d9',
            'fontsize': 10
        }
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(12)
        at.set_fontweight('bold')
    ax1.set_title(
        'Mission Outcomes',
        color='#58a6ff',
        fontsize=11,
        fontweight='bold',
        pad=10
    )
    ax1.text(
        0, 0,
        f'{success}/{num_runs}\nSuccess',
        ha='center', va='center',
        color='#3fb950',
        fontsize=11,
        fontweight='bold'
    )

    # 2. Turns histogram
    ax2 = axes[0, 1]
    style_ax(
        ax2, 'Turns to Complete Mission',
        'Number of Turns', 'Frequency'
    )
    ax2.hist(
        results["turns_list"], bins=8,
        color='#388bfd',
        edgecolor='#0d1117',
        linewidth=1.2,
        alpha=0.9
    )
    mean_turns = np.mean(results["turns_list"])
    ax2.axvline(
        mean_turns,
        color='#f0883e',
        linestyle='--',
        linewidth=2,
        label=f'Mean: {mean_turns:.1f} turns'
    )
    ax2.legend(
        facecolor='#21262d',
        labelcolor='#c9d1d9',
        fontsize=9,
        framealpha=0.8
    )

    # 3. Knowledge score scatter
    ax3 = axes[0, 2]
    style_ax(
        ax3, 'Knowledge Score per Run',
        'Run Number', 'Knowledge Score'
    )
    dot_colors = [
        '#3fb950' if o == 'Success' else '#f85149'
        for o in results["outcomes"]
    ]
    ax3.scatter(
        run_numbers,
        results["knowledge_list"],
        c=dot_colors,
        s=70,
        alpha=0.9,
        zorder=5,
        edgecolors='#0d1117',
        linewidth=0.5
    )
    mean_k = np.mean(results["knowledge_list"])
    ax3.axhline(
        mean_k,
        color='#f0883e',
        linestyle='--',
        linewidth=1.8,
        label=f'Mean: {mean_k:.0f}'
    )
    ax3.legend(
        facecolor='#21262d',
        labelcolor='#c9d1d9',
        fontsize=9,
        framealpha=0.8
    )

    # 4. Taumoeba survival rate
    ax4 = axes[1, 0]
    style_ax(
        ax4, 'Taumoeba Earth Survival Rate',
        'Run Number', 'Survival Rate'
    )
    bar_colors = [
        '#3fb950' if r >= 0.8 else
        '#d29922' if r >= 0.5 else
        '#f85149'
        for r in results["survival_rates"]
    ]
    ax4.bar(
        run_numbers,
        results["survival_rates"],
        color=bar_colors,
        edgecolor='#0d1117',
        linewidth=0.8,
        alpha=0.9,
        width=0.7
    )
    ax4.axhline(
        0.8,
        color='#58a6ff',
        linestyle='--',
        linewidth=1.8,
        label='Viability threshold (80%)'
    )
    mean_s = np.mean(results["survival_rates"])
    ax4.axhline(
        mean_s,
        color='#f0883e',
        linestyle=':',
        linewidth=1.8,
        label=f'Mean: {mean_s:.1%}'
    )
    ax4.set_ylim(0, 1.15)
    ax4.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{x:.0%}')
    )
    ax4.legend(
        facecolor='#21262d',
        labelcolor='#c9d1d9',
        fontsize=8,
        framealpha=0.8
    )

    # 5. Probes deployed
    ax5 = axes[1, 1]
    style_ax(
        ax5, 'Beetle Probes Deployed',
        'Probes Deployed', 'Number of Runs'
    )
    probe_counts = [0, 1, 2, 3, 4]
    probe_freq = [
        results["probes_list"].count(p)
        for p in probe_counts
    ]
    bars = ax5.bar(
        probe_counts,
        probe_freq,
        color='#8957e5',
        edgecolor='#0d1117',
        linewidth=0.8,
        alpha=0.9,
        width=0.5
    )
    for bar, freq in zip(bars, probe_freq):
        if freq > 0:
            ax5.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                str(freq),
                ha='center',
                color='#c9d1d9',
                fontsize=10,
                fontweight='bold'
            )
    ax5.set_xticks(probe_counts)

    # 6. Summary stats text panel
    ax6 = axes[1, 2]
    ax6.set_facecolor('#161b22')
    ax6.axis('off')
    ax6.set_title(
        'Summary Statistics',
        color='#58a6ff',
        fontsize=11,
        fontweight='bold',
        pad=10
    )

    success_rate = results["success_count"] / num_runs * 100
    summary_lines = [
        ('Total Runs', f'{num_runs}'),
        ('Success Rate', f'{success_rate:.0f}%'),
        ('Avg Turns',
         f'{np.mean(results["turns_list"]):.1f}'),
        ('Min Turns',
         f'{np.min(results["turns_list"])}'),
        ('Max Turns',
         f'{np.max(results["turns_list"])}'),
        ('Avg Knowledge',
         f'{np.mean(results["knowledge_list"]):.0f}'),
        ('Avg Survival',
         f'{np.mean(results["survival_rates"]):.1%}'),
        ('Avg Probes',
         f'{np.mean(results["probes_list"]):.1f}'),
    ]

    for i, (label, value) in enumerate(summary_lines):
        y_pos = 0.88 - i * 0.11
        ax6.text(
            0.05, y_pos, label,
            transform=ax6.transAxes,
            color='#8b949e', fontsize=10
        )
        ax6.text(
            0.95, y_pos, value,
            transform=ax6.transAxes,
            color='#3fb950', fontsize=10,
            fontweight='bold', ha='right'
        )
        # Divider line using plot
        ax6.plot(
            [0.02, 0.98],
            [y_pos - 0.03, y_pos - 0.03],
            color='#21262d',
            linewidth=0.5,
            transform=ax6.transAxes
        )

    plt.tight_layout(pad=2.0)
    plt.savefig(
        'simulation_statistics.png',
        facecolor='#0d1117',
        bbox_inches='tight',
        dpi=150
    )
    print("\nGraph saved as 'simulation_statistics.png'")
    print("Close the graph window to exit.")
    plt.show(block=True)


if __name__ == "__main__":
    NUM_RUNS = 20
    results = run_multiple_simulations(NUM_RUNS)
    print_statistics(results, NUM_RUNS)
    plot_statistics(results, NUM_RUNS)