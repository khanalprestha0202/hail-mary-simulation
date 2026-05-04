import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe


def draw_class_diagram():
    """Generate Clean Light Class Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(22, 16))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fa')
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.axis('off')

    ax.text(11, 15.5,
            'Project Hail Mary — Class Diagram',
            color='#1a1a2e', fontsize=18,
            fontweight='bold', ha='center',
            fontfamily='sans-serif')

    def draw_class_box(ax, x, y, width, height,
                       class_name, attributes, methods,
                       header_color, border_color):
        # Shadow
        shadow = FancyBboxPatch(
            (x + 0.08, y - 0.08), width, height,
            boxstyle="round,pad=0.1",
            facecolor='#cccccc',
            edgecolor='none',
            linewidth=0,
            zorder=1
        )
        ax.add_patch(shadow)

        # Main box
        box = FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.1",
            facecolor='white',
            edgecolor=border_color,
            linewidth=2,
            zorder=2
        )
        ax.add_patch(box)

        # Header
        header = FancyBboxPatch(
            (x, y + height - 0.65), width, 0.65,
            boxstyle="round,pad=0.05",
            facecolor=header_color,
            edgecolor=border_color,
            linewidth=2,
            zorder=3
        )
        ax.add_patch(header)

        # Class name
        ax.text(x + width/2, y + height - 0.32,
                class_name,
                color='white', fontsize=10,
                fontweight='bold', ha='center',
                va='center', zorder=4)

        # Divider line attributes/methods
        mid_y = y + height - 0.65
        attr_start = mid_y - 0.35
        for attr in attributes:
            ax.text(x + 0.2, attr_start,
                    attr, color='#333333',
                    fontsize=7.5, va='center', zorder=4)
            attr_start -= 0.3

        # Divider line
        div_y = attr_start + 0.1
        ax.plot([x + 0.1, x + width - 0.1],
                [div_y, div_y],
                color=border_color,
                linewidth=1, alpha=0.5, zorder=4)

        # Methods
        method_start = div_y - 0.28
        for method in methods:
            ax.text(x + 0.2, method_start,
                    method, color='#1a5276',
                    fontsize=7.5, va='center',
                    fontweight='bold', zorder=4)
            method_start -= 0.3

    def draw_arrow(ax, x1, y1, x2, y2,
                   label='', color='#555555'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=color,
                lw=1.8,
                connectionstyle='arc3,rad=0.0'
            ),
            zorder=5
        )
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(mx + 0.1, my + 0.15, label,
                    color=color, fontsize=8,
                    ha='center', style='italic',
                    bbox=dict(
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.8,
                        pad=1
                    ),
                    zorder=6)

    # Simulation (centre top)
    draw_class_box(
        ax, 7.5, 10.0, 6, 5.0,
        'Simulation',
        ['- grace: Grace',
         '- rocky: Rocky',
         '- taumoeba: Taumoeba',
         '- environment: Environment',
         '- beetle_probes: list',
         '- turn: int',
         '- mission_success: bool',
         '- earth_saved: bool',
         '- erid_saved: bool'],
        ['+ step()',
         '+ run(max_turns)',
         '+ run_text_only()',
         '+ _grace_action()',
         '+ _rocky_action()',
         '+ _deploy_probe()'],
        '#e67e22', '#d35400'
    )

    # Environment (left)
    draw_class_box(
        ax, 0.3, 9.5, 5, 4.5,
        'Environment',
        ['- width: int = 20',
         '- height: int = 20',
         '- grid: Cell[][]',
         '- turn: int',
         '- taumoeba_deployed: int'],
        ['+ setup_world()',
         '+ spread_astrophage()',
         '+ get_cell(x, y)',
         '+ apply_taumoeba_resistance()',
         '+ trigger_equipment_failure()',
         '+ display()'],
        '#2980b9', '#1a5276'
    )

    # Cell (bottom left)
    draw_class_box(
        ax, 0.3, 5.5, 5, 3.5,
        'Cell',
        ['- cell_type: str',
         '- astrophage_level: int',
         '- astrophage_resistance: int',
         '- has_taumoeba: bool',
         '- is_time_dilation: bool'],
        ['+ __str__(): str'],
        '#2980b9', '#1a5276'
    )

    # Grace (right)
    draw_class_box(
        ax, 16.5, 9.0, 5.2, 5.5,
        'Grace',
        ['- health: int',
         '- energy: int',
         '- knowledge: int',
         '- taumoeba_samples: int',
         '- beetle_probes: int',
         '- strategy_weights: dict',
         '- experiment_history: dict',
         '- equipment_damaged: bool'],
        ['+ move()',
         '+ collect_sample()',
         '+ conduct_experiment()',
         '+ deploy_beetle_probe()',
         '+ flashback()',
         '+ travel_tunnel()',
         '+ perform_eva()'],
        '#16a085', '#0e6655'
    )

    # Rocky (far right bottom)
    draw_class_box(
        ax, 16.5, 4.0, 5.2, 4.5,
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
        '#8e44ad', '#6c3483'
    )

    # Taumoeba (bottom centre)
    draw_class_box(
        ax, 7.5, 4.5, 6, 4.5,
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
        '#27ae60', '#1e8449'
    )

    # BeetleProbe (bottom far left)
    draw_class_box(
        ax, 0.3, 1.0, 5, 4.0,
        'BeetleProbe',
        ['- name: str',
         '- knowledge_payload: int',
         '- data_integrity: int',
         '- reached_earth: bool',
         '- turns_in_flight: int'],
        ['+ navigate()',
         '+ configure()',
         '+ status()'],
        '#c0392b', '#922b21'
    )

    # Arrows
    draw_arrow(ax, 7.5, 12.5, 5.3, 12.0,
               'uses', '#2980b9')
    draw_arrow(ax, 13.5, 13.5, 16.5, 12.5,
               'controls', '#16a085')
    draw_arrow(ax, 13.5, 11.5, 16.5, 7.0,
               'controls', '#8e44ad')
    draw_arrow(ax, 10.5, 10.0, 10.5, 9.0,
               'manages', '#27ae60')
    draw_arrow(ax, 7.5, 11.0, 5.3, 3.5,
               'deploys', '#c0392b')
    draw_arrow(ax, 2.8, 9.5, 2.8, 9.0,
               'contains', '#2980b9')

    plt.tight_layout()
    plt.savefig(
        'diagram_classes.png',
        facecolor='white',
        bbox_inches='tight',
        dpi=200
    )
    print("Class diagram saved!")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


def draw_flowchart():
    """Generate Clean Light Flowchart"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 22))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fa')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 22)
    ax.axis('off')

    ax.text(7, 21.5,
            'Project Hail Mary — Simulation Flowchart',
            color='#1a1a2e', fontsize=16,
            fontweight='bold', ha='center')

    def draw_rect(ax, x, y, w, h, text,
                  bg='#d6eaf8', border='#2980b9',
                  fontsize=8, text_color='#1a1a2e'):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1",
            facecolor=bg,
            edgecolor=border,
            linewidth=2
        )
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text,
                color=text_color,
                fontsize=fontsize,
                ha='center', va='center',
                fontweight='bold',
                wrap=True)

    def draw_diamond(ax, x, y, w, h, text,
                     bg='#fef9e7', border='#f39c12',
                     fontsize=8):
        diamond = plt.Polygon(
            [[x + w/2, y + h],
             [x + w, y + h/2],
             [x + w/2, y],
             [x, y + h/2]],
            facecolor=bg,
            edgecolor=border,
            linewidth=2
        )
        ax.add_patch(diamond)
        ax.text(x + w/2, y + h/2, text,
                color='#1a1a2e',
                fontsize=fontsize,
                ha='center', va='center',
                fontweight='bold')

    def draw_oval(ax, x, y, w, h, text, bg, border):
        ellipse = mpatches.Ellipse(
            (x + w/2, y + h/2), w, h,
            facecolor=bg,
            edgecolor=border,
            linewidth=2.5
        )
        ax.add_patch(ellipse)
        ax.text(x + w/2, y + h/2, text,
                color='white',
                fontsize=10,
                ha='center', va='center',
                fontweight='bold')

    def arrow(ax, x1, y1, x2, y2,
              label='', color='#555555'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=color,
                lw=2
            )
        )
        if label:
            mx = (x1 + x2) / 2 + 0.2
            my = (y1 + y2) / 2
            ax.text(mx, my, label,
                    color=color, fontsize=8,
                    fontweight='bold',
                    bbox=dict(
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.9
                    ))

    # START
    draw_oval(ax, 4.5, 20.5, 5, 0.8,
              'START', '#27ae60', '#1e8449')

    # Init
    draw_rect(ax, 3.5, 19.3, 7, 0.9,
              'Initialise Simulation\n(Environment, Grace, Rocky, Taumoeba)',
              '#d6eaf8', '#2980b9')

    # Grace wakes
    draw_rect(ax, 3.5, 18.1, 7, 0.9,
              'Grace wakes from coma\nKnowledge = 0, No memory',
              '#d6eaf8', '#2980b9')

    # Rocky encountered
    draw_rect(ax, 3.5, 16.9, 7, 0.9,
              'Rocky encountered at Tau Ceti\nBegin sonar communication',
              '#e8daef', '#8e44ad')

    # Begin turn
    draw_rect(ax, 4.0, 15.8, 6, 0.8,
              'BEGIN TURN',
              '#fdebd0', '#e67e22', 10, '#7d3c00')

    # Grace energy check
    draw_diamond(ax, 3.5, 14.4, 7, 1.1,
                 'Grace Energy < 15?')

    # Rest box
    draw_rect(ax, 0.3, 14.5, 2.8, 0.7,
              'Grace Rests\n+20 Energy',
              '#d5f5e3', '#27ae60')

    # Taumoeba viable?
    draw_diamond(ax, 3.5, 13.0, 7, 1.1,
                 'Taumoeba Viable\nfor Earth?',
                 '#fef9e7', '#f39c12')

    # Deploy probe
    draw_rect(ax, 0.3, 13.1, 2.8, 0.7,
              'Deploy\nBeetle Probe',
              '#e8daef', '#8e44ad')

    # Enough samples?
    draw_diamond(ax, 3.5, 11.6, 7, 1.1,
                 'Samples >= 2\nand Knowledge >= 20?',
                 '#fef9e7', '#f39c12')

    # Breed
    draw_rect(ax, 0.3, 11.7, 2.8, 0.7,
              'Breed\nTaumoeba',
              '#d5f5e3', '#27ae60')

    # On planet?
    draw_diamond(ax, 3.5, 10.2, 7, 1.1,
                 'Grace on\nPlanet Adrian?',
                 '#fef9e7', '#f39c12')

    # Collect
    draw_rect(ax, 0.3, 10.3, 2.8, 0.7,
              'Collect\nSamples',
              '#d5f5e3', '#27ae60')

    # Move
    draw_rect(ax, 3.5, 9.1, 7, 0.8,
              'Move Toward Planet Adrian\n(Avoid Astrophage hazards)',
              '#d6eaf8', '#2980b9')

    # Rocky action
    draw_rect(ax, 3.5, 8.0, 7, 0.8,
              'Rocky Actions:\nCommunicate, Share, Assist, Repair',
              '#e8daef', '#8e44ad')

    # Environment update
    draw_rect(ax, 3.5, 6.9, 7, 0.8,
              'Environment Update:\nSpread Astrophage + Equipment Failures',
              '#fadbd8', '#c0392b')

    # Navigate probes
    draw_rect(ax, 3.5, 5.8, 7, 0.8,
              'Navigate Beetle Probes\nCheck if reached Earth',
              '#e8daef', '#8e44ad')

    # Mission success?
    draw_diamond(ax, 3.5, 4.4, 7, 1.1,
                 'Mission Success?\n(Earth saved + Probe reached Earth)',
                 '#d5f5e3', '#27ae60')

    # Success box
    draw_rect(ax, 11.0, 4.5, 2.8, 0.7,
              'MISSION\nSUCCESS!',
              '#d5f5e3', '#27ae60',
              text_color='#1e8449')

    # Aborted?
    draw_diamond(ax, 3.5, 3.0, 7, 1.1,
                 'Mission Aborted?\n(Grace health/energy = 0)',
                 '#fadbd8', '#c0392b')

    # Failed box
    draw_rect(ax, 11.0, 3.1, 2.8, 0.7,
              'MISSION\nFAILED',
              '#fadbd8', '#c0392b',
              text_color='#922b21')

    # Max turns?
    draw_diamond(ax, 3.5, 1.6, 7, 1.1,
                 'Turn >= Max Turns?',
                 '#fef9e7', '#f39c12')

    # END
    draw_oval(ax, 4.5, 0.3, 5, 0.8,
              'END', '#c0392b', '#922b21')

    # Main flow arrows
    arrow(ax, 7, 20.5, 7, 20.2)
    arrow(ax, 7, 19.3, 7, 19.0)
    arrow(ax, 7, 18.1, 7, 17.8)
    arrow(ax, 7, 16.9, 7, 16.6)
    arrow(ax, 7, 15.8, 7, 15.5)

    # Energy check arrows
    arrow(ax, 3.5, 14.95, 3.1, 14.95,
          'YES', '#27ae60')
    arrow(ax, 3.1, 14.95, 3.1, 14.85)
    arrow(ax, 7, 14.4, 7, 14.1, 'NO', '#c0392b')

    # Viable arrows
    arrow(ax, 3.5, 13.55, 3.1, 13.55,
          'YES', '#27ae60')
    arrow(ax, 3.1, 13.55, 3.1, 13.45)
    arrow(ax, 7, 13.0, 7, 12.7, 'NO', '#c0392b')

    # Samples arrows
    arrow(ax, 3.5, 12.15, 3.1, 12.15,
          'YES', '#27ae60')
    arrow(ax, 3.1, 12.15, 3.1, 12.05)
    arrow(ax, 7, 11.6, 7, 11.3, 'NO', '#c0392b')

    # Planet arrows
    arrow(ax, 3.5, 10.75, 3.1, 10.75,
          'YES', '#27ae60')
    arrow(ax, 3.1, 10.75, 3.1, 10.65)
    arrow(ax, 7, 10.2, 7, 9.9, 'NO', '#c0392b')

    arrow(ax, 7, 9.1, 7, 8.8)
    arrow(ax, 7, 8.0, 7, 7.7)
    arrow(ax, 7, 6.9, 7, 6.6)
    arrow(ax, 7, 5.8, 7, 5.5)

    # Condition arrows
    arrow(ax, 10.5, 4.95, 11.0, 4.85,
          'YES', '#27ae60')
    arrow(ax, 7, 4.4, 7, 4.1, 'NO', '#c0392b')
    arrow(ax, 10.5, 3.55, 11.0, 3.45,
          'YES', '#c0392b')
    arrow(ax, 7, 3.0, 7, 2.7, 'NO', '#555555')
    arrow(ax, 7, 1.6, 7, 1.1, 'YES', '#f39c12')

    # Loop back
    ax.annotate(
        '',
        xy=(13.5, 16.2), xytext=(13.5, 1.8),
        arrowprops=dict(
            arrowstyle='->', color='#f39c12', lw=2
        )
    )
    ax.plot([7, 13.5], [1.8, 1.8],
            color='#f39c12', lw=2)
    ax.plot([13.5, 13.5], [1.8, 16.2],
            color='#f39c12', lw=2)
    ax.plot([13.5, 10.0], [16.2, 16.2],
            color='#f39c12', lw=2)
    ax.text(13.7, 9.0, 'NO\n(next\nturn)',
            color='#f39c12', fontsize=8,
            fontweight='bold')

    plt.tight_layout()
    plt.savefig(
        'diagram_flowchart.png',
        facecolor='white',
        bbox_inches='tight',
        dpi=200
    )
    print("Flowchart saved!")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


