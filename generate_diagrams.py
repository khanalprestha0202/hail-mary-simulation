import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe


def draw_class_diagram():
    """Generate Class Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')

    ax.text(10, 13.5,
            'Project Hail Mary — Class Diagram',
            color='white', fontsize=16,
            fontweight='bold', ha='center')

    def draw_class_box(ax, x, y, width, height,
                       class_name, attributes, methods,
                       color='#58a6ff'):
        # Main box
        box = FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.1",
            facecolor='#161b22',
            edgecolor=color,
            linewidth=2
        )
        ax.add_patch(box)

        # Class name background
        header = FancyBboxPatch(
            (x, y + height - 0.6), width, 0.6,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor=color,
            linewidth=1,
            alpha=0.8
        )
        ax.add_patch(header)

        # Class name
        ax.text(x + width/2, y + height - 0.3,
                class_name,
                color='white', fontsize=9,
                fontweight='bold', ha='center',
                va='center')

        # Divider line
        ax.plot([x, x + width],
                [y + height - 0.65, y + height - 0.65],
                color=color, linewidth=1, alpha=0.5)

        # Attributes
        attr_start = y + height - 0.9
        for attr in attributes:
            ax.text(x + 0.15, attr_start,
                    attr, color='#8b949e',
                    fontsize=7, va='center')
            attr_start -= 0.28

        # Divider
        ax.plot([x, x + width],
                [attr_start + 0.1, attr_start + 0.1],
                color=color, linewidth=0.5,
                alpha=0.3, linestyle='--')

        # Methods
        method_start = attr_start - 0.1
        for method in methods:
            ax.text(x + 0.15, method_start,
                    method, color='#3fb950',
                    fontsize=7, va='center')
            method_start -= 0.28

    def draw_arrow(ax, x1, y1, x2, y2,
                   label='', color='#58a6ff'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=color,
                lw=1.5
            )
        )
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(mx, my + 0.1, label,
                    color=color, fontsize=7,
                    ha='center', style='italic')

    # --- Draw all classes ---

    # Simulation (centre top)
    draw_class_box(
        ax, 7.5, 9.5, 5, 3.5,
        'Simulation',
        ['- grace: Grace',
         '- rocky: Rocky',
         '- taumoeba: Taumoeba',
         '- environment: Environment',
         '- beetle_probes: list',
         '- turn: int',
         '- mission_success: bool'],
        ['+ step()',
         '+ run(max_turns)',
         '+ run_text_only()',
         '+ _grace_action()',
         '+ _rocky_action()',
         '+ _deploy_probe()'],
        color='#f0883e'
    )

    # Environment (left)
    draw_class_box(
        ax, 0.5, 8.5, 4, 3.5,
        'Environment',
        ['- width: int',
         '- height: int',
         '- grid: Cell[][]',
         '- turn: int',
         '- taumoeba_deployed: int'],
        ['+ setup_world()',
         '+ spread_astrophage()',
         '+ get_cell(x, y)',
         '+ apply_taumoeba_resistance()',
         '+ trigger_equipment_failure()',
         '+ display()'],
        color='#58a6ff'
    )

    # Cell (far left)
    draw_class_box(
        ax, 0.5, 5.0, 4, 3.0,
        'Cell',
        ['- cell_type: str',
         '- astrophage_level: int',
         '- astrophage_resistance: int',
         '- has_taumoeba: bool',
         '- is_time_dilation: bool'],
        ['+ __str__()'],
        color='#58a6ff'
    )

    # Grace (right)
    draw_class_box(
        ax, 15.5, 8.0, 4, 4.5,
        'Grace',
        ['- health: int',
         '- energy: int',
         '- knowledge: int',
         '- taumoeba_samples: int',
         '- beetle_probes: int',
         '- strategy_weights: dict',
         '- experiment_history: dict'],
        ['+ move()',
         '+ collect_sample()',
         '+ conduct_experiment()',
         '+ deploy_beetle_probe()',
         '+ flashback()',
         '+ travel_tunnel()',
         '+ perform_eva()'],
        color='#00FFFF'
    )

    # Rocky (far right)
    draw_class_box(
        ax, 15.5, 4.0, 4, 3.5,
        'Rocky',
        ['- health: int',
         '- energy: int',
         '- trust_level: int',
         '- translation_level: int',
         '- astrophage_fuel: int',
         '- ship_contaminated: bool'],
        ['+ communicate()',
         '+ share_knowledge()',
         '+ perform_repair()',
         '+ transfer_fuel()',
         '+ conduct_reconnaissance()',
         '+ assist_experiment()'],
        color='#FF69B4'
    )

    # Taumoeba (bottom centre)
    draw_class_box(
        ax, 7.5, 4.5, 5, 3.5,
        'Taumoeba',
        ['- survival_rate_earth: float',
         '- survival_rate_erid: float',
         '- generation: int',
         '- mutation_rate: float',
         '- breeding_log: list'],
        ['+ breed_for_earth()',
         '+ breed_for_erid()',
         '+ consume_astrophage()',
         '+ is_viable_earth()',
         '+ is_viable_erid()'],
        color='#3fb950'
    )

    # BeetleProbe (bottom left)
    draw_class_box(
        ax, 0.5, 1.0, 4, 3.5,
        'BeetleProbe',
        ['- name: str',
         '- knowledge_payload: int',
         '- data_integrity: int',
         '- reached_earth: bool',
         '- turns_in_flight: int'],
        ['+ navigate()',
         '+ configure()',
         '+ status()'],
        color='#9400D3'
    )

    # --- Draw arrows ---
    # Simulation uses Environment
    draw_arrow(ax, 7.5, 11.0, 4.5, 11.0,
               'uses', '#58a6ff')
    # Simulation controls Grace
    draw_arrow(ax, 12.5, 11.5, 15.5, 11.5,
               'controls', '#00FFFF')
    # Simulation controls Rocky
    draw_arrow(ax, 12.5, 10.5, 15.5, 6.5,
               'controls', '#FF69B4')
    # Simulation manages Taumoeba
    draw_arrow(ax, 10.0, 9.5, 10.0, 8.0,
               'manages', '#3fb950')
    # Simulation deploys BeetleProbe
    draw_arrow(ax, 7.5, 10.0, 4.5, 3.5,
               'deploys', '#9400D3')
    # Environment contains Cell
    draw_arrow(ax, 2.5, 8.5, 2.5, 8.0,
               'contains', '#58a6ff')
    # Grace experiments on Taumoeba
    draw_arrow(ax, 15.5, 9.5, 12.5, 7.0,
               'experiments', '#3fb950')
    # Rocky cooperates with Grace
    draw_arrow(ax, 15.5, 7.0, 15.5, 8.0,
               'cooperates', '#FF69B4')

    plt.tight_layout()
    plt.savefig(
        'diagram_classes.png',
        facecolor='#0d1117',
        bbox_inches='tight',
        dpi=150
    )
    print("Class diagram saved as 'diagram_classes.png'")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


def draw_flowchart():
    """Generate Simulation Flowchart"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 20))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 20)
    ax.axis('off')

    ax.text(7, 19.5,
            'Project Hail Mary — Simulation Flowchart',
            color='white', fontsize=14,
            fontweight='bold', ha='center')

    def draw_box(ax, x, y, w, h, text,
                 shape='rect', color='#58a6ff',
                 text_color='white', fontsize=8):
        if shape == 'diamond':
            diamond = plt.Polygon(
                [[x, y + h/2],
                 [x + w/2, y + h],
                 [x + w, y + h/2],
                 [x + w/2, y]],
                facecolor='#1a1a3e',
                edgecolor=color,
                linewidth=2
            )
            ax.add_patch(diamond)
            ax.text(x + w/2, y + h/2, text,
                    color=text_color,
                    fontsize=fontsize,
                    ha='center', va='center',
                    fontweight='bold')
        elif shape == 'oval':
            ellipse = mpatches.Ellipse(
                (x + w/2, y + h/2), w, h,
                facecolor=color,
                edgecolor='white',
                linewidth=2
            )
            ax.add_patch(ellipse)
            ax.text(x + w/2, y + h/2, text,
                    color='white',
                    fontsize=fontsize + 1,
                    ha='center', va='center',
                    fontweight='bold')
        else:
            box = FancyBboxPatch(
                (x, y), w, h,
                boxstyle="round,pad=0.1",
                facecolor='#161b22',
                edgecolor=color,
                linewidth=2
            )
            ax.add_patch(box)
            ax.text(x + w/2, y + h/2, text,
                    color=text_color,
                    fontsize=fontsize,
                    ha='center', va='center',
                    fontweight='bold')

    def draw_flow_arrow(ax, x1, y1, x2, y2,
                        label='', color='#8b949e'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=color,
                lw=1.5
            )
        )
        if label:
            mx = (x1 + x2) / 2 + 0.2
            my = (y1 + y2) / 2
            ax.text(mx, my, label,
                    color=color, fontsize=7,
                    ha='left')

    # START
    draw_box(ax, 5, 18.5, 4, 0.7,
             'START', shape='oval',
             color='#3fb950')

    # Initialise
    draw_box(ax, 4, 17.3, 6, 0.8,
             'Initialise Simulation\n'
             '(Environment, Grace, Rocky, Taumoeba)',
             color='#58a6ff')

    # Grace wakes
    draw_box(ax, 4, 16.2, 6, 0.8,
             'Grace wakes from coma\n'
             'Memory = 0, Knowledge = 0',
             color='#58a6ff')

    # Rocky encountered
    draw_box(ax, 4, 15.1, 6, 0.8,
             'Rocky encountered at Tau Ceti\n'
             'Begin communication',
             color='#FF69B4')

    # Turn loop
    draw_box(ax, 4.5, 14.0, 5, 0.7,
             'BEGIN TURN',
             color='#f0883e',
             text_color='white')

    # Grace action decision
    draw_box(ax, 3.5, 12.6, 7, 1.1,
             'Grace Action?\n'
             'Energy < 15?',
             shape='diamond',
             color='#00FFFF')

    # Rest
    draw_box(ax, 0.5, 12.7, 2.5, 0.7,
             'Grace Rests\n+20 Energy',
             color='#00FFFF')

    # Taumoeba viable?
    draw_box(ax, 3.5, 11.2, 7, 1.1,
             'Taumoeba Viable\nfor Earth?',
             shape='diamond',
             color='#3fb950')

    # Deploy probe
    draw_box(ax, 0.5, 11.3, 2.5, 0.7,
             'Deploy\nBeetle Probe',
             color='#9400D3')

    # Enough samples?
    draw_box(ax, 3.5, 9.8, 7, 1.1,
             'Taumoeba Samples >= 2\nand Knowledge >= 20?',
             shape='diamond',
             color='#3fb950')

    # Breed
    draw_box(ax, 0.5, 9.9, 2.5, 0.7,
             'Breed\nTaumoeba',
             color='#3fb950')

    # On planet?
    draw_box(ax, 3.5, 8.5, 7, 1.0,
             'Grace on Planet Adrian?',
             shape='diamond',
             color='#228B22')

    # Collect
    draw_box(ax, 0.5, 8.6, 2.5, 0.7,
             'Collect\nSamples',
             color='#228B22')

    # Move
    draw_box(ax, 4, 7.5, 6, 0.7,
             'Move Toward Planet Adrian\n'
             '(Avoid Astrophage hazards)',
             color='#58a6ff')

    # Rocky action
    draw_box(ax, 4, 6.5, 6, 0.7,
             'Rocky Actions:\n'
             'Communicate, Share, Assist, Repair',
             color='#FF69B4')

    # Environment update
    draw_box(ax, 4, 5.5, 6, 0.7,
             'Environment Update:\n'
             'Spread Astrophage + Equipment Failures',
             color='#cc2200')

    # Navigate probes
    draw_box(ax, 4, 4.5, 6, 0.7,
             'Navigate Beetle Probes\n'
             'Check if reached Earth',
             color='#9400D3')

    # Check conditions
    draw_box(ax, 3.5, 3.4, 7, 0.8,
             'Mission Success?\n'
             '(Earth saved + Probe reached Earth)',
             shape='diamond',
             color='#3fb950')

    # Mission success
    draw_box(ax, 10.5, 3.5, 3, 0.6,
             'MISSION\nSUCCESS!',
             color='#3fb950',
             text_color='#3fb950')

    # Aborted?
    draw_box(ax, 3.5, 2.2, 7, 0.8,
             'Mission Aborted?\n'
             '(Grace health/energy = 0)',
             shape='diamond',
             color='#f85149')

    # Mission failed
    draw_box(ax, 10.5, 2.3, 3, 0.6,
             'MISSION\nFAILED',
             color='#f85149',
             text_color='#f85149')

    # Max turns?
    draw_box(ax, 3.5, 1.0, 7, 0.9,
             'Turn >= Max Turns?',
             shape='diamond',
             color='#f0883e')

    # End
    draw_box(ax, 5, 0.1, 4, 0.6,
             'END', shape='oval',
             color='#f85149')

    # --- Arrows ---
    draw_flow_arrow(ax, 7, 18.5, 7, 18.15)
    draw_flow_arrow(ax, 7, 17.3, 7, 17.0)
    draw_flow_arrow(ax, 7, 16.2, 7, 15.9)
    draw_flow_arrow(ax, 7, 15.1, 7, 14.7)
    draw_flow_arrow(ax, 7, 14.0, 7, 13.7)

    # Grace energy check
    draw_flow_arrow(ax, 7, 12.6, 7, 12.3, '', '#00FFFF')
    draw_flow_arrow(ax, 3.5, 13.15, 3.0, 13.15, 'YES', '#00FFFF')
    draw_flow_arrow(ax, 3.0, 13.15, 3.0, 13.05)
    draw_flow_arrow(ax, 7, 11.2, 7, 10.9, 'NO', '#8b949e')

    # Taumoeba viable
    draw_flow_arrow(ax, 3.5, 11.75, 3.0, 11.75, 'YES', '#3fb950')
    draw_flow_arrow(ax, 3.0, 11.75, 3.0, 11.65)
    draw_flow_arrow(ax, 7, 9.8, 7, 9.55, 'NO', '#8b949e')

    # Enough samples
    draw_flow_arrow(ax, 3.5, 10.35, 3.0, 10.35, 'YES', '#3fb950')
    draw_flow_arrow(ax, 3.0, 10.35, 3.0, 10.25)
    draw_flow_arrow(ax, 7, 8.5, 7, 8.25, 'NO', '#8b949e')

    # On planet
    draw_flow_arrow(ax, 3.5, 9.0, 3.0, 9.0, 'YES', '#228B22')
    draw_flow_arrow(ax, 3.0, 9.0, 3.0, 8.95)
    draw_flow_arrow(ax, 7, 7.5, 7, 7.2, 'NO', '#8b949e')

    draw_flow_arrow(ax, 7, 7.5, 7, 7.2)
    draw_flow_arrow(ax, 7, 6.5, 7, 6.2)
    draw_flow_arrow(ax, 7, 5.5, 7, 5.2)
    draw_flow_arrow(ax, 7, 4.5, 7, 4.2)

    # Check conditions
    draw_flow_arrow(ax, 10.5, 3.8, 10.5, 3.8, 'YES', '#3fb950')
    draw_flow_arrow(ax, 7, 3.4, 7, 3.0, 'NO', '#8b949e')
    draw_flow_arrow(ax, 10.5, 2.6, 10.5, 2.6, 'YES', '#f85149')
    draw_flow_arrow(ax, 7, 2.2, 7, 1.9, 'NO', '#8b949e')
    draw_flow_arrow(ax, 7, 1.0, 7, 0.7, 'YES', '#f0883e')

    # Loop back arrow
    ax.annotate(
        '',
        xy=(13.5, 14.35), xytext=(13.5, 1.45),
        arrowprops=dict(
            arrowstyle='->', color='#f0883e', lw=1.5
        )
    )
    ax.plot([7, 13.5], [1.45, 1.45],
            color='#f0883e', lw=1.5)
    ax.plot([13.5, 13.5], [1.45, 14.35],
            color='#f0883e', lw=1.5)
    ax.plot([13.5, 9.5], [14.35, 14.35],
            color='#f0883e', lw=1.5)
    ax.text(13.7, 8.0, 'NO\n(next turn)',
            color='#f0883e', fontsize=7)

    plt.tight_layout()
    plt.savefig(
        'diagram_flowchart.png',
        facecolor='#0d1117',
        bbox_inches='tight',
        dpi=150
    )
    print("Flowchart saved as 'diagram_flowchart.png'")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


