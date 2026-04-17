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
        # Online learning - track experiment success rates
        self.experiment_history = {
            "solo": {"success": 0, "total": 0},
            "with_rocky": {"success": 0, "total": 0}
        }
        # Reinforcement learning weights
        self.strategy_weights = {
            "breed_solo": 0.5,
            "breed_with_rocky": 0.8,
            "collect_more": 0.6,
            "rest_first": 0.7
        }

    def move(self, dx, dy, environment):
        """Move to adjacent cell with energy cost"""
        cost = 2
        if self.in_eva:
            cost = 5  # EVA costs more energy
        if self.equipment_damaged:
            cost += 2

        cell = environment.get_cell(
            self.x + dx, self.y + dy
        )

        # Time dilation zone slows movement
        if cell.is_time_dilation:
            cost += 3
            print("Grace enters time-dilation zone! "
                  "Movement slowed.")

        # Astrophage exposure costs health and energy
        if cell.astrophage_level > 0:
            damage = cell.astrophage_level
            cost += damage
            self.health -= damage
            print(f"Astrophage exposure! "
                  f"Health -{damage}: {self.health}")

        # Hazard zone damage
        if cell.cell_type == "hazard":
            self.health -= 5
            self.energy -= 5
            print("Radiation hazard! Health -5, Energy -5")

        if self.energy >= cost:
            self.x = (self.x + dx) % environment.height
            self.y = (self.y + dy) % environment.width
            self.energy -= cost
        else:
            print("Not enough energy to move!")

    def travel_tunnel(self, environment):
        """
        Travel via xenonite tunnel to Rocky's ship.
        Costs extra energy but allows inter-ship travel.
        """
        tunnel_x, tunnel_y = 10, 10
        blip_x, blip_y = 10, 15

        # Check if near tunnel
        if (abs(self.x - tunnel_x) <= 1
                and abs(self.y - tunnel_y) <= 1):
            if self.energy >= 10:
                self.x = blip_x
                self.y = blip_y
                self.energy -= 10
                print("Grace travels through xenonite "
                      "tunnel to Rocky's ship!")
                return True
            else:
                print("Not enough energy for tunnel travel!")
        return False

    def perform_eva(self, environment):
        """Extra-vehicular activity - costly but reaches more cells"""
        if self.energy >= 20:
            self.in_eva = True
            self.energy -= 20
            print("Grace performs EVA! "
                  "Extended movement range active.")
            return True
        else:
            print("Not enough energy for EVA!")
            return False

    def end_eva(self):
        self.in_eva = False
        print("Grace returns from EVA.")

    def collect_sample(self, environment):
        """Collect Astrophage or Taumoeba samples"""
        cell = environment.get_cell(self.x, self.y)
        if cell.astrophage_level > 0:
            self.astrophage_samples += 1
            cell.astrophage_level = max(
                0, cell.astrophage_level - 1
            )
            self.energy -= 3
            print(f"Collected Astrophage sample! "
                  f"Total: {self.astrophage_samples}")
        elif cell.has_taumoeba:
            self.taumoeba_samples += 1
            self.energy -= 3
            print(f"Collected Taumoeba sample! "
                  f"Total: {self.taumoeba_samples}")
        else:
            print("Nothing to collect here.")

    def analyse_data(self):
        """Analyse collected data for knowledge gain"""
        if self.astrophage_samples < 1:
            print("Need samples to analyse!")
            return 0
        self.energy -= 5
        gain = random.randint(5, 15)
        self.knowledge += gain
        print(f"Data analysis complete! Knowledge +{gain}")
        return gain

    def conduct_experiment(self, with_rocky=False):
        """
        Conduct experiment with online learning.
        Strategy weights update based on outcomes.
        """
        if self.taumoeba_samples < 1:
            print("Need Taumoeba samples!")
            return "no_samples"
        if self.energy < 10:
            print("Not enough energy!")
            return "no_energy"

        self.energy -= 10

        # Use learned strategy weights
        if with_rocky:
            success_chance = min(
                0.7,
                self.strategy_weights["breed_with_rocky"]
            )
            key = "with_rocky"
        else:
            success_chance = min(
                0.5,
                self.strategy_weights["breed_solo"]
            )
            key = "solo"

        outcome_roll = random.random()
        if outcome_roll < success_chance * 0.5:
            outcome = "success"
            self.knowledge += 20
            # Reinforce successful strategy
            self.strategy_weights[
                f"breed_{key.replace('_', '_')}"
            ] = min(0.9, self.strategy_weights.get(
                f"breed_{key}", 0.5
            ) + 0.05)
        elif outcome_roll < success_chance:
            outcome = "partial"
            self.knowledge += 10
        else:
            outcome = "failure"
            self.knowledge += 2
            # Learn from failure - reduce weight slightly
            weight_key = (
                "breed_with_rocky" if with_rocky
                else "breed_solo"
            )
            self.strategy_weights[weight_key] = max(
                0.2,
                self.strategy_weights[weight_key] - 0.03
            )

        # Update experiment history for online learning
        self.experiment_history[key]["total"] += 1
        if outcome == "success":
            self.experiment_history[key]["success"] += 1

        print(f"Experiment {outcome.upper()}! "
              f"Knowledge: {self.knowledge}")
        self.experiment_log.append(outcome)
        return outcome

    def deploy_beetle_probe(self, knowledge_threshold=30):
        """Deploy a beetle probe if conditions met"""
        if self.beetle_probes > 0 and (
                self.knowledge >= knowledge_threshold
        ):
            self.beetle_probes -= 1
            self.energy -= 15
            print(f"Beetle probe deployed! "
                  f"Remaining: {self.beetle_probes}")
            return True
        print("Cannot deploy probe yet!")
        return False

    def repair_equipment(self):
        """Repair damaged equipment"""
        if self.equipment_damaged and self.energy >= 10:
            self.equipment_damaged = False
            self.energy -= 10
            print("Grace repairs equipment!")

    def flashback(self):
        """Flashback event when knowledge threshold reached"""
        if not self.memory_restored and self.knowledge >= 10:
            self.memory_restored = True
            print("\n*** FLASHBACK ***")
            print("Grace remembers: Eva Stratt, "
                  "the Hail Mary mission,")
            print("the Astrophage threat on Earth...")
            print("Mission: Find why Tau Ceti is unaffected."
                  " Save Earth!")
            print("*****************\n")

    def rest(self):
        """Rest to restore energy"""
        self.energy = min(100, self.energy + 20)
        self.in_eva = False
        print(f"Grace rested. Energy: {self.energy}")

    def get_success_rate(self, mode="with_rocky"):
        """Get experiment success rate for reporting"""
        hist = self.experiment_history[mode]
        if hist["total"] == 0:
            return 0.0
        return hist["success"] / hist["total"]

    def status(self):
        print(f"\n--- {self.name} ---")
        print(f"Position: ({self.x}, {self.y})")
        print(f"Health: {self.health} | Energy: {self.energy}")
        print(f"Knowledge: {self.knowledge}")
        print(f"Astrophage samples: {self.astrophage_samples}")
        print(f"Taumoeba samples: {self.taumoeba_samples}")
        print(f"Beetle Probes: {self.beetle_probes}")
        print(f"EVA active: {self.in_eva}")
        print(f"Equipment damaged: {self.equipment_damaged}")
        print(f"Experiment log: {self.experiment_log}")
        print(f"Solo success rate: "
              f"{self.get_success_rate('solo'):.1%}")
        print(f"With Rocky success rate: "
              f"{self.get_success_rate('with_rocky'):.1%}")