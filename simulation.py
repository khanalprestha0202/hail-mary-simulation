import random
from environment import Environment
from agents.grace import Grace
from agents.rocky import Rocky
from entities.taumoeba import Taumoeba
from entities.beetle_probe import BeetleProbe


class Simulation:
    def __init__(self):
        self.environment = Environment()
        self.grace = Grace(x=10, y=5)
        self.rocky = Rocky(x=10, y=15)
        self.taumoeba = Taumoeba()
        self.beetle_probes = []
        self.turn = 0
        self.mission_success = False
        self.mission_aborted = False
        self.probe_counter = 0

    def step(self):
        """One turn of the simulation"""
        self.turn += 1
        print(f"\n========== TURN {self.turn} ==========")

        # --- Grace actions ---
        self._grace_action()

        # --- Rocky actions ---
        self._rocky_action()

        # --- Environment updates ---
        self.environment.spread_astrophage()

        # --- Update beetle probes ---
        for probe in self.beetle_probes:
            probe.navigate()

        # --- Check flashback ---
        self.grace.flashback()

        # --- Check win/lose conditions ---
        self._check_conditions()

    def _grace_action(self):
        """Grace AI decision making"""
        cell = self.environment.get_cell(self.grace.x, self.grace.y)

        # Priority 1: rest if energy low
        if self.grace.energy < 20:
            self.grace.rest()
        # Priority 2: collect taumoeba if on planet
        elif cell.cell_type == "planet":
            self.grace.collect_sample(self.environment)
        # Priority 3: experiment if enough samples
        elif self.grace.taumoeba_samples >= 2:
            outcome = self.taumoeba.breed(self.grace, self.rocky)
            if outcome:
                print("🌍 Taumoeba viable for Earth! Deploying beetle probe!")
                self._deploy_probe()
        # Priority 4: collect astrophage sample
        elif cell.astrophage_level > 0:
            self.grace.collect_sample(self.environment)
        # Priority 5: move toward planet
        else:
            self._move_grace_toward_planet()

    def _move_grace_toward_planet(self):
        """Move Grace toward planet Adrian"""
        planet_x, planet_y = 5, 10
        dx = 1 if self.grace.x < planet_x else -1 if self.grace.x > planet_x else 0
        dy = 1 if self.grace.y < planet_y else -1 if self.grace.y > planet_y else 0
        self.grace.move(dx, dy, self.environment)

    def _rocky_action(self):
        """Rocky AI decision making"""
        # Rocky always tries to communicate first
        if self.rocky.translation_level < 100:
            self.rocky.communicate(self.grace)

        # Share knowledge when trust is high enough
        if self.rocky.trust_level >= 20:
            self.rocky.share_knowledge(self.grace)

        # Assist experiments when trust is high
        if self.rocky.trust_level >= 30 and self.grace.taumoeba_samples >= 1:
            self.rocky.assist_experiment(self.grace)

        # Transfer fuel if Grace is low
        if self.grace.energy < 30 and self.rocky.trust_level >= 50:
            self.grace.energy = self.rocky.transfer_fuel(self.grace.energy)

        # Rocky rests if energy low
        if self.rocky.energy < 20:
            self.rocky.rest()

    def _deploy_probe(self):
        """Deploy a beetle probe with current knowledge"""
        if self.probe_counter < 4 and self.grace.beetle_probes > 0:
            probe = BeetleProbe(
                probe_id=self.probe_counter,
                x=self.grace.x,
                y=self.grace.y,
                knowledge_payload=self.grace.knowledge
            )
            self.beetle_probes.append(probe)
            self.grace.beetle_probes -= 1
            self.probe_counter += 1
            print(f"🛸 Probe {probe.name} launched with {probe.knowledge_payload} knowledge!")

    def _check_conditions(self):
        """Check win and lose conditions"""
        # Win condition
        if self.taumoeba.is_viable() and any(p.reached_earth for p in self.beetle_probes):
            self.mission_success = True
            print("\n🌍 MISSION SUCCESS! Earth is saved!")

        # Lose conditions
        if self.grace.energy <= 0 or self.grace.health <= 0:
            self.mission_aborted = True
            print("\n💀 MISSION ABORTED! Grace has fallen!")

    def print_status(self):
        self.grace.status()
        self.rocky.status()
        self.taumoeba.status()
        for probe in self.beetle_probes:
            probe.status()

    def run(self, max_turns=50):
        print("🚀 HAIL MARY MISSION BEGINS!")
        print("Grace wakes from coma... where am I?")
        self.environment.display()

        while (self.turn < max_turns
               and not self.mission_success
               and not self.mission_aborted):
            self.step()
            if self.turn % 10 == 0:
                self.print_status()
                self.environment.display()

        print(f"\n=== SIMULATION ENDED AT TURN {self.turn} ===")
        print(f"Mission Success: {self.mission_success}")
        print(f"Final Knowledge: {self.grace.knowledge}")
        print(f"Probes Deployed: {self.probe_counter}")
        self.print_status()