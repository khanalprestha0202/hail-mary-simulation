import random
from src.environment import Environment, ASTROPHAGE, ADRIAN, TAUMOEBA, HAIL_MARY, BLIP_A
from src.agents import Grace, Rocky, BeetleProbe
from src.experiments import ExperimentManager


class Simulation:
    """Main simulation controller — turn-based multi-agent system"""

    def __init__(self, max_turns=100, seed=None):
        if seed is not None:
            random.seed(seed)
        self.max_turns        = max_turns
        self.turn             = 0
        self.environment      = Environment(25, 25)
        self.grace            = Grace(5, 5)
        self.rocky            = Rocky(5, 8)
        self.experiment_manager = ExperimentManager()
        self.beetle_probes    = []
        self.log              = []
        self.mission_success  = False
        self.abort            = False
        self.equipment_failure_turns = []  # turns where random failures occurred

        self.metrics = {
            "turns":              [],
            "grace_health":       [],
            "grace_energy":       [],
            "knowledge_score":    [],
            "taumoeba_viability": [],
            "mission_progress":   [],
            "rocky_cooperation":  [],
            "astrophage_spread":  [],
            "translation_level":  [],
            "equipment_degradation": [],
        }

    # ── logging ───────────────────────────────
    def _log(self, msg):
        self.log.append(f"[Turn {self.turn:03d}] {msg}")

    # ── helpers ───────────────────────────────
    def _count_astrophage(self):
        count = 0
        for row in self.environment.grid:
            for cell in row:
                if cell == ASTROPHAGE:
                    count += 1
        return count

    # ── random equipment failures ─────────────
    def _check_equipment_failure(self):
        """Random equipment failures add realism — increases over time"""
        failure_chance = 0.03 + (self.grace.equipment_degradation / 1000)
        if random.random() < failure_chance:
            severity = random.randint(5, 20)
            self.grace.equipment_degradation = min(100,
                self.grace.equipment_degradation + severity)
            self.grace.use_energy(severity // 2)
            self.equipment_failure_turns.append(self.turn)
            self._log(f"EQUIPMENT FAILURE! Degradation +{severity}. "
                      f"Total: {self.grace.equipment_degradation}%")

    # ── Grace AI ──────────────────────────────
    def _grace_ai_action(self):
        actions = []

        # Priority 1: Rest if critically low energy
        if self.grace.energy < 20:
            self.grace.rest()
            actions.append("Grace rests to recover energy and health.")
            return actions

        # Priority 2: Repair if equipment badly degraded
        if self.grace.equipment_degradation > 65:
            msg = self.grace.repair_equipment(self.rocky)
            actions.append(f"Grace repairs equipment: {msg}")
            return actions

        # Priority 3: Use tunnel to visit Rocky if trust high enough
        if (self.rocky.tunnel_built
                and self.grace.rocky_trust >= 30
                and not self.grace.in_tunnel
                and self.turn % 15 == 0
                and self.grace.energy > 40):
            ok, msg = self.grace.enter_tunnel()
            if ok:
                actions.append(msg)
                # While in tunnel — share experiment data with Rocky
                self.rocky.cooperation_level = min(100,
                    self.rocky.cooperation_level + 5)
                self.grace.knowledge_score += 3
                actions.append("Grace and Rocky exchange experimental data "
                                "through the tunnel interface.")
                self.grace.exit_tunnel()
                actions.append("Grace returns to Hail Mary.")

        # Priority 4: EVA if needed to collect samples and energy sufficient
        current = self.environment.get_cell(self.grace.row, self.grace.col)
        if current in (ADRIAN, TAUMOEBA) and self.grace.taumoeba_samples == 0:
            msg = self.grace.perform_eva(self.environment)
            actions.append(msg)
            msg2 = self.grace.collect_sample(self.environment)
            actions.append(msg2)

        # Priority 5: Collect sample from current cell
        elif current in (ASTROPHAGE, ADRIAN, TAUMOEBA):
            msg = self.grace.collect_sample(self.environment)
            actions.append(msg)

        # Priority 6: Run experiment every 3 turns if we have samples
        if self.grace.taumoeba_samples > 0 and self.turn % 3 == 0:
            result, notes = self.experiment_manager.run_experiment(
                self.grace, self.rocky, self.turn
            )
            if result:
                actions.append(
                    f"EXPERIMENT [{result.outcome.upper()}]: {notes}"
                )

        # Priority 7: Deploy beetle probe when ready
        if (self.grace.knowledge_score >= 30
                and self.grace.probes_deployed < 4
                and self.grace.taumoeba_viability >= 0.2 * (self.grace.probes_deployed + 1)
                and self.grace.beetle_probes > 0):
            threshold = 25 + self.grace.probes_deployed * 15
            ok, msg = self.grace.deploy_beetle_probe(threshold)
            if ok:
                probe_names = ["John", "Paul", "George", "Ringo"]
                pname = probe_names[self.grace.probes_deployed - 1]
                probe = BeetleProbe(
                    pname,
                    self.grace.row, self.grace.col,
                    self.grace.knowledge_score,
                    round(self.grace.taumoeba_viability * 100, 1),
                )
                self.beetle_probes.append(probe)
                actions.append(msg)

        # Priority 8: Navigate — toward Adrian if no Taumoeba yet
        if self.grace.taumoeba_samples == 0:
            dr = 12 - self.grace.row
            dc = 12 - self.grace.col
            direction = ("down" if dr > 0 else "up") if abs(dr) >= abs(dc) \
                   else ("right" if dc > 0 else "left")
            drain = self.grace.move(direction, self.environment)
            actions.append(
                f"Grace moves {direction} toward Adrian. Drain: {drain}"
            )
        else:
            direction = random.choice(["up", "down", "left", "right"])
            drain = self.grace.move(direction, self.environment)
            actions.append(f"Grace moves {direction}. Drain: {drain}")

        # Flashbacks
        for fb in self.grace.check_flashbacks():
            actions.append(fb)
            self.grace.knowledge_score += 3

        return actions

    # ── win / abort conditions ─────────────────
    def _check_win(self):
        if (self.grace.taumoeba_viability >= 0.8
                and self.grace.probes_deployed >= 2
                and self.grace.knowledge_score >= 80):
            self.mission_success = True
            return True
        return False

    def _check_abort(self):
        if not self.grace.is_alive():
            self.abort = True
            self._log("MISSION ABORT: Grace has perished.")
            return True
        return False

    # ── metrics ───────────────────────────────
    def _record_metrics(self):
        self.metrics["turns"].append(self.turn)
        self.metrics["grace_health"].append(self.grace.health)
        self.metrics["grace_energy"].append(self.grace.energy)
        self.metrics["knowledge_score"].append(self.grace.knowledge_score)
        self.metrics["taumoeba_viability"].append(
            round(self.grace.taumoeba_viability * 100, 2))
        self.metrics["mission_progress"].append(self.grace.mission_progress)
        self.metrics["rocky_cooperation"].append(self.rocky.cooperation_level)
        self.metrics["astrophage_spread"].append(self._count_astrophage())
        self.metrics["translation_level"].append(self.rocky.translation_level)
        self.metrics["equipment_degradation"].append(
            self.grace.equipment_degradation)

    # ── single step ───────────────────────────
    def step(self):
        self.turn += 1
        self.environment.step()

        # Grace acts
        for action in self._grace_ai_action():
            self._log(action)

        # Rocky acts autonomously
        for action in self.rocky.autonomous_action(self.grace, self.environment):
            self._log(action)

        # Beetle probes navigate and transmit
        for probe in self.beetle_probes:
            arrived, msg = probe.transmit(self.environment)
            if arrived:
                self._log(f"*** {msg} ***")
                self.grace.mission_progress += 20
            elif self.turn % 5 == 0:
                self._log(msg)

        # Environmental hazard on Grace's current cell
        drain = self.environment.get_energy_drain(self.grace.row, self.grace.col)
        if drain > 0:
            self.grace.use_energy(drain)
            self._log(f"Hazard! Grace loses {drain} energy.")

        # Random equipment failure check
        self._check_equipment_failure()

        # Record metrics
        self._record_metrics()

        # Win / abort
        if self._check_win():
            self._log("*** MISSION SUCCESS! Viable Taumoeba strain transmitted to Earth! ***")
        self._check_abort()

    # ── full run ──────────────────────────────
    def run(self, verbose=False):
        self._log("Grace wakes from coma aboard the Hail Mary.")
        self._log("Memory: 0%. Location: Unknown. Mission: Unknown.")
        self._log("A second spacecraft detected nearby — designation: Blip-A.")

        while (self.turn < self.max_turns
               and not self.mission_success
               and not self.abort):
            self.step()
            if verbose and self.turn % 10 == 0:
                self.print_status()

        if not self.mission_success and not self.abort:
            self._log("Simulation ended: maximum turns reached.")

        return self.get_results()

    # ── results ───────────────────────────────
    def get_results(self):
        exp = self.experiment_manager.get_statistics()
        return {
            "turns_survived":       self.turn,
            "mission_success":      self.mission_success,
            "abort":                self.abort,
            "knowledge_score":      self.grace.knowledge_score,
            "taumoeba_viability":   round(self.grace.taumoeba_viability * 100, 2),
            "probes_deployed":      self.grace.probes_deployed,
            "mission_progress":     self.grace.mission_progress,
            "rocky_cooperation":    self.rocky.cooperation_level,
            "rocky_trust":          self.grace.rocky_trust,
            "tunnel_built":         self.rocky.tunnel_built,
            "translation_level":    self.rocky.translation_level,
            "eva_count":            self.grace.eva_count,
            "equipment_failures":   len(self.equipment_failure_turns),
            "total_experiments":    exp.get("total_experiments", 0),
            "success_rate":         exp.get("success_rate", 0),
            "final_strategy":       exp.get("current_strategy", "N/A"),
            "grace_health":         self.grace.health,
            "grace_energy":         self.grace.energy,
            "metrics":              self.metrics,
            "experiment_stats":     exp,
            "chord_log":            self.rocky.chord_log,
        }

    def print_status(self):
        gs = self.grace.get_status()
        rs = self.rocky.get_status()
        print(f"\n{'='*60}")
        print(f"TURN {self.turn:03d} | Knowledge: {gs['knowledge_score']:4d} | "
              f"Viability: {gs['taumoeba_viability']:5.1f}%")
        print(f"Grace  | HP:{gs['health']:3d} | EN:{gs['energy']:3d} | "
              f"EVAs:{gs['eva_count']} | Equip degr:{gs['equipment_degradation']}%")
        print(f"Rocky  | Coop:{rs['cooperation_level']:3d} | "
              f"Trans:{rs['translation_level']:3d} | "
              f"Tunnel:{'YES' if rs['tunnel_built'] else 'no'}")
        print(f"Probes deployed: {gs['probes_deployed']}/4 | "
              f"In tunnel: {gs['in_tunnel']}")
        if rs['chord_log']:
            print(f"Last chord: {rs['chord_log'][-1]}")
        print(f"{'='*60}")