import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch


def draw_class_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(28, 20))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f0f4f8')
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 20)
    ax.axis('off')

    ax.text(14, 19.4,
            'Project Hail Mary — Class Diagram',
            color='#1a1a2e', fontsize=22,
            fontweight='bold', ha='center')

    def draw_class_box(ax, x, y, w, h,
                       class_name, attributes,
                       methods, header_color,
                       border_color):
        shadow = FancyBboxPatch(
            (x + 0.1, y - 0.1), w, h,
            boxstyle="round,pad=0.15",
            facecolor='#bbbbbb',
            edgecolor='none',
            zorder=1
        )
        ax.add_patch(shadow)

        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.15",
            facecolor='white',
            edgecolor=border_color,
            linewidth=2.5,
            zorder=2
        )
        ax.add_patch(box)

        header = FancyBboxPatch(
            (x, y + h - 0.8), w, 0.8,
            boxstyle="round,pad=0.05",
            facecolor=header_color,
            edgecolor=border_color,
            linewidth=2,
            zorder=3
        )
        ax.add_patch(header)

        ax.text(x + w/2, y + h - 0.4,
                f'<<class>>  {class_name}',
                color='white', fontsize=11,
                fontweight='bold',
                ha='center', va='center',
                zorder=4)

        ax.text(x + 0.25, y + h - 1.1,
                'Attributes:',
                color='#555555', fontsize=8.5,
                style='italic', zorder=4)

        attr_y = y + h - 1.5
        for attr in attributes:
            ax.text(x + 0.35, attr_y,
                    attr,
                    color='#222222',
                    fontsize=9, va='center',
                    zorder=4)
            attr_y -= 0.38

        ax.plot([x + 0.1, x + w - 0.1],
                [attr_y + 0.15, attr_y + 0.15],
                color=border_color,
                linewidth=1.2, alpha=0.4,
                zorder=4, linestyle='--')

        ax.text(x + 0.25, attr_y - 0.1,
                'Methods:',
                color='#555555', fontsize=8.5,
                style='italic', zorder=4)

        meth_y = attr_y - 0.48
        for method in methods:
            ax.text(x + 0.35, meth_y,
                    method,
                    color='#1a5276',
                    fontsize=9, va='center',
                    fontweight='bold',
                    zorder=4)
            meth_y -= 0.38

    def arrow(ax, x1, y1, x2, y2,
              label='', color='#555555'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->', color=color,
                lw=2.0
            ),
            zorder=5
        )
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(mx, my + 0.2, label,
                    color=color, fontsize=9,
                    ha='center', style='italic',
                    fontweight='bold',
                    bbox=dict(
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.9, pad=2
                    ),
                    zorder=6)

    # SIMULATION
    draw_class_box(
        ax, 9, 12.5, 8, 6.5,
        'Simulation',
        ['- grace: Grace',
         '- rocky: Rocky',
         '- taumoeba: Taumoeba',
         '- environment: Environment',
         '- beetle_probes: list',
         '- turn: int',
         '- mission_success: bool',
         '- earth_saved: bool'],
        ['+ step()',
         '+ run(max_turns: int)',
         '+ run_text_only()',
         '+ _grace_action()',
         '+ _rocky_action()',
         '+ _deploy_probe()'],
        '#e67e22', '#d35400'
    )

    # ENVIRONMENT
    draw_class_box(
        ax, 0.5, 11.5, 7, 6.5,
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

    # CELL
    draw_class_box(
        ax, 0.5, 5.5, 7, 5.5,
        'Cell',
        ['- cell_type: str',
         '- astrophage_level: int',
         '- astrophage_resistance: int',
         '- has_taumoeba: bool',
         '- is_time_dilation: bool',
         '- agent: object'],
        ['+ __str__(): str'],
        '#2980b9', '#1a5276'
    )

    # GRACE
    draw_class_box(
        ax, 20, 11.0, 7.5, 7.5,
        'Grace',
        ['- health: int',
         '- energy: int',
         '- knowledge: int',
         '- taumoeba_samples: int',
         '- beetle_probes: int',
         '- strategy_weights: dict',
         '- equipment_damaged: bool'],
        ['+ move(dx, dy)',
         '+ collect_sample()',
         '+ conduct_experiment()',
         '+ deploy_beetle_probe()',
         '+ flashback()',
         '+ travel_tunnel()',
         '+ perform_eva()'],
        '#16a085', '#0e6655'
    )

    # ROCKY
    draw_class_box(
        ax, 20, 3.5, 7.5, 7.0,
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

    # TAUMOEBA
    draw_class_box(
        ax, 9, 3.5, 8, 7.5,
        'Taumoeba',
        ['- survival_rate_earth: float',
         '- survival_rate_erid: float',
         '- generation: int',
         '- mutation_rate: float',
         '- breeding_log: list',
         '- astrophage_consumed: int'],
        ['+ breed_for_earth()',
         '+ breed_for_erid()',
         '+ consume_astrophage()',
         '+ is_viable_earth(): bool',
         '+ is_viable_erid(): bool',
         '+ analyse()'],
        '#27ae60', '#1e8449'
    )

    # BEETLEPROBE
    draw_class_box(
        ax, 0.5, 0.3, 7, 4.8,
        'BeetleProbe',
        ['- name: str',
         '- knowledge_payload: int',
         '- data_integrity: int',
         '- reached_earth: bool',
         '- turns_in_flight: int'],
        ['+ navigate()',
         '+ configure(heading, payload)',
         '+ status()'],
        '#c0392b', '#922b21'
    )

    # Arrows
    arrow(ax, 9, 15.5, 7.5, 15.0,
          'uses', '#2980b9')
    arrow(ax, 17, 16.5, 20, 15.0,
          'controls', '#16a085')
    arrow(ax, 17, 14.0, 20, 8.0,
          'controls', '#8e44ad')
    arrow(ax, 13, 12.5, 13, 11.0,
          'manages', '#27ae60')
    arrow(ax, 9.5, 12.5, 7.5, 3.5,
          'deploys', '#c0392b')
    arrow(ax, 4, 11.5, 4, 11.0,
          'contains', '#2980b9')

    plt.tight_layout()
    plt.savefig(
        'diagram_classes.png',
        facecolor='white',
        bbox_inches='tight',
        dpi=180
    )
    print("Class diagram saved!")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


def draw_flowchart():
    fig, ax = plt.subplots(1, 1, figsize=(16, 26))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fa')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 26)
    ax.axis('off')

    ax.text(8, 25.4,
            'Project Hail Mary — Simulation Flowchart',
            color='#1a1a2e', fontsize=18,
            fontweight='bold', ha='center')

    def box(ax, x, y, w, h, text,
            bg='#d6eaf8', border='#2980b9',
            fontsize=10, bold=False):
        b = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.12",
            facecolor=bg,
            edgecolor=border,
            linewidth=2.2
        )
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text,
                color='#1a1a2e',
                fontsize=fontsize,
                ha='center', va='center',
                fontweight='bold' if bold else 'normal',
                multialignment='center')

    def diamond(ax, x, y, w, h, text,
                bg='#fef9e7', border='#e67e22',
                fontsize=10):
        d = plt.Polygon(
            [[x + w/2, y + h],
             [x + w, y + h/2],
             [x + w/2, y],
             [x, y + h/2]],
            facecolor=bg,
            edgecolor=border,
            linewidth=2.2
        )
        ax.add_patch(d)
        ax.text(x + w/2, y + h/2, text,
                color='#1a1a2e',
                fontsize=fontsize,
                ha='center', va='center',
                fontweight='bold',
                multialignment='center')

    def oval(ax, x, y, w, h, text, bg, border):
        e = mpatches.Ellipse(
            (x + w/2, y + h/2), w, h,
            facecolor=bg,
            edgecolor=border,
            linewidth=3
        )
        ax.add_patch(e)
        ax.text(x + w/2, y + h/2, text,
                color='white',
                fontsize=13,
                ha='center', va='center',
                fontweight='bold')

    def arr(ax, x1, y1, x2, y2,
            label='', color='#555555'):
        ax.annotate(
            '',
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->',
                color=color, lw=2.2
            )
        )
        if label:
            mx = (x1 + x2) / 2 + 0.2
            my = (y1 + y2) / 2
            ax.text(mx, my, label,
                    color=color,
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.9
                    ))

    # START
    oval(ax, 5, 24.3, 6, 1.0,
         'START', '#27ae60', '#1e8449')

    box(ax, 3, 22.8, 10, 1.1,
        'Initialise Simulation\n(Environment, Grace, Rocky, Taumoeba)',
        '#d6eaf8', '#2980b9')

    box(ax, 3, 21.4, 10, 1.1,
        'Grace wakes from coma\nKnowledge = 0,  No memory',
        '#d6eaf8', '#2980b9')

    box(ax, 3, 20.0, 10, 1.1,
        'Rocky encountered at Tau Ceti\nBegin sonar communication',
        '#e8daef', '#8e44ad')

    box(ax, 3.5, 18.7, 9, 1.0,
        'BEGIN TURN',
        '#fdebd0', '#e67e22', 12, True)

    diamond(ax, 3, 17.1, 10, 1.4,
            'Grace Energy < 15?',
            '#fef9e7', '#e67e22')

    box(ax, 0.2, 17.2, 2.5, 0.9,
        'Grace Rests\n+20 Energy',
        '#d5f5e3', '#27ae60', 9)

    diamond(ax, 3, 15.4, 10, 1.4,
            'Taumoeba Viable\nfor Earth?',
            '#fef9e7', '#e67e22')

    box(ax, 0.2, 15.5, 2.5, 0.9,
        'Deploy\nBeetle Probe',
        '#e8daef', '#8e44ad', 9)

    diamond(ax, 3, 13.7, 10, 1.4,
            'Samples >= 2\nand Knowledge >= 20?',
            '#fef9e7', '#e67e22')

    box(ax, 0.2, 13.8, 2.5, 0.9,
        'Breed\nTaumoeba',
        '#d5f5e3', '#27ae60', 9)

    diamond(ax, 3, 12.0, 10, 1.4,
            'Grace on\nPlanet Adrian?',
            '#fef9e7', '#e67e22')

    box(ax, 0.2, 12.1, 2.5, 0.9,
        'Collect\nSamples',
        '#d5f5e3', '#27ae60', 9)

    box(ax, 3, 10.8, 10, 0.9,
        'Move Toward Planet Adrian  (Avoid Astrophage hazards)',
        '#d6eaf8', '#2980b9')

    box(ax, 3, 9.6, 10, 0.9,
        'Rocky Actions:  Communicate, Share Knowledge, Assist, Repair',
        '#e8daef', '#8e44ad')

    box(ax, 3, 8.4, 10, 0.9,
        'Environment Update:  Spread Astrophage  +  Equipment Failures',
        '#fadbd8', '#c0392b')

    box(ax, 3, 7.2, 10, 0.9,
        'Navigate Beetle Probes  —  Check if reached Earth',
        '#e8daef', '#8e44ad')

    diamond(ax, 3, 5.6, 10, 1.4,
            'Mission Success?\n(Earth saved + Probe reached Earth)',
            '#d5f5e3', '#27ae60')

    box(ax, 13.3, 5.8, 2.5, 0.9,
        'MISSION\nSUCCESS!',
        '#a9dfbf', '#27ae60', 9, True)

    diamond(ax, 3, 4.0, 10, 1.4,
            'Mission Aborted?\n(Grace health or energy = 0)',
            '#fadbd8', '#c0392b')

    box(ax, 13.3, 4.2, 2.5, 0.9,
        'MISSION\nFAILED',
        '#f5b7b1', '#c0392b', 9, True)

    diamond(ax, 3, 2.3, 10, 1.4,
            'Turn >= Max Turns?',
            '#fef9e7', '#e67e22')

    oval(ax, 5, 0.5, 6, 1.0,
         'END', '#c0392b', '#922b21')

    # Arrows
    arr(ax, 8, 24.3, 8, 23.9)
    arr(ax, 8, 22.8, 8, 22.5)
    arr(ax, 8, 21.4, 8, 21.1)
    arr(ax, 8, 20.0, 8, 19.7)
    arr(ax, 8, 18.7, 8, 18.5)

    arr(ax, 3, 17.8, 2.7, 17.8, 'YES', '#27ae60')
    arr(ax, 8, 17.1, 8, 16.8, 'NO', '#c0392b')

    arr(ax, 3, 16.1, 2.7, 16.1, 'YES', '#27ae60')
    arr(ax, 8, 15.4, 8, 15.1, 'NO', '#c0392b')

    arr(ax, 3, 14.4, 2.7, 14.4, 'YES', '#27ae60')
    arr(ax, 8, 13.7, 8, 13.4, 'NO', '#c0392b')

    arr(ax, 3, 12.7, 2.7, 12.7, 'YES', '#27ae60')
    arr(ax, 8, 12.0, 8, 11.7, 'NO', '#c0392b')

    arr(ax, 8, 10.8, 8, 10.5)
    arr(ax, 8, 9.6, 8, 9.3)
    arr(ax, 8, 8.4, 8, 8.1)
    arr(ax, 8, 7.2, 8, 7.0)

    arr(ax, 13, 6.3, 13.3, 6.3, 'YES', '#27ae60')
    arr(ax, 8, 5.6, 8, 5.4, 'NO', '#555555')
    arr(ax, 13, 4.7, 13.3, 4.7, 'YES', '#c0392b')
    arr(ax, 8, 4.0, 8, 3.7, 'NO', '#555555')
    arr(ax, 8, 2.3, 8, 1.5, 'YES', '#e67e22')

    ax.plot([8, 15.2], [1.5, 1.5],
            color='#e67e22', lw=2.2)
    ax.plot([15.2, 15.2], [1.5, 19.2],
            color='#e67e22', lw=2.2)
    ax.plot([15.2, 12.5], [19.2, 19.2],
            color='#e67e22', lw=2.2)
    ax.annotate(
        '',
        xy=(12.5, 19.2), xytext=(15.2, 19.2),
        arrowprops=dict(
            arrowstyle='->', color='#e67e22', lw=2.2
        )
    )
    ax.text(15.4, 10.0, 'NO\n(next\nturn)',
            color='#e67e22', fontsize=9,
            fontweight='bold')

    plt.tight_layout()
    plt.savefig(
        'diagram_flowchart.png',
        facecolor='white',
        bbox_inches='tight',
        dpi=180
    )
    print("Flowchart saved!")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


def draw_architecture():
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
        shadow = FancyBboxPatch(
            (x + 0.07, y - 0.07), w, h,
            boxstyle="round,pad=0.15",
            facecolor='#cccccc',
            edgecolor='none',
            zorder=1
        )
        ax.add_patch(shadow)

        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.15",
            facecolor='white',
            edgecolor=border_color,
            linewidth=2.5,
            zorder=2
        )
        ax.add_patch(box)

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

    ax.text(0.3, 10.8, 'LAYER 1: CORE ENGINE',
            color='#e67e22', fontsize=9,
            fontweight='bold', style='italic')
    ax.text(0.3, 6.5, 'LAYER 2: AGENTS & ENTITIES',
            color='#2980b9', fontsize=9,
            fontweight='bold', style='italic')
    ax.text(0.3, 2.3, 'LAYER 3: ANALYSIS & OUTPUT',
            color='#8e44ad', fontsize=9,
            fontweight='bold', style='italic')

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
    print("Generating diagrams...")
    draw_class_diagram()
    print("Class diagram done!")
    draw_flowchart()
    print("Flowchart done!")
    draw_architecture()
    print("Architecture done!")
    print("\nAll 3 diagrams saved!")