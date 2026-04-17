import random


class Cell:
    def __init__(self):
        self.cell_type = "space"
        self.astrophage_level = 0
        self.has_taumoeba = False
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
        if self.cell_type == "hazard":
            return "☢ "
        if self.astrophage_level > 5:
            return "💀"
        if self.astrophage_level > 0:
            return "🔴"
        return "⬛"


class Environment:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)]
                     for _ in range(height)]
        self._setup_world()

    def _setup_world(self):
        # Place Hail Mary spacecraft
        self.grid[10][5].cell_type = "hail_mary"
        # Place Blip-A spacecraft
        self.grid[10][15].cell_type = "blip_a"
        # Place planet Adrian
        self.grid[5][10].cell_type = "planet"
        self.grid[5][10].has_taumoeba = True
        # Petrova line - dense Astrophage column
        for i in range(self.height):
            self.grid[i][10].astrophage_level = 8
        # Random Astrophage clusters
        for _ in range(15):
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            self.grid[x][y].astrophage_level = random.randint(1, 4)
        # Hazard zones
        for _ in range(5):
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            self.grid[x][y].cell_type = "hazard"

    def get_cell(self, x, y):
        # Wraps around edges (open space simulation)
        return self.grid[x % self.height][y % self.width]

    def spread_astrophage(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.grid[x][y].astrophage_level > 0:
                    if random.random() < 0.1:
                        nx = (x + random.choice([-1, 1])) % self.height
                        ny = (y + random.choice([-1, 1])) % self.width
                        self.grid[nx][ny].astrophage_level += 1

    def display(self):
        print("\n=== TAU CETI SYSTEM ===")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print("=======================\n")


if __name__ == "__main__":
    env = Environment()
    env.display()