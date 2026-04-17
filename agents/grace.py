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
        self.in_eva = False
        self.equipment_damaged = False
        self.mission_violations = 0
        self.experiment_history = {
            "solo": {"success": 0, "total": 0},
            "with_rocky": {"success": 0, "total": 0}
        }
        self.strategy_weights = {
            "breed_solo": 0.5,
            "breed_with_rocky": 0.8,
            "collect_more": 0.6,
            "rest_first": 0.7
        }

    def move(self, dx, dy, environment):
        """Move to adjacent cell"""
        cost = 2
        if self.in_eva:
            cost = 5
        if self.equipment_damaged:
            cost += 2

        next_x = (self.x + dx) % environment.height
        next_y = (self.y + dy) % environment.width
        cell = environment.get_cell(next_x, next_y)

        if cell.is_time_dilation:
            cost += 3
            print("Grace enters time-dilation zone!")

        if cell.astrophage_level > 0:
            damage = cell.astrophage_level
            cost += damage
            self.health = max(0, self.health - damage)

        if cell.cell_type == "hazard":
            self.health = max(0, self.health - 5)
            self.energy = max(0, self.energy - 3)

        if self.energy >= cost:
            self.x = next_x
            self.y = next_y
            self.energy -= cost
            print(f"Grace moved to ({self.x}, {self.y}). "
                  f"Energy: {self.energy}")
        else:
            print("Not enough energy to move!")

    def travel_tunnel(self, environment):
        """Travel via xenonite tunnel to Rocky's ship"""
        tunnel_x, tunnel_y = 10, 10
        if (abs(self.x - tunnel_x) <= 2
                and abs(self.y - tunnel_y) <= 2):
            if self.energy >= 10:
                self.x = 10
                self.y = 15
                self.energy -= 10
                print("Grace travels through xenonite "
                      "tunnel to Rocky's ship!")
                return True
        return False

    def perform_eva(self, environment):
        """Extra-vehicular activity"""
        if self.energy >= 15:
            self.in_eva = True
            self.energy -= 15
            print("Grace performs EVA!")
            return True
        return False

    def end_eva(self):
        self.in_eva = False

    def collect_sample(self, environment):
        """
        Collect samples — planet cells prioritise
        Taumoeba over Astrophage
        """
        cell = environment.get_cell(self.x, self.y)

        # On planet: always collect Taumoeba first
        if cell.cell_type == "planet" and cell.has_taumoeba:
            self.taumoeba_samples += 1
            self.energy = max(0, self.energy - 3)
            print(f"Collected Taumoeba sample! "
                  f"Total: {self.taumoeba_samples}")
        elif cell.astrophage_level > 0:
            self.astrophage_samples += 1
            cell.astrophage_level = max(
                0, cell.astrophage_level - 1
            )
            self.energy = max(0, self.energy - 3)
            print(f"Collected Astrophage sample! "
                  f"Total: {self.astrophage_samples}")
        else:
            print("Nothing to collect here.")

    def analyse_data(self):
        """Analyse data for knowledge"""
        if self.astrophage_samples < 1:
            return 0
        self.energy = max(0, self.energy - 5)
        gain = random.randint(5, 15)
        self.knowledge += gain
        print(f"Data analysis! Knowledge +{gain}")
        return gain

    def conduct_experiment(self, with_rocky=False):
        """Experiment with online learning"""
        if self.taumoeba_samples < 1:
            return "no_samples"
        if self.energy < 10:
            return "no_energy"

        self.energy -= 10
        key = "with_rocky" if with_rocky else "solo"

        if with_rocky:
            success_chance = min(
                0.7, self.strategy_weights["breed_with_rocky"]
            )
        else:
            success_chance = min(
                0.5, self.strategy_weights["breed_solo"]
            )

        outcome_roll = random.random()
        if outcome_roll < success_chance * 0.4:
            outcome = "success"
            self.knowledge += 20
            self.strategy_weights[
                "breed_with_rocky" if with_rocky
                else "breed_solo"
            ] = min(0.9, self.strategy_weights[
                "breed_with_rocky" if with_rocky
                else "breed_solo"
            ] + 0.05)
        elif outcome_roll < success_chance:
            outcome = "partial"
            self.knowledge += 10
        else:
            outcome = "failure"
            self.knowledge += 2
            weight_key = (
                "breed_with_rocky" if with_rocky
                else "breed_solo"
            )
            self.strategy_weights[weight_key] = max(
                0.2,
                self.strategy_weights[weight_key] - 0.02
            )

        self.experiment_history[key]["total"] += 1
        if outcome == "success":
            self.experiment_history[key]["success"] += 1

        self.experiment_log.append(outcome)
        return outcome

    def deploy_beetle_probe(self):
        """Deploy a beetle probe"""
        if self.beetle_probes > 0 and self.knowledge >= 20:
            self.beetle_probes -= 1
            self.energy = max(0, self.energy - 15)
            print(f"Beetle probe deployed! "
                  f"Remaining: {self.beetle_probes}")
            return True
        return False

    def repair_equipment(self):
        if self.equipment_damaged and self.energy >= 10:
            self.equipment_damaged = False
            self.energy -= 10
            print("Grace repairs equipment!")

    def flashback(self):
        if not self.memory_restored and self.knowledge >= 10:
            self.memory_restored = True
            print("\n*** FLASHBACK ***")
            print("Grace remembers: Eva Stratt, "
                  "the Hail Mary mission!")
            print("Mission: Find why Tau Ceti is "
                  "unaffected. Save Earth!")
            print("*****************\n")

    def rest(self):
        self.energy = min(100, self.energy + 20)
        self.in_eva = False
        print(f"Grace rested. Energy: {self.energy}")

    def get_success_rate(self, mode="with_rocky"):
        hist = self.experiment_history[mode]
        if hist["total"] == 0:
            return 0.0
        return hist["success"] / hist["total"]

    def status(self):
        print(f"\n--- {self.name} ---")
        print(f"Position: ({self.x}, {self.y})")
        print(f"Health: {self.health} | "
              f"Energy: {self.energy}")
        print(f"Knowledge: {self.knowledge}")
        print(f"Astrophage samples: {self.astrophage_samples}")
        print(f"Taumoeba samples: {self.taumoeba_samples}")
        print(f"Beetle Probes: {self.beetle_probes}")
        print(f"Equipment damaged: {self.equipment_damaged}")
        print(f"Experiments: {self.experiment_log}")
        print(f"Solo success rate: "
              f"{self.get_success_rate('solo'):.1%}")
        print(f"Rocky success rate: "
              f"{self.get_success_rate('with_rocky'):.1%}")