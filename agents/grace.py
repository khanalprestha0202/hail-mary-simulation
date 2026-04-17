import random


class Grace:
    def __init__(self, x=10, y=5):
        self.x = x
        self.y = y
        self.health = 100
        self.energy = 100
        self.knowledge = 0
        self.astrophage_samples = 0
        self.taumoeba_samples = 0
        self.name = "Dr. Ryland Grace"
        self.experiment_log = []
        self.beetle_probes = 4
        self.memory_restored = False

    def move(self, dx, dy, environment):
        cost = 2
        cell = environment.get_cell(self.x + dx, self.y + dy)
        if cell.astrophage_level > 0:
            cost += cell.astrophage_level
            self.health -= cell.astrophage_level
        if self.energy >= cost:
            self.x = (self.x + dx) % environment.height
            self.y = (self.y + dy) % environment.width
            self.energy -= cost
            print(f"Grace moved to ({self.x}, {self.y}). Energy: {self.energy}")
        else:
            print("Not enough energy to move!")

    def collect_sample(self, environment):
        cell = environment.get_cell(self.x, self.y)
        if cell.astrophage_level > 0:
            self.astrophage_samples += 1
            cell.astrophage_level -= 1
            self.energy -= 3
            print(f"Collected Astrophage sample! Total: {self.astrophage_samples}")
        elif cell.has_taumoeba:
            self.taumoeba_samples += 1
            self.energy -= 3
            print(f"Collected Taumoeba sample! Total: {self.taumoeba_samples}")
        else:
            print("Nothing to collect here.")

    def conduct_experiment(self):
        if self.taumoeba_samples < 1:
            print("Need Taumoeba samples to experiment!")
            return
        if self.energy < 10:
            print("Not enough energy to experiment!")
            return
        self.energy -= 10
        outcome = random.choices(
            ["success", "partial", "failure"],
            weights=[0.3, 0.4, 0.3]
        )[0]
        if outcome == "success":
            self.knowledge += 20
            print("Experiment SUCCESS! Knowledge +20")
        elif outcome == "partial":
            self.knowledge += 10
            print("Experiment PARTIAL success. Knowledge +10")
        else:
            self.knowledge += 2
            print("Experiment FAILED. Recording results...")
        self.experiment_log.append(outcome)

    def deploy_beetle_probe(self):
        if self.beetle_probes > 0 and self.knowledge >= 30:
            self.beetle_probes -= 1
            self.energy -= 15
            print(f"Beetle probe deployed! Probes remaining: {self.beetle_probes}")
            return True
        else:
            print("Cannot deploy - need knowledge >= 30 or no probes left!")
            return False

    def flashback(self):
        if not self.memory_restored and self.knowledge >= 10:
            self.memory_restored = True
            print("\n*** FLASHBACK ***")
            print("Grace remembers: Eva Stratt, the Hail Mary mission,")
            print("the Astrophage threat on Earth...")
            print("Mission: Find why Tau Ceti is unaffected. Save Earth!")
            print("*****************\n")

    def rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"Grace rested. Energy: {self.energy}")

    def status(self):
        print(f"\n--- {self.name} ---")
        print(f"Position: ({self.x}, {self.y})")
        print(f"Health: {self.health} | Energy: {self.energy}")
        print(f"Knowledge: {self.knowledge}")
        print(f"Astrophage samples: {self.astrophage_samples}")
        print(f"Taumoeba samples: {self.taumoeba_samples}")
        print(f"Beetle Probes left: {self.beetle_probes}")
        print(f"Experiments: {self.experiment_log}\n")