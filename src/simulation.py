import random
from src.environment import Environment
from src.agents import Grace, Rocky, BeetleProbe
from src.experiments import ExperimentManager

class Simulation:
    """Main simulation controller"""

    def __init__(self, max_turns=100, seed=None):
        if seed is not None:
            random.seed(seed)
        self.max_turns = max_turns
        self.turn = 0
        self.environment = Environment(25, 25)
        self.grace = Grace(5, 5)
        self.rocky = Rocky(5, 8)
        self.experiment_manager = ExperimentManager()
        self.beetle_probes = []
        self.log = []
        self.mission_success = False
        self.abort = False

        # Metrics tracking for graphs
        self.metrics = {
            "turns": [],
            "grace_health": [],
            "grace_energy": [],
            "knowledge_score": [],
            "taumoeba_viability": [],
            "mission_progress": [],
            "rocky_cooperation": [],
            "astrophage_spread": [],
        }

    def _log(self, message):
        entry = f"[Turn {self.turn:03d}] {message}"
        self.log.append(entry)

    def _count_astrophage(self):
        from src.environment import ASTROPHAGE
        count = 0
        for row in self.environment.grid:
            for cell in row:
                if cell == ASTROPHAGE:
                    count += 1
        return count

    def _grace_ai_action(self):
        """AI decision making for Grace each turn"""
        from src.environment import ASTROPHAGE, ADRIAN, TAUMOEBA, HAIL_MARY

        actions_taken = []

        # Priority 1: Rest if energy critically low
        if self.grace.energy < 20:
            self.grace.rest()
            actions_taken.append("Grace rests to recover energy.")
            return actions_taken

        # Priority 2: Repair equipment if badly degraded
        if self.grace.equipment_degradation > 70:
            msg = self.grace.repair_equipment(self.rocky)
            actions_taken.append(f"Grace repairs equipment: {msg}")
            return actions_taken

        # Priority 3: Collect samples if near Adrian or Astrophage
        current_cell = self.environment.get_cell(self.grace.row, self.grace.col)
        if current_cell in (ADRIAN, TAUMOEBA, ASTROPHAGE):
            msg = self.grace.collect_sample(self.environment)
            actions_taken.append(msg)

        # Priority 4: Experiment if we have samples
        if self.grace.taumoeba_samples > 0 and self.turn % 3 == 0:
            result, notes = self.experiment_manager.run_experiment(
                self.grace, self.rocky, self.turn
            )
            if result:
                actions_taken.append(f"Experiment [{result.outcome.upper()}]: {notes}")

        # Priority 5: Deploy beetle probe when knowledge is sufficient
        if (self.grace.knowledge_score >= 30 and
                self.grace.probes_deployed < 4 and
                self.grace.taumoeba_viability >= 0.25 * (self.grace.probes_deployed + 1)):
            success, msg = self.grace.deploy_beetle_probe(
                knowledge_threshold=25 + self.grace.probes_deployed * 15
            )
            if success:
                probe_name = ["John", "Paul", "George", "Ringo"][self.grace.probes_deployed - 1]
                probe = BeetleProbe(probe_name, self.grace.row, self.grace.col, self.grace.knowledge_score)
                self.beetle_probes.append(probe)
                actions_taken.append(msg)

        # Priority 6: Move towards Adrian if no Taumoeba samples yet
        if self.grace.taumoeba_samples == 0:
            # Move toward Adrian (12,12)
            dr = 12 - self.grace.row
            dc = 12 - self.grace.col
            if abs(dr) > abs(dc):
                direction = "down" if dr > 0 else "up"
            else:
                direction = "right" if dc > 0 else "left"
            drain = self.grace.move(direction, self.environment)
            actions_taken.append(f"Grace moves {direction} toward Adrian. Energy drain: {drain}")
        else:
            # Move somewhat randomly once we have samples
            direction = random.choice(["up", "down", "left", "right"])
            drain = self.grace.move(direction, self.environment)
            actions_taken.append(f"Grace moves {direction}. Energy drain: {drain}")

        # Check flashbacks
        flashbacks = self.grace.check_flashbacks()
        for fb in flashbacks:
            actions_taken.append(fb)
            self.grace.knowledge_score += 3

        return actions_taken

    def _check_win_condition(self):
        """Check if the mission is complete"""
        if (self.grace.taumoeba_viability >= 0.8 and
                self.grace.probes_deployed >= 2 and
                self.grace.knowledge_score >= 80):
            self.mission_success = True
            return True
        return False

    def _check_abort_condition(self):
        """Check if mission must be aborted"""
        if not self.grace.is_alive():
            self.abort = True
            self._log("MISSION ABORT: Grace has perished. Simulation ends.")
            return True
        if self.grace.mission_progress < 0:
            self.abort = True
            self._log("MISSION ABORT: Mission progress critically negative.")
            return True
        return False

    def _record_metrics(self):
        self.metrics["turns"].append(self.turn)
        self.metrics["grace_health"].append(self.grace.health)
        self.metrics["grace_energy"].append(self.grace.energy)
        self.metrics["knowledge_score"].append(self.grace.knowledge_score)
        self.metrics["taumoeba_viability"].append(round(self.grace.taumoeba_viability * 100, 2))
        self.metrics["mission_progress"].append(self.grace.mission_progress)
        self.metrics["rocky_cooperation"].append(self.rocky.cooperation_level)
        self.metrics["astrophage_spread"].append(self._count_astrophage())

    def step(self):
        """Run one turn of the simulation"""
        self.turn += 1
        self.environment.step()

        # Grace acts
        grace_actions = self._grace_ai_action()
        for action in grace_actions:
            self._log(action)

        # Rocky acts autonomously
        rocky_actions = self.rocky.autonomous_action(self.grace, self.environment)
        for action in rocky_actions:
            self._log(action)

        # Update beetle probes
        for probe in self.beetle_probes:
            msg = probe.transmit()
            if "reached Earth" in msg:
                self._log(f"*** {msg} ***")
                self.grace.mission_progress += 20

        # Apply environmental effects on Grace
        drain = self.environment.get_energy_drain(self.grace.row, self.grace.col)
        if drain > 0:
            self.grace.use_energy(drain)
            self._log(f"Environmental hazard! Grace loses {drain} energy.")

        # Record metrics
        self._record_metrics()

        # Check win/abort
        if self._check_win_condition():
            self._log("*** MISSION SUCCESS! Taumoeba strain viable. Data transmitted to Earth! ***")
        self._check_abort_condition()

    def run(self, verbose=False):
        """Run full simulation"""
        self._log("Simulation started. Grace wakes from coma aboard the Hail Mary.")
        self._log("Memory: 0%. Location: Unknown. Mission: Unknown.")

        while self.turn < self.max_turns and not self.mission_success and not self.abort:
            self.step()
            if verbose and self.turn % 10 == 0:
                self.print_status()

        if not self.mission_success and not self.abort:
            self._log("Simulation ended: Maximum turns reached.")

        return self.get_results()

    def get_results(self):
        """Return final simulation results"""
        exp_stats = self.experiment_manager.get_statistics()
        return {
            "turns_survived": self.turn,
            "mission_success": self.mission_success,
            "abort": self.abort,
            "knowledge_score": self.grace.knowledge_score,
            "taumoeba_viability": round(self.grace.taumoeba_viability * 100, 2),
            "probes_deployed": self.grace.probes_deployed,
            "mission_progress": self.grace.mission_progress,
            "rocky_cooperation": self.rocky.cooperation_level,
            "rocky_trust": self.grace.rocky_trust,
            "total_experiments": exp_stats.get("total_experiments", 0),
            "success_rate": exp_stats.get("success_rate", 0),
            "final_strategy": exp_stats.get("current_strategy", "N/A"),
            "grace_health": self.grace.health,
            "grace_energy": self.grace.energy,
            "metrics": self.metrics,
            "experiment_stats": exp_stats,
        }

    def print_status(self):
        gs = self.grace.get_status()
        rs = self.rocky.get_status()
        print(f"\n{'='*55}")
        print(f"TURN {self.turn} | Knowledge: {gs['knowledge_score']} | "
              f"Viability: {gs['taumoeba_viability']}%")
        print(f"Grace  | HP:{gs['health']:3d} | EN:{gs['energy']:3d} | "
              f"Progress:{gs['mission_progress']}")
        print(f"Rocky  | Cooperation:{rs['cooperation_level']:3d} | "
              f"Translation:{rs['translation_level']:3d}")
        print(f"Probes deployed: {gs['probes_deployed']}/4")
        print(f"{'='*55}")