import random
from environment import Environment
from agents.grace import Grace
from agents.rocky import Rocky
from entities.taumoeba import Taumoeba
from entities.beetle_probe import BeetleProbe
from visualiser import Visualiser


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
        self.earth_saved = False
        self.erid_saved = False
        self.rocky_ship_saved = False
        self.protocol_violations = 0
        self.equipment_failures = 0

    def step(self):
        """One complete simulation turn"""
        self.turn += 1
        print(f"\n========== TURN {self.turn} ==========")

        # Grace actions
        self._grace_action()

        # Rocky actions
        self._rocky_action()

        # Environment updates
        self.environment.spread_astrophage()

        # Equipment failure check
        if self.environment.trigger_equipment_failure():
            self.equipment_failures += 1
            if random.random() < 0.3:
                self.grace.equipment_damaged = True
                print("Equipment failure! "
                      "Grace's equipment damaged!")

        # Navigate beetle probes
        for probe in self.beetle_probes:
            probe.navigate()

        # Taumoeba consumes Astrophage near planet
        if self.taumoeba.is_viable_earth():
            self.taumoeba.consume_astrophage(
                self.environment, 5, 10
            )

        # Check Rocky's ship contamination
        if self.taumoeba.generation > 3:
            self.rocky.check_contamination(self.taumoeba)

        # Flashback event
        self.grace.flashback()

        # Mission protocol check
        self._check_protocol_violations()

        # Win/lose conditions
        self._check_conditions()

    def _grace_action(self):
        """Grace AI with priority-based decision making"""
        cell = self.environment.get_cell(
            self.grace.x, self.grace.y
        )

        # Repair equipment if damaged
        if self.grace.equipment_damaged:
            if self.rocky.trust_level >= 50:
                self.rocky.repair_grace_equipment(self.grace)
            else:
                self.grace.repair_equipment()
            return

        # Treat Rocky's contamination if critical
        if self.rocky.ship_contaminated:
            result = self.taumoeba.treat_contamination(
                self.grace, self.rocky
            )
            if result:
                self.rocky_ship_saved = True
            return

        # Priority 1: Rest if critically low energy
        if self.grace.energy < 15:
            self.grace.rest()

        # Priority 2: Deploy probe if Earth viable
        elif self.taumoeba.is_viable_earth():
            if self.probe_counter < 4:
                self._deploy_probe()
            # Also work on Erid strain
            elif (not self.taumoeba.is_viable_erid()
                  and self.grace.taumoeba_samples >= 2
                  and self.rocky.trust_level >= 50):
                self.taumoeba.breed_for_erid(
                    self.grace, self.rocky
                )

        # Priority 3: Breed Taumoeba for Earth
        elif (self.grace.taumoeba_samples >= 2
              and self.grace.knowledge >= 20):
            result = self.taumoeba.breed_for_earth(
                self.grace, self.rocky
            )
            if result:
                print("Taumoeba viable for Earth!")
                self._deploy_probe()

        # Priority 4: Collect on planet
        elif cell.cell_type == "planet":
            self.grace.collect_sample(self.environment)
            self.grace.collect_sample(self.environment)

        # Priority 5: Use tunnel to get more samples
        elif (self.grace.taumoeba_samples < 2
              and self.rocky.trust_level >= 30):
            self._move_grace_toward_planet()

        # Priority 6: Breed with 1 sample
        elif (self.grace.taumoeba_samples >= 1
              and self.grace.knowledge >= 20):
            self.taumoeba.breed_for_earth(
                self.grace, self.rocky
            )

        # Priority 7: Analyse data if have samples
        elif self.grace.astrophage_samples >= 3:
            self.grace.analyse_data()

        # Priority 8: Move toward planet
        else:
            self._move_grace_toward_planet()

    def _move_grace_toward_planet(self):
        """Smart pathfinding toward planet Adrian"""
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

        # Check hazards ahead
        next_cell = self.environment.get_cell(
            self.grace.x + dx,
            self.grace.y + dy
        )

        # Avoid deadly Astrophage
        if next_cell.astrophage_level > 6:
            # Try alternate routes
            alternatives = [
                (dx, 0), (0, dy),
                (dx, -dy), (-dx, dy)
            ]
            for alt_dx, alt_dy in alternatives:
                alt_cell = self.environment.get_cell(
                    self.grace.x + alt_dx,
                    self.grace.y + alt_dy
                )
                if alt_cell.astrophage_level <= 4:
                    dx, dy = alt_dx, alt_dy
                    break

        self.grace.move(dx, dy, self.environment)

    def _rocky_action(self):
        """Rocky AI with full cooperation mechanics"""
        # Build translation and trust
        if self.rocky.translation_level < 100:
            self.rocky.communicate(self.grace)

        # Share knowledge
        if self.rocky.trust_level >= 20:
            self.rocky.share_knowledge(self.grace)

        # Reconnaissance scan
        if self.turn % 5 == 0:
            self.rocky.conduct_reconnaissance(
                self.environment
            )

        # Assist experiments
        if (self.rocky.trust_level >= 30
                and self.grace.taumoeba_samples >= 1):
            self.rocky.assist_experiment(self.grace)

        # Transfer fuel if Grace energy low
        if (self.grace.energy < 30
                and self.rocky.trust_level >= 50):
            self.grace.energy = self.rocky.transfer_fuel(
                self.grace.energy
            )

        # Perform repairs
        if (self.grace.energy < 20
                and self.rocky.trust_level >= 40):
            self.rocky.perform_repair(self.grace)

        # Rocky moves for reconnaissance
        if (self.turn % 8 == 0
                and self.rocky.energy > 30):
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            self.rocky.move(dx, dy, self.environment)

        # Rocky rests if low energy
        if self.rocky.energy < 20:
            self.rocky.rest()

    def _deploy_probe(self):
        """Deploy beetle probe with configured payload"""
        if (self.probe_counter < 4
                and self.grace.beetle_probes > 0):
            probe = BeetleProbe(
                probe_id=self.probe_counter,
                x=self.grace.x,
                y=self.grace.y,
                knowledge_payload=self.grace.knowledge
            )
            # Configure stellar heading
            probe.configure(
                heading=-1,
                payload_boost=self.rocky.knowledge // 10
            )
            self.beetle_probes.append(probe)
            self.grace.beetle_probes -= 1
            self.probe_counter += 1
            print(f"Beetle probe {probe.name} launched!")
            print(f"Payload: {probe.knowledge_payload} "
                  f"knowledge units")
        else:
            print("No probes available!")

    def _check_protocol_violations(self):
        """Check mission protocol rules"""
        # Violation: wasting energy on nothing
        if (self.grace.energy > 80
                and self.grace.taumoeba_samples == 0
                and self.turn > 15):
            self.protocol_violations += 1
            if self.protocol_violations >= 3:
                self.grace.knowledge = max(
                    0, self.grace.knowledge - 5
                )
                print("Protocol violation: "
                      "Resource waste! Knowledge -5")

    def _check_conditions(self):
        """Check all win and lose conditions"""
        # Earth saved condition
        if (self.taumoeba.is_viable_earth()
                and any(p.reached_earth
                        for p in self.beetle_probes)):
            if not self.earth_saved:
                self.earth_saved = True
                print("\n=== EARTH IS SAVED! ===")
                print("Taumoeba solution transmitted!")

        # Erid saved condition
        if self.taumoeba.is_viable_erid():
            if not self.erid_saved:
                self.erid_saved = True
                print("\n=== ERID IS SAVED! ===")
                print("Rocky's home star is protected!")

        # Full mission success
        if self.earth_saved:
            self.mission_success = True
            if self.earth_saved and self.erid_saved:
                print("\n" + "=" * 50)
                print("COMPLETE MISSION SUCCESS!")
                print("Both Earth AND Erid are saved!")
                print("=" * 50)

        # Lose conditions
        if self.grace.energy <= 0:
            self.mission_aborted = True
            print("\nMISSION ABORTED! Grace out of energy!")

        if self.grace.health <= 0:
            self.mission_aborted = True
            print("\nMISSION ABORTED! Grace died!")

        if (len(self.taumoeba.breeding_log) >= 10
                and not self.taumoeba.is_viable_earth()):
            failures = sum(
                1 for e in self.taumoeba.breeding_log
                if e["result"] == "FAILURE"
            )
            if failures >= 8:
                self.mission_aborted = True
                print("\nMISSION ABORTED! "
                      "All experiments failed!")

    def print_status(self):
        """Print full status"""
        self.grace.status()
        self.rocky.status()
        self.taumoeba.status()
        if self.beetle_probes:
            print("--- Beetle Probes ---")
            for probe in self.beetle_probes:
                probe.status()
        print(f"\n--- Mission Status ---")
        print(f"Earth saved: {self.earth_saved}")
        print(f"Erid saved: {self.erid_saved}")
        print(f"Rocky's ship saved: {self.rocky_ship_saved}")
        print(f"Equipment failures: {self.equipment_failures}")
        print(f"Protocol violations: "
              f"{self.protocol_violations}")

    def run(self, max_turns=50):
        """Run with live matplotlib visualisation"""
        print("=" * 50)
        print("   HAIL MARY MISSION BEGINS")
        print("=" * 50)
        print("\nGrace wakes from coma...")
        print("He doesn't know who he is or where he is...")
        print("Two crewmates are dead.")
        print("The mission must go on.\n")

        vis = Visualiser(
            self.environment, self.grace, self.rocky
        )
        self.environment.display()

        while (self.turn < max_turns
               and not self.mission_success
               and not self.mission_aborted):
            self.step()
            vis.update(self.turn, self.taumoeba)
            if self.turn % 10 == 0:
                self.print_status()
                self.environment.display()

        self._print_summary()
        vis.show_final(
            self.mission_success,
            self.turn,
            self.grace.knowledge,
            self.probe_counter
        )

    def run_text_only(self, max_turns=100):
        """Run without graphics for statistics"""
        while (self.turn < max_turns
               and not self.mission_success
               and not self.mission_aborted):
            self.step()

    def _print_summary(self):
        print(f"\n{'=' * 50}")
        print(f"SIMULATION ENDED AT TURN {self.turn}")
        print(f"{'=' * 50}")
        print(f"Mission Success:  {self.mission_success}")
        print(f"Mission Aborted:  {self.mission_aborted}")
        print(f"Earth Saved:      {self.earth_saved}")
        print(f"Erid Saved:       {self.erid_saved}")
        print(f"Rocky Ship Saved: {self.rocky_ship_saved}")
        print(f"Final Knowledge:  {self.grace.knowledge}")
        print(f"Probes Deployed:  {self.probe_counter}")
        print(f"Earth survival:   "
              f"{self.taumoeba.survival_rate_earth:.1%}")
        print(f"Erid survival:    "
              f"{self.taumoeba.survival_rate_erid:.1%}")
        print(f"Equipment failures: "
              f"{self.equipment_failures}")
        self.print_status()