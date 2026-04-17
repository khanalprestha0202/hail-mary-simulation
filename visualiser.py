import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import ListedColormap


class Visualiser:
    def __init__(self, environment, grace, rocky):
        self.environment = environment
        self.grace = grace
        self.rocky = rocky
        self.closed = False
        plt.ion()
        self.fig, self.axes = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.patch.set_facecolor('#0a0a2e')
        self.fig.suptitle(
            'Project Hail Mary Simulation',
            color='white', fontsize=16, fontweight='bold'
        )
        self.fig.canvas.mpl_connect(
            'close_event', self._on_close
        )

    def _on_close(self, event):
        self.closed = True

    def draw_grid(self, turn):
        ax = self.axes[0]
        ax.clear()
        ax.set_facecolor('#0a0a2e')

        grid_data = np.zeros((
            self.environment.height,
            self.environment.width
        ))

        for x in range(self.environment.height):
            for y in range(self.environment.width):
                cell = self.environment.grid[x][y]
                if cell.cell_type == "hail_mary":
                    grid_data[x][y] = 5
                elif cell.cell_type == "blip_a":
                    grid_data[x][y] = 6
                elif cell.cell_type == "planet":
                    grid_data[x][y] = 4
                elif cell.cell_type == "tunnel":
                    grid_data[x][y] = 10
                elif cell.cell_type == "hazard":
                    grid_data[x][y] = 7
                elif cell.is_time_dilation:
                    grid_data[x][y] = 11
                elif cell.astrophage_level > 6:
                    grid_data[x][y] = 3
                elif cell.astrophage_level > 0:
                    grid_data[x][y] = 2
                else:
                    grid_data[x][y] = 0

        # Mark agent positions
        grid_data[self.grace.x][self.grace.y] = 8
        grid_data[self.rocky.x][self.rocky.y] = 9

        colors = [
            '#0a0a2e',  # 0 empty space
            '#1a1a4e',  # 1 unused
            '#cc2200',  # 2 astrophage low
            '#ff0000',  # 3 astrophage high
            '#228B22',  # 4 planet Adrian
            '#4169E1',  # 5 Hail Mary
            '#9400D3',  # 6 Blip-A
            '#FFA500',  # 7 hazard
            '#00FFFF',  # 8 Grace
            '#FF69B4',  # 9 Rocky
            '#00CED1',  # 10 tunnel
            '#FFD700',  # 11 time dilation
        ]

        cmap = ListedColormap(colors)
        ax.imshow(grid_data, cmap=cmap, vmin=0, vmax=11)
        ax.set_title(
            f'Tau Ceti System - Turn {turn}',
            color='white', fontsize=12
        )
        ax.tick_params(colors='white')

        legend_items = [
            mpatches.Patch(color='#00FFFF', label='Grace'),
            mpatches.Patch(color='#FF69B4', label='Rocky'),
            mpatches.Patch(color='#228B22', label='Planet Adrian'),
            mpatches.Patch(color='#4169E1', label='Hail Mary'),
            mpatches.Patch(color='#9400D3', label='Blip-A'),
            mpatches.Patch(color='#00CED1', label='Tunnel'),
            mpatches.Patch(color='#cc2200', label='Astrophage'),
            mpatches.Patch(color='#ff0000', label='Dense Astrophage'),
            mpatches.Patch(color='#FFA500', label='Hazard'),
            mpatches.Patch(color='#FFD700', label='Time Dilation'),
        ]
        ax.legend(
            handles=legend_items,
            loc='upper right', fontsize=7,
            facecolor='#0a0a2e', labelcolor='white'
        )

    def draw_stats(self, turn, taumoeba):
        ax = self.axes[1]
        ax.clear()
        ax.set_facecolor('#0a0a2e')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        ax.text(5, 9.5, 'Mission Status',
                color='white', fontsize=14,
                ha='center', fontweight='bold')

        # Grace stats
        ax.text(0.5, 8.8, '--- Dr. Ryland Grace ---',
                color='#00FFFF', fontsize=10,
                fontweight='bold')
        ax.text(0.5, 8.3,
                f'Health: {self.grace.health} | '
                f'Energy: {self.grace.energy}',
                color='white', fontsize=9)
        ax.text(0.5, 7.8,
                f'Knowledge: {self.grace.knowledge}',
                color='white', fontsize=9)
        ax.text(0.5, 7.3,
                f'Taumoeba Samples: '
                f'{self.grace.taumoeba_samples}',
                color='white', fontsize=9)
        ax.text(0.5, 6.8,
                f'Beetle Probes: '
                f'{self.grace.beetle_probes}',
                color='white', fontsize=9)
        ax.text(0.5, 6.3,
                f'Position: ({self.grace.x}, {self.grace.y})',
                color='white', fontsize=9)

        # Rocky stats
        ax.text(0.5, 5.7, '--- Rocky (Eridian) ---',
                color='#FF69B4', fontsize=10,
                fontweight='bold')
        ax.text(0.5, 5.2,
                f'Trust: {self.rocky.trust_level}% | '
                f'Energy: {self.rocky.energy}',
                color='white', fontsize=9)
        ax.text(0.5, 4.7,
                f'Translation: '
                f'{self.rocky.translation_level}%',
                color='white', fontsize=9)
        ax.text(0.5, 4.2,
                f'Fuel: {self.rocky.astrophage_fuel} | '
                f'Contaminated: {self.rocky.ship_contaminated}',
                color='white', fontsize=9)

        # Taumoeba stats
        ax.text(0.5, 3.6, '--- Taumoeba Research ---',
                color='#90EE90', fontsize=10,
                fontweight='bold')
        ax.text(0.5, 3.1,
                f'Earth: {taumoeba.survival_rate_earth:.1%} | '
                f'Erid: {taumoeba.survival_rate_erid:.1%}',
                color='white', fontsize=9)
        ax.text(0.5, 2.6,
                f'Gen: {taumoeba.generation} | '
                f'Mutation: {taumoeba.mutation_rate:.2f}',
                color='white', fontsize=9)
        ax.text(0.5, 2.2,
                f'Earth viable: {taumoeba.is_viable_earth()} | '
                f'Erid viable: {taumoeba.is_viable_erid()}',
                color='#90EE90', fontsize=8)

        # Breeding log
        ax.text(0.5, 1.8, '--- Breeding Log ---',
                color='yellow', fontsize=9,
                fontweight='bold')
        if taumoeba.breeding_log:
            recent = taumoeba.breeding_log[-2:]
            for i, entry in enumerate(recent):
                color = (
                    '#00FF00' if entry['result'] == 'SUCCESS'
                    else '#FFA500' if entry['result'] == 'PARTIAL'
                    else '#FF0000'
                )
                # Use correct key from new taumoeba
                rate = entry.get(
                    'survival_rate_earth',
                    entry.get('survival_rate', 0)
                )
                ax.text(
                    0.5, 1.4 - (i * 0.35),
                    f"Gen {entry['generation']}: "
                    f"{entry['result']} - "
                    f"{rate:.0%}",
                    color=color, fontsize=8
                )
        else:
            ax.text(0.5, 1.4,
                    'No experiments yet',
                    color='grey', fontsize=8)

        # Earth viability progress bar
        earth_progress = min(1.0, taumoeba.survival_rate_earth)
        ax.text(0.5, 0.9,
                'Earth Viability:',
                color='white', fontsize=8)
        ax.barh(0.55, earth_progress * 4.5, height=0.25,
                left=0.5, color='#00FF00', alpha=0.8)
        ax.barh(0.55, 4.5, height=0.25,
                left=0.5, color='grey', alpha=0.2)
        ax.text(5.2, 0.55, f'{earth_progress:.0%}',
                color='white', fontsize=8, va='center')

        # Erid viability progress bar
        erid_progress = min(1.0, taumoeba.survival_rate_erid)
        ax.text(5.3, 0.9,
                'Erid Viability:',
                color='#FF69B4', fontsize=8)
        ax.barh(0.55, erid_progress * 4, height=0.25,
                left=5.5, color='#FF69B4', alpha=0.8)
        ax.barh(0.55, 4, height=0.25,
                left=5.5, color='grey', alpha=0.2)
        ax.text(9.7, 0.55, f'{erid_progress:.0%}',
                color='white', fontsize=8, va='center')

    def update(self, turn, taumoeba):
        """Update the live visualisation each turn"""
        try:
            if self.closed:
                return
            if not plt.fignum_exists(self.fig.number):
                self.closed = True
                return
            self.draw_grid(turn)
            self.draw_stats(turn, taumoeba)
            plt.tight_layout()
            plt.pause(0.5)
        except Exception:
            self.closed = True

    def show_final(self, success, turn, knowledge, probes):
        """Show final mission result screen"""
        try:
            plt.ioff()
            plt.close('all')

            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#0a0a2e')
            ax.set_facecolor('#0a0a2e')
            ax.axis('off')

            if success:
                ax.text(
                    0.5, 0.80,
                    'MISSION SUCCESS!',
                    color='#00FF00', fontsize=36,
                    ha='center', fontweight='bold',
                    transform=ax.transAxes
                )
                ax.text(
                    0.5, 0.63,
                    'Earth has been saved from Astrophage!',
                    color='white', fontsize=16,
                    ha='center', transform=ax.transAxes
                )
            else:
                ax.text(
                    0.5, 0.80,
                    'MISSION FAILED',
                    color='#FF0000', fontsize=36,
                    ha='center', fontweight='bold',
                    transform=ax.transAxes
                )
                ax.text(
                    0.5, 0.63,
                    'The Astrophage wins...',
                    color='white', fontsize=16,
                    ha='center', transform=ax.transAxes
                )

            ax.text(
                0.5, 0.45,
                f'Turns: {turn}   |   '
                f'Knowledge: {knowledge}   |   '
                f'Probes: {probes}',
                color='#AAAAAA', fontsize=13,
                ha='center', transform=ax.transAxes
            )

            plt.savefig(
                'mission_result.png',
                facecolor='#0a0a2e',
                bbox_inches='tight'
            )
            print("\nClose the result window to exit.")
            plt.show(block=True)

        except Exception as e:
            print(f"Visualiser error: {e}")