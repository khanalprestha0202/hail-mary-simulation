import random


class Cell:
    def __init__(self):
        self.cell_type = "space"
        self.astrophage_level = 0
        self.astrophage_resistance = 0
        self.has_taumoeba = False
        self.is_time_dilation = False
        self.agent = None

    def __str__(self):
        if self.agent:
            return self.agent
        if self.cell_type == "planet":
            return "🪐"
        if self.cell_type == "hail_mary":
            return "🚀"
        if self.cell_type == "blip_a":
            return "🛸"
        if self.cell_type == "tunnel":
            return "🔗"
        if self.cell_type == "hazard":
            return "☢ "
        if self.is_time_dilation:
            return "⏳"
        if self.astrophage_level > 6:
            return "💀"
        if self.astrophage_level > 0:
            return "🔴"
        return "⬛"


class Environment:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]
        self.turn = 0
        self.taumoeba_deployed = 0
        self._setup_world()

    def _setup_world(self):
        """Procedurally generate the world"""
        # Place Hail Mary spacecraft
        self.grid[10][5].cell_type = "hail_mary"
        # Place Blip-A spacecraft (Rocky's ship)
        self.grid[10][15].cell_type = "blip_a"
        # Place planet Adrian with Taumoeba
        self.grid[5][10].cell_type = "planet"
        self.grid[5][10].has_taumoeba = True
        # Connecting tunnel between ships
        self.grid[10][10].cell_type = "tunnel"

        # Petrova line - procedurally generated intensity
        for i in range(self.height):
            intensity = random.randint(7, 10)
            self.grid[i][10].astrophage_level = intensity

        # Random Astrophage clusters - procedural generation
        cluster_count = random.randint(10, 20)
        for _ in range(cluster_count):
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if self.grid[x][y].cell_type == "space":
                self.grid[x][y].astrophage_level = (
                    random.randint(1, 5)
                )

        # Hazard zones - random radiation/debris
        hazard_count = random.randint(3, 7)
        for _ in range(hazard_count):
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if self.grid[x][y].cell_type == "space":
                self.grid[x][y].cell_type = "hazard"

        # Time dilation zones (near-light-speed segments)
        for _ in range(3):
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if self.grid[x][y].cell_type == "space":
                self.grid[x][y].is_time_dilation = True

    def get_cell(self, x, y):
        """Get cell with edge wrapping for open space"""
        return self.grid[x % self.height][y % self.width]

    def spread_astrophage(self):
        """Astrophage spreads each turn dynamically"""
        self.turn += 1
        new_levels = {}

        for x in range(self.height):
            for y in range(self.width):
                cell = self.grid[x][y]
                if cell.astrophage_level > 0:
                    # Spread chance increases over time
                    spread_chance = min(0.3, 0.05 + self.turn * 0.002)

                    # Resistance reduces spread chance
                    spread_chance = max(
                        0.01,
                        spread_chance - cell.astrophage_resistance * 0.05
                    )

                    if random.random() < spread_chance:
                        nx = (x + random.choice([-1, 1])) % self.height
                        ny = (y + random.choice([-1, 1])) % self.width
                        key = (nx, ny)
                        new_levels[key] = (
                            new_levels.get(key, 0) + 1
                        )

        for (x, y), amount in new_levels.items():
            self.grid[x][y].astrophage_level += amount

    def apply_taumoeba_resistance(self, x, y):
        """
        When Taumoeba is deployed, Astrophage
        develops resistance over time
        """
        self.taumoeba_deployed += 1
        cell = self.get_cell(x, y)
        # Reduce Astrophage but increase resistance
        reduction = max(1, 3 - cell.astrophage_resistance)
        cell.astrophage_level = max(
            0, cell.astrophage_level - reduction
        )
        # Astrophage develops resistance
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbour = self.get_cell(x + dx, y + dy)
                if neighbour.astrophage_level > 0:
                    neighbour.astrophage_resistance = min(
                        5,
                        neighbour.astrophage_resistance + 1
                    )

    def trigger_equipment_failure(self):
        """Random equipment failure event"""
        if random.random() < 0.05:
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            if self.grid[x][y].astrophage_level == 0:
                self.grid[x][y].cell_type = "hazard"
            return True
        return False

    def display(self):
        print("\n=== TAU CETI SYSTEM ===")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print("=======================\n")