def draw_architecture():
    """Generate Clean Light Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fa')
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')

    ax.text(9, 11.6,
            'Project Hail Mary — System Architecture',
            color='#1a1a2e', fontsize=18,
            fontweight='bold', ha='center')

    def draw_component(ax, x, y, w, h,
                       title, items,
                       header_color, border_color):
        # Shadow
        shadow = FancyBboxPatch(
            (x + 0.07, y - 0.07), w, h,
            boxstyle="round,pad=0.15",
            facecolor='#cccccc',
            edgecolor='none',
            zorder=1
        )
        ax.add_patch(shadow)

        # Box
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.15",
            facecolor='white',
            edgecolor=border_color,
            linewidth=2.5,
            zorder=2
        )
        ax.add_patch(box)

        # Header bar
        header = FancyBboxPatch(
            (x, y + h - 0.7), w, 0.7,
            boxstyle="round,pad=0.05",
            facecolor=header_color,
            edgecolor=border_color,
            linewidth=2,
            zorder=3
        )
        ax.add_patch(header)

        ax.text(x + w/2, y + h - 0.35,
                title, color='white',
                fontsize=10, fontweight='bold',
                ha='center', va='center', zorder=4)

        item_y = y + h - 1.1
        for item in items:
            ax.text(x + 0.25, item_y,
                    f'• {item}',
                    color='#333333',
                    fontsize=8, va='center', zorder=4)
            item_y -= 0.38

    def draw_arch_arrow(ax, x1, y1, x2, y2,
                        label='', color='#555555'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=color,
                lw=2
            )
        )
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(mx, my + 0.15, label,
                    color=color, fontsize=8,
                    ha='center', fontweight='bold',
                    bbox=dict(
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.9
                    ))

    # Layer labels
    ax.text(0.3, 10.8, 'LAYER 1: CORE ENGINE',
            color='#e67e22', fontsize=9,
            fontweight='bold', style='italic')
    ax.text(0.3, 6.5, 'LAYER 2: AGENTS & ENTITIES',
            color='#2980b9', fontsize=9,
            fontweight='bold', style='italic')
    ax.text(0.3, 2.3, 'LAYER 3: ANALYSIS & OUTPUT',
            color='#8e44ad', fontsize=9,
            fontweight='bold', style='italic')

    # Layer 1 backgrounds
    layer1_bg = FancyBboxPatch(
        (0.2, 7.0), 17.6, 3.6,
        boxstyle="round,pad=0.1",
        facecolor='#fef9e7',
        edgecolor='#f39c12',
        linewidth=1.5,
        alpha=0.4,
        zorder=0
    )
    ax.add_patch(layer1_bg)

    layer2_bg = FancyBboxPatch(
        (0.2, 2.7), 17.6, 4.1,
        boxstyle="round,pad=0.1",
        facecolor='#eaf2ff',
        edgecolor='#2980b9',
        linewidth=1.5,
        alpha=0.4,
        zorder=0
    )
    ax.add_patch(layer2_bg)

    layer3_bg = FancyBboxPatch(
        (0.2, 0.3), 17.6, 2.2,
        boxstyle="round,pad=0.1",
        facecolor='#f5eef8',
        edgecolor='#8e44ad',
        linewidth=1.5,
        alpha=0.4,
        zorder=0
    )
    ax.add_patch(layer3_bg)

    # ENVIRONMENT
    draw_component(
        ax, 0.5, 7.3, 5.2, 3.0,
        'ENVIRONMENT',
        ['20x20 procedural grid',
         'Astrophage spread system',
         'Hazard + time dilation zones',
         'Petrova line',
         'Xenonite tunnel'],
        '#2980b9', '#1a5276'
    )

    # SIMULATION ENGINE
    draw_component(
        ax, 6.4, 7.3, 5.2, 3.0,
        'SIMULATION ENGINE',
        ['Turn-based step() loop',
         'Priority AI decisions',
         'Win/lose conditions',
         'Mission protocol',
         'Equipment failure events'],
        '#e67e22', '#d35400'
    )

    # VISUALISER
    draw_component(
        ax, 12.3, 7.3, 5.2, 3.0,
        'VISUALISER',
        ['Live 20x20 grid display',
         'Real-time stats panel',
         'Earth/Erid viability bars',
         'Mission result screen',
         'matplotlib TkAgg backend'],
        '#16a085', '#0e6655'
    )

    # GRACE AGENT
    draw_component(
        ax, 0.5, 2.9, 5.2, 3.3,
        'GRACE AGENT',
        ['Priority-based AI decisions',
         'Online learning weights',
         'EVA and tunnel travel',
         'Taumoeba experiments',
         'Beetle probe deployment',
         'Flashback events'],
        '#2ecc71', '#1e8449'
    )

    # TAUMOEBA SYSTEM
    draw_component(
        ax, 6.4, 2.9, 5.2, 3.3,
        'TAUMOEBA SYSTEM',
        ['Earth strain breeding',
         'Erid strain breeding',
         'Procedural mutation rates',
         'Astrophage consumption',
         'Resistance mechanic',
         'Generation tracking'],
        '#27ae60', '#1a7a42'
    )

    # ROCKY AGENT
    draw_component(
        ax, 12.3, 2.9, 5.2, 3.3,
        'ROCKY AGENT',
        ['Sonar communication',
         'Progressive trust system',
         'Fuel transfer mechanic',
         'Ship repairs',
         'Reconnaissance scanning',
         'Contamination system'],
        '#8e44ad', '#6c3483'
    )

    # STATISTICS ENGINE
    draw_component(
        ax, 0.5, 0.4, 17.0, 1.8,
        'STATISTICS ENGINE  (run_statistics.py)',
        ['20 simulation runs  |  '
         'Success rate tracking  |  '
         'Knowledge score analysis  |  '
         'Taumoeba survival rates  |  '
         'Professional matplotlib graphs'],
        '#e74c3c', '#c0392b'
    )

    # Arrows
    draw_arch_arrow(ax, 5.7, 8.8, 6.4, 8.8,
                    'reads', '#2980b9')
    draw_arch_arrow(ax, 11.6, 8.8, 12.3, 8.8,
                    'updates', '#16a085')
    draw_arch_arrow(ax, 8.0, 7.3, 4.0, 6.2,
                    'controls', '#2ecc71')
    draw_arch_arrow(ax, 9.0, 7.3, 9.0, 6.2,
                    'manages', '#27ae60')
    draw_arch_arrow(ax, 10.0, 7.3, 14.0, 6.2,
                    'controls', '#8e44ad')
    draw_arch_arrow(ax, 3.0, 2.9, 3.0, 2.2)
    draw_arch_arrow(ax, 9.0, 2.9, 9.0, 2.2)
    draw_arch_arrow(ax, 15.0, 2.9, 15.0, 2.2)

    plt.tight_layout()
    plt.savefig(
        'diagram_architecture.png',
        facecolor='white',
        bbox_inches='tight',
        dpi=200
    )
    print("Architecture diagram saved!")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


if __name__ == "__main__":
    print("Generating clean diagrams...")
    draw_class_diagram()
    print("Class diagram done!")
    draw_flowchart()
    print("Flowchart done!")
    draw_architecture()
    print("Architecture done!")
    print("\nAll 3 diagrams saved!")