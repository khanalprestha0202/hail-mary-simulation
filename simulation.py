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

        # Priority 1: rest if energy very low
        if self.grace.energy < 15:
            self.grace.rest()

        # Priority 2: deploy probe if Taumoeba is viable
        elif self.taumoeba.is_viable():
            self._deploy_probe()

        # Priority 3: breed Taumoeba if enough samples and knowledge
        elif self.grace.taumoeba_samples >= 2 and self.grace.knowledge >= 20:
            result = self.taumoeba.breed(self.grace, self.rocky)
            if result:
                print("🌍 Taumoeba viable! Deploying beetle probe!")
                self._deploy_probe()

        # Priority 4: collect samples if standing on planet
        elif cell.cell_type == "planet":
            self.grace.collect_sample(self.environment)
            self.grace.collect_sample(self.environment)

        # Priority 5: experiment if have at least 1 sample
        elif self.grace.taumoeba_samples >= 1 and self.grace.knowledge >= 20:
            self.taumoeba.breed(self.grace, self.rocky)

        # Priority 6: move toward planet Adrian
        else:
            self._move_grace_toward_planet()

    def _move_grace_toward_planet(self):
        """Move Grace toward planet Adrian smartly avoiding hazards"""
        planet_x, planet_y = 5, 10
        dx = 0
        dy = 0

        if self.grace.x < planet_x:
            dx = 1
        elif self.grace.x > planet_x:
            dx = -1

        if self.grace.y < planet_y:
            dy = 1
        elif self.grace.y > planet_y:
            dy = -1

        # Check if next cell is too dangerous
        next_cell = self.environment.get_cell(
            self.grace.x + dx,
            self.grace.y + dy
        )

        # Avoid deadly Astrophage cells
        if next_cell.astrophage_level > 6:
            # Try alternate route around hazard
            alt_dx = random.choice([-1, 0, 1])
            alt_dy = random.choice([-1, 0, 1])
            alt_cell = self.environment.get_cell(
                self.grace.x + alt_dx,
                self.grace.y + alt_dy
            )
            if alt_cell.astrophage_level <= 6:
                dx = alt_dx
                dy = alt_dy

        self.grace.move(dx, dy, self.environment)

    def _rocky_action(self):
        """Rocky AI decision making"""

        # Rocky always tries to communicate to build translation
        if self.rocky.translation_level < 100:
            self.rocky.communicate(self.grace)

        # Share knowledge when trust is high enough
        if self.rocky.trust_level >= 20:
            self.rocky.share_knowledge(self.grace)

        # Assist experiments when trust is high enough
        if self.rocky.trust_level >= 30 and self.grace.taumoeba_samples >= 1:
            self.rocky.assist_experiment(self.grace)

        # Transfer fuel if Grace energy is getting low
        if self.grace.energy < 30 and self.rocky.trust_level >= 50:
            self.grace.energy = self.rocky.transfer_fuel(self.grace.energy)

        # Perform repairs if Grace energy is critically low
        if self.grace.energy < 20 and self.rocky.trust_level >= 40:
            self.rocky.perform_repair(self.grace)

        # Rocky rests if his own energy is low
        if self.rocky.energy < 20:
            self.rocky.rest()

    def _deploy_probe(self):
        """Deploy a beetle probe carrying current knowledge"""
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
            print(f"🛸 Beetle probe {probe.name} launched!")
            print(f"   Carrying {probe.knowledge_payload} knowledge units to Earth!")
        else:
            print("No probes available to deploy!")

    def _check_conditions(self):
        """Check win and lose conditions every turn"""

        # Win condition: Taumoeba viable AND a probe reached Earth
        if self.taumoeba.is_viable() and any(
                p.reached_earth for p in self.beetle_probes
        ):
            self.mission_success = True
            print("\n🌍 ============================================")
            print("   MISSION SUCCESS! EARTH IS SAVED!")
            print("   Taumoeba solution transmitted to humanity!")
            print("============================================ 🌍\n")

        # Lose condition 1: Grace runs out of energy
        if self.grace.energy <= 0:
            self.mission_aborted = True
            print("\n💀 MISSION ABORTED! Grace has run out of energy!")

        # Lose condition 2: Grace health depleted
        if self.grace.health <= 0:
            self.mission_aborted = True
            print("\n💀 MISSION ABORTED! Grace has died from Astrophage exposure!")

        # Lose condition 3: All experiments failed
        if (len(self.grace.experiment_log) >= 5 and
                self.grace.experiment_log.count("failure") == len(
                    self.grace.experiment_log
                )):
            self.mission_aborted = True
            print("\n💀 MISSION ABORTED! All experiments failed!")

    def print_status(self):
        """Print full status of all agents"""
        self.grace.status()
        self.rocky.status()
        self.taumoeba.status()
        if self.beetle_probes:
            print("--- Beetle Probes ---")
            for probe in self.beetle_probes:
                probe.status()

    def run(self, max_turns=50):
        """Run the full simulation"""
        print("=" * 50)
        print("🚀  HAIL MARY MISSION BEGINS  🚀")
        print("=" * 50)
        print("\nGrace wakes from coma...")
        print("He doesn't know who he is or where he is...")
        print("Two crewmates are dead.")
        print("The mission must go on.\n")

        self.environment.display()

        while (self.turn < max_turns
               and not self.mission_success
               and not self.mission_aborted):
            self.step()

            # Print full status every 10 turns
            if self.turn % 10 == 0:
                self.print_status()
                self.environment.display()

        # Final summary
        print(f"\n{'=' * 50}")
        print(f"SIMULATION ENDED AT TURN {self.turn}")
        print(f"{'=' * 50}")
        print(f"Mission Success:  {self.mission_success}")
        print(f"Mission Aborted:  {self.mission_aborted}")
        print(f"Final Knowledge:  {self.grace.knowledge}")
        print(f"Probes Deployed:  {self.probe_counter}")
        print(f"Taumoeba viable:  {self.taumoeba.is_viable()}")
        print(f"Taumoeba Earth survival rate: "
              f"{self.taumoeba.survival_rate_earth:.1%}")
        self.print_status()