def draw_architecture():
    """Generate System Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(8, 9.6,
            'Project Hail Mary — System Architecture',
            color='white', fontsize=16,
            fontweight='bold', ha='center')

    def draw_component(ax, x, y, w, h,
                       title, items, color):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.15",
            facecolor='#161b22',
            edgecolor=color,
            linewidth=2.5
        )
        ax.add_patch(box)

        # Title bar
        title_bar = FancyBboxPatch(
            (x, y + h - 0.5), w, 0.5,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor=color,
            linewidth=1,
            alpha=0.9
        )
        ax.add_patch(title_bar)

        ax.text(x + w/2, y + h - 0.25,
                title, color='white',
                fontsize=9, fontweight='bold',
                ha='center', va='center')

        item_y = y + h - 0.8
        for item in items:
            ax.text(x + 0.2, item_y,
                    f'• {item}',
                    color='#c9d1d9',
                    fontsize=7.5, va='center')
            item_y -= 0.35

    def draw_arch_arrow(ax, x1, y1, x2, y2,
                        label='', color='#8b949e',
                        style='->'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle=style,
                color=color, lw=1.5
            )
        )
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(mx, my + 0.15, label,
                    color=color, fontsize=7,
                    ha='center',
                    bbox=dict(
                        facecolor='#0d1117',
                        edgecolor='none',
                        alpha=0.7
                    ))

    # Main simulation engine
    draw_component(
        ax, 5.5, 6.5, 5, 2.8,
        'SIMULATION ENGINE',
        ['Main simulation loop',
         'Turn-based step() function',
         'Win/lose condition checking',
         'Mission protocol enforcement',
         'Beetle probe management'],
        '#f0883e'
    )

    # Environment
    draw_component(
        ax, 0.3, 6.5, 4.5, 2.8,
        'ENVIRONMENT',
        ['20x20 procedural grid',
         'Astrophage spread system',
         'Hazard zones',
         'Time dilation zones',
         'Xenonite tunnel'],
        '#58a6ff'
    )

    # Grace agent
    draw_component(
        ax, 0.3, 2.5, 4.5, 3.5,
        'GRACE AGENT',
        ['Priority-based AI decisions',
         'Online learning weights',
         'EVA and tunnel travel',
         'Taumoeba experiments',
         'Beetle probe deployment',
         'Flashback events'],
        '#00FFFF'
    )

    # Rocky agent
    draw_component(
        ax, 11.2, 2.5, 4.5, 3.5,
        'ROCKY AGENT',
        ['Sonar communication',
         'Progressive trust system',
         'Fuel transfer mechanic',
         'Ship repairs',
         'Reconnaissance scanning',
         'Contamination system'],
        '#FF69B4'
    )

    # Taumoeba
    draw_component(
        ax, 5.5, 2.5, 5, 3.5,
        'TAUMOEBA SYSTEM',
        ['Earth strain breeding',
         'Erid strain breeding',
         'Procedural mutation rates',
         'Astrophage consumption',
         'Resistance mechanic',
         'Generation tracking'],
        '#3fb950'
    )

    # Visualiser
    draw_component(
        ax, 11.2, 6.5, 4.5, 2.8,
        'VISUALISER',
        ['Live 20x20 grid display',
         'Real-time stats panel',
         'Earth/Erid viability bars',
         'Mission result screen',
         'Matplotlib TkAgg backend'],
        '#9400D3'
    )

    # Statistics
    draw_component(
        ax, 0.3, 0.2, 15.4, 1.8,
        'STATISTICS ENGINE (run_statistics.py)',
        ['20 simulation runs | Success rate tracking | '
         'Knowledge score analysis | '
         'Taumoeba survival rates | '
         'Professional matplotlib graphs'],
        '#d29922'
    )

    # Arrows
    draw_arch_arrow(ax, 5.5, 8.0, 4.8, 8.0,
                    'reads', '#58a6ff')
    draw_arch_arrow(ax, 10.5, 8.0, 11.2, 8.0,
                    'updates', '#9400D3')
    draw_arch_arrow(ax, 7.5, 6.5, 5.5, 6.0,
                    'controls', '#00FFFF')
    draw_arch_arrow(ax, 9.0, 6.5, 10.5, 6.0,
                    'controls', '#FF69B4')
    draw_arch_arrow(ax, 8.0, 6.5, 8.0, 6.0,
                    'manages', '#3fb950')
    draw_arch_arrow(ax, 2.5, 2.5, 2.5, 2.3,
                    '', '#00FFFF')
    draw_arch_arrow(ax, 8.0, 2.5, 8.0, 2.3,
                    '', '#3fb950')
    draw_arch_arrow(ax, 13.5, 2.5, 13.5, 2.3,
                    '', '#FF69B4')

    # Layer labels
    ax.text(0.1, 9.4, 'LAYER 1: CORE ENGINE',
            color='#f0883e', fontsize=8,
            fontweight='bold', style='italic')
    ax.text(0.1, 6.0, 'LAYER 2: AGENTS & ENTITIES',
            color='#58a6ff', fontsize=8,
            fontweight='bold', style='italic')
    ax.text(0.1, 2.1, 'LAYER 3: ANALYSIS',
            color='#d29922', fontsize=8,
            fontweight='bold', style='italic')

    plt.tight_layout()
    plt.savefig(
        'diagram_architecture.png',
        facecolor='#0d1117',
        bbox_inches='tight',
        dpi=150
    )
    print("Architecture diagram saved as "
          "'diagram_architecture.png'")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


if __name__ == "__main__":
    print("Generating diagrams...")
    draw_class_diagram()
    print("Class diagram done!")
    draw_flowchart()
    print("Flowchart done!")
    draw_architecture()
    print("Architecture done!")
    print("\nAll 3 diagrams saved as PNG files!")