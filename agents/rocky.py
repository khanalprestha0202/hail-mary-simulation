import random


class Rocky:
    def __init__(self, x=10, y=15):
        self.x = x
        self.y = y
        self.health = 100
        self.energy = 100
        self.knowledge = 50
        self.name = "Rocky"
        self.species = "Eridian"
        self.astrophage_fuel = 80
        self.trust_level = 0
        self.shared_data = []
        self.translation_level = 0
        self.ship_contaminated = False
        self.contamination_level = 0
        self.reconnaissance_data = []
        self.equipment_repaired = 0

    def move(self, dx, dy, environment):
        """Rocky moves within his ship and nearby space"""
        cost = 2
        if self.energy >= cost:
            self.x = (self.x + dx) % environment.height
            self.y = (self.y + dy) % environment.width
            self.energy -= cost

    def communicate(self, grace):
        """Rocky communicates via sonar chord patterns"""
        self.translation_level = min(
            100, self.translation_level + 10
        )
        grace.knowledge += 5
        self.trust_level = min(100, self.trust_level + 10)
        chords = ["♪♫♪", "♫♪♫", "♪♪♫", "♫♫♪"]
        chord = random.choice(chords)
        print(f"Rocky: {chord} "
              f"(Translation: {self.translation_level}%)")
        if self.translation_level >= 30:
            print("Rocky: 'My star also threatened. "
                  "We help each other!'")
        if self.translation_level >= 60:
            print("Rocky shares star map data! "
                  "Grace knowledge +5")
        if self.translation_level >= 80:
            print("Rocky: 'Taumoeba must survive in "
                  "both atmospheres!'")
        self.shared_data.append(
            f"Communication at {self.translation_level}%"
        )

    def share_knowledge(self, grace):
        """Rocky shares scientific data"""
        if self.trust_level < 20:
            print("Rocky not yet trusting enough.")
            return
        gain = random.randint(10, 25)
        grace.knowledge += gain
        self.energy -= 5
        print(f"Rocky shares Astrophage data! "
              f"Grace knowledge +{gain}")
        self.shared_data.append(f"Knowledge shared: +{gain}")

    def perform_repair(self, grace):
        """Rocky performs engineering repairs"""
        if self.trust_level < 40:
            print("Rocky needs more trust for repairs.")
            return
        grace.energy = min(100, grace.energy + 30)
        self.energy -= 20
        self.equipment_repaired += 1
        print("Rocky repairs Hail Mary systems! "
              "Grace energy +30")

    def repair_grace_equipment(self, grace):
        """Rocky fixes Grace's damaged equipment"""
        if grace.equipment_damaged and self.trust_level >= 50:
            grace.equipment_damaged = False
            self.energy -= 15
            print("Rocky fixes Grace's equipment!")

    def transfer_fuel(self, grace_energy):
        """Rocky shares Astrophage fuel reserves"""
        if (self.astrophage_fuel >= 20
                and self.trust_level >= 50):
            self.astrophage_fuel -= 20
            grace_energy = min(100, grace_energy + 20)
            print(f"Rocky transfers fuel! "
                  f"Rocky fuel: {self.astrophage_fuel}")
            return grace_energy
        print("Rocky cannot transfer fuel yet.")
        return grace_energy

    def assist_experiment(self, grace):
        """Rocky assists Taumoeba experiments"""
        if self.trust_level < 30:
            print("Rocky not ready to assist.")
            return
        if grace.taumoeba_samples < 1:
            print("No Taumoeba samples!")
            return
        self.energy -= 10
        bonus = random.randint(5, 15)
        grace.knowledge += bonus
        print(f"Rocky assists experiment! "
              f"Extra knowledge +{bonus}")

    def conduct_reconnaissance(self, environment):
        """
        Rocky scouts nearby space from the Blip-A,
        using sonar to detect Astrophage patterns.
        """
        if self.energy < 10:
            return None

        self.energy -= 10
        scan_results = []

        # Scan area around Rocky's position
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                cell = environment.get_cell(
                    self.x + dx, self.y + dy
                )
                if cell.astrophage_level > 3:
                    scan_results.append({
                        "x": (self.x + dx) % environment.height,
                        "y": (self.y + dy) % environment.width,
                        "level": cell.astrophage_level
                    })

        self.reconnaissance_data.extend(scan_results)
        if scan_results:
            print(f"Rocky reconnaissance: Found "
                  f"{len(scan_results)} Astrophage threats!")
        return scan_results

    def check_contamination(self, taumoeba):
        """
        Check if Taumoeba has contaminated Rocky's ship.
        Taumoeba can survive in Rocky's atmosphere
        but poses risks.
        """
        if (taumoeba.survival_rate_erid > 0.5
                and random.random() < 0.1):
            self.contamination_level += 1
            if self.contamination_level >= 3:
                self.ship_contaminated = True
                print("WARNING: Rocky's ship contaminated "
                      "by Taumoeba!")
            else:
                print(f"Taumoeba detected in Blip-A! "
                      f"Level: {self.contamination_level}/3")

    def treat_contamination(self, grace):
        """Grace and Rocky work together to treat contamination"""
        if (self.ship_contaminated
                and grace.knowledge >= 50
                and self.trust_level >= 60):
            self.ship_contaminated = False
            self.contamination_level = 0
            grace.energy -= 20
            self.energy -= 20
            grace.knowledge += 30
            print("Contamination treated! Rocky's ship saved!")
            return True
        return False

    def rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"Rocky rested. Energy: {self.energy}")

    def status(self):
        print(f"\n--- {self.name} ({self.species}) ---")
        print(f"Position: ({self.x}, {self.y})")
        print(f"Health: {self.health} | Energy: {self.energy}")
        print(f"Knowledge: {self.knowledge}")
        print(f"Trust: {self.trust_level}% | "
              f"Translation: {self.translation_level}%")
        print(f"Astrophage fuel: {self.astrophage_fuel}")
        print(f"Ship contaminated: {self.ship_contaminated}")
        print(f"Contamination level: "
              f"{self.contamination_level}/3")
        print(f"Repairs done: {self.equipment_repaired}")