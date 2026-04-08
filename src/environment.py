import random

# Cell types on the grid
EMPTY = 0
ASTROPHAGE = 1
ADRIAN = 2
HAIL_MARY = 3
BLIP_A = 4
RADIATION = 5
TAUMOEBA = 6
RELATIVISTIC = 7  # Optional: Time-dilation zones (req a ext)

CELL_NAMES = {
    RELATIVISTIC: "Relativistic Zone",
    EMPTY: "Empty Space",
    ASTROPHAGE: "Astrophage Cloud",
    ADRIAN: "Planet Adrian",
    HAIL_MARY: "Hail Mary Ship",
    BLIP_A: "Blip-A Ship",
    RADIATION: "Radiation Zone",
    TAUMOEBA: "Taumoeba Zone",
}

class Environment:
    def __init__(self, width=25, height=25):
        self.width = width
        self.height = height
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.astrophage_intensity = [[0.0 for _ in range(width)] for _ in range(height)]
        self.taumoeba_present = [[False for _ in range(width)] for _ in range(height)]
        self.turn = 0
        self._setup_grid()

    def _setup_grid(self):
        # Place planet Adrian
        self.grid[12][12] = ADRIAN
        self.taumoeba_present[12][12] = True

        # Place Hail Mary spacecraft
        self.grid[5][5] = HAIL_MARY
        self.hail_mary_pos = (5, 5)

        # Place Blip-A spacecraft
        self.grid[5][8] = BLIP_A
        self.blip_a_pos = (5, 8)

        # Place Petrova line (dense Astrophage band)
        for col in range(self.width):
            self.grid[10][col] = ASTROPHAGE
            self.astrophage_intensity[10][col] = random.uniform(0.7, 1.0)

        # Place scattered Astrophage clouds
        for _ in range(20):
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = ASTROPHAGE
                self.astrophage_intensity[row][col] = random.uniform(0.1, 0.5)

# Place radiation zones
        for _ in range(8):
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = RADIATION

        # Relativistic zones (optional ext)
        for _ in range(3):
            row = random.randint(18, self.height - 1)
            col = random.randint(18, self.width - 1)
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = RELATIVISTIC

    def get_cell(self, row, col):
        # Wrap around edges (open space simulation)
        row = row % self.height
        col = col % self.width
        return self.grid[row][col]

    def spread_astrophage(self):
        """Astrophage spreads to adjacent empty cells each turn"""
        new_astrophage = []
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == ASTROPHAGE:
                    intensity = self.astrophage_intensity[row][col]
                    if intensity > 0.3 and random.random() < 0.08:
                        # Try to spread to a neighbour
                        neighbours = [
                            ((row-1) % self.height, col),
                            ((row+1) % self.height, col),
                            (row, (col-1) % self.width),
                            (row, (col+1) % self.width),
                        ]
                        for nr, nc in neighbours:
                            if self.grid[nr][nc] == EMPTY:
                                new_astrophage.append((nr, nc, intensity * 0.5))
                                break

        for row, col, intensity in new_astrophage:
            self.grid[row][col] = ASTROPHAGE
            self.astrophage_intensity[row][col] = intensity
    
    def adapt_astrophage_resistance(self, taumoeba_deployed_count):
        """
        Expert-level: Astrophage becomes more resistant
        as Taumoeba is deployed more — simulates evolutionary pressure.
        """
        resistance = min(0.5, taumoeba_deployed_count * 0.05)
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] == ASTROPHAGE:
                    # Resistant Astrophage regenerates intensity slightly
                    if random.random() < resistance:
                        self.astrophage_intensity[r][c] = min(
                            1.0, self.astrophage_intensity[r][c] + 0.05
                        )

    def apply_taumoeba(self, row, col):
        """Taumoeba reduces Astrophage intensity"""
        row = row % self.height
        col = col % self.width
        if self.grid[row][col] == ASTROPHAGE:
            self.astrophage_intensity[row][col] -= 0.3
            if self.astrophage_intensity[row][col] <= 0:
                self.grid[row][col] = EMPTY
                self.astrophage_intensity[row][col] = 0
            return True
        return False

    def get_energy_drain(self, row, col):
        """Returns how much energy is drained by a cell"""
        row = row % self.height
        col = col % self.width
        cell = self.grid[row][col]
        if cell == ASTROPHAGE:
            return int(self.astrophage_intensity[row][col] * 15)
        elif cell == RADIATION:
            return 10
        elif cell == RELATIVISTIC:
            return 8  # Time-dilation fatigue
        return 0

    def step(self):
        self.turn += 1
        if self.turn % 3 == 0:
            self.spread_astrophage()

    def display_text(self):
        """Simple text display of the grid"""
        symbols = {
            EMPTY: ".",
            ASTROPHAGE: "A",
            ADRIAN: "P",
            HAIL_MARY: "H",
            BLIP_A: "B",
            RADIATION: "R",
            TAUMOEBA: "T",
            RELATIVISTIC: "W",  # Warp/Relativistic
        }
        print(f"\n=== TAU CETI SYSTEM - Turn {self.turn} ===")
        for row in self.grid:
            print(" ".join(symbols.get(cell, "?") for cell in row))