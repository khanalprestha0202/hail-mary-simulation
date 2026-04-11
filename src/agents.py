import random


class Agent:
    """Base class for all agents in the simulation"""
    def __init__(self, name, row, col):
        self.name   = name
        self.row    = row
        self.col    = col
        self.health = 100
        self.energy = 100
        self.alive  = True

    def is_alive(self):
        return self.alive and self.health > 0 and self.energy > 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.alive = False

    def use_energy(self, amount):
        self.energy = max(0, self.energy - amount)
        if self.energy <= 0:
            self.alive = False

    def rest(self):
        """Rest to recover energy and health"""
        self.energy = min(120, self.energy + 20)
        self.health = min(110, self.health + 8)


# ─────────────────────────────────────────────
#  GRACE
# ─────────────────────────────────────────────
class Grace(Agent):
    """
    Dr. Ryland Grace — central human agent.

    Wakes from coma with no memory. Progressively recovers mission context
    through flashback events tied to knowledge milestones. Must navigate
    the Tau Ceti system, collect samples, conduct experiments, cooperate
    with Rocky, and deploy beetle probes before energy or health runs out.
    """

    FLASHBACK_EVENTS = [
        (10, "FLASHBACK: Eva Stratt briefs you. Astrophage is consuming the Sun. Earth has decades left."),
        (20, "FLASHBACK: You volunteered for a one-way mission. You knew you would never return."),
        (35, "FLASHBACK: Launch day. Billions watched the Hail Mary leave Earth. You were already in your coma."),
        (50, "FLASHBACK: Eva's last words — 'Grace, whatever you find, transmit it. Don't come home empty.'"),
        (70, "FLASHBACK: Your students. You promised them there would be a world to grow up in."),
        (90, "FLASHBACK: Memory fully restored. You are Dr. Ryland Grace. Humanity's last hope."),
    ]

    def __init__(self, row, col):
        super().__init__("Dr. Ryland Grace", row, col)
        # Start with slightly higher stamina — Grace is a trained astronaut
        self.energy = 120
        self.health = 110

        self.knowledge_score       = 0
        self.astrophage_samples    = 0
        self.taumoeba_samples      = 0
        self.taumoeba_viability    = 0.0
        self.beetle_probes         = 4
        self.probes_deployed       = 0
        self.mission_progress      = 0
        self.memory_restored       = 0
        self.experiment_log        = []
        self.flashbacks_triggered  = set()
        self.rocky_trust           = 0
        self.in_tunnel             = False  # inside xenonite tunnel
        self.equipment_degradation = 0     # 0-100, higher = worse
        self.eva_count             = 0     # number of EVAs performed

    # ── movement ──────────────────────────────
    def move(self, direction, environment):
        """Move one cell in given direction — costs energy, more in hazardous cells"""
        dr, dc = {"up": (-1, 0), "down": (1, 0),
                  "left": (0, -1), "right": (0, 1)}.get(direction, (0, 0))
        new_row = (self.row + dr) % environment.height
        new_col = (self.col + dc) % environment.width
        drain   = environment.get_energy_drain(new_row, new_col)
        cost    = 4 + drain if self.in_tunnel else 2 + drain
        self.use_energy(cost)
        self.health = max(0, self.health - drain // 2)
        self.row, self.col = new_row, new_col
        return drain

    def enter_tunnel(self):
        """Grace enters the pressurised xenonite tunnel connecting ships"""
        if self.energy < 10:
            return False, "Not enough energy to enter the tunnel."
        self.in_tunnel = True
        self.use_energy(5)
        return True, "Grace enters the pressurised xenonite tunnel connecting Hail Mary to Blip-A."

    def exit_tunnel(self):
        """Grace exits the xenonite tunnel back to Hail Mary"""
        self.in_tunnel = False
        self.use_energy(3)
        return "Grace exits the tunnel back into the Hail Mary."

    def perform_eva(self, environment):
        """
        Extra-vehicular activity — costly but necessary to collect samples.
        Costs energy and health; increases equipment degradation.
        """
        self.eva_count += 1
        self.use_energy(15)
        self.take_damage(4)
        self.equipment_degradation += 4
        drain = environment.get_energy_drain(self.row, self.col)
        if drain > 0:
            self.use_energy(drain)
            self.take_damage(drain // 2)
        return f"EVA #{self.eva_count} complete. Exposed to space environment."

    # ── samples ───────────────────────────────
    def collect_sample(self, environment):
        """Collect Astrophage or Taumoeba sample from current cell"""
        from src.environment import ASTROPHAGE, ADRIAN, TAUMOEBA
        cell = environment.get_cell(self.row, self.col)
        if cell == ASTROPHAGE:
            self.astrophage_samples += 1
            self.use_energy(5)
            self.knowledge_score += 2
            return "Collected Astrophage sample."
        elif cell in (ADRIAN, TAUMOEBA):
            self.taumoeba_samples += 1
            self.use_energy(8)
            self.knowledge_score += 5
            return "Collected Taumoeba sample from Adrian's atmosphere!"
        return "Nothing to collect here."

    # ── experiment ────────────────────────────
    def conduct_experiment(self, rocky=None):
        """
        Direct experiment method — used for simple cases.
        Main simulation uses ExperimentManager with Q-learning instead.
        """
        if self.taumoeba_samples == 0 and self.astrophage_samples == 0:
            return "experiment_fail", "No samples available."
        self.use_energy(10)
        self.equipment_degradation = min(100, self.equipment_degradation + 2)
        base = 0.3 + self.knowledge_score / 300
        if rocky and rocky.is_alive():
            base += 0.15 + rocky.engineering_skill / 200
        roll = random.random()
        if roll < base * 0.4:
            outcome, gain, vgain = "failure", 1, -0.01
            msg = "Experiment failed. Recording results for future reference."
        elif roll < base * 0.8:
            outcome, gain, vgain = "partial", 4, 0.05
            msg = "Partial success! Taumoeba survived briefly."
        else:
            outcome, gain, vgain = "success", 10, 0.15
            msg = "SUCCESS! Taumoeba strain showing strong viability!"
            self.mission_progress += 5
        self.knowledge_score   += gain
        self.taumoeba_viability = min(1.0, max(0.0, self.taumoeba_viability + vgain))
        self.experiment_log.append({
            "outcome":   outcome,
            "viability": round(self.taumoeba_viability, 3),
            "knowledge": self.knowledge_score,
        })
        return outcome, msg

    # ── beetle probes ─────────────────────────
    def deploy_beetle_probe(self, knowledge_threshold=25):
        """
        Deploy a beetle probe to transmit findings to Earth.
        Requires minimum knowledge threshold before deployment.
        Probe names: John, Paul, George, Ringo (in order).
        """
        if self.beetle_probes == 0:
            return False, "No beetle probes remaining."
        if self.knowledge_score < knowledge_threshold:
            return False, f"Need {knowledge_threshold} knowledge points first."
        self.beetle_probes   -= 1
        self.probes_deployed += 1
        self.mission_progress += 15
        self.use_energy(8)
        names = ["John", "Paul", "George", "Ringo"]
        name  = names[self.probes_deployed - 1] if self.probes_deployed <= 4 \
                else f"Probe-{self.probes_deployed}"
        return True, (f"Beetle probe '{name}' deployed! "
                      f"Transmitting {self.knowledge_score} knowledge points to Earth.")

    # ── repair ────────────────────────────────
    def repair_equipment(self, rocky=None):
        """Repair equipment — Rocky's assistance significantly improves outcome"""
        self.use_energy(12)
        if rocky and rocky.is_alive():
            amt = random.randint(18, 35)
            self.equipment_degradation = max(0, self.equipment_degradation - amt)
            return f"Rocky assisted repair. Degradation reduced by {amt}."
        amt = random.randint(5, 15)
        self.equipment_degradation = max(0, self.equipment_degradation - amt)
        return f"Self-repair completed. Degradation reduced by {amt}."

    # ── flashbacks ────────────────────────────
    def check_flashbacks(self):
        """
        Check if any flashback events should trigger based on knowledge score.
        Each flashback restores memory and grants bonus knowledge.
        """
        msgs = []
        for threshold, msg in self.FLASHBACK_EVENTS:
            if (self.knowledge_score >= threshold
                    and threshold not in self.flashbacks_triggered):
                self.flashbacks_triggered.add(threshold)
                self.memory_restored = min(100, self.memory_restored + 15)
                msgs.append(msg)
        return msgs

    def get_status(self):
        return {
            "name":                  self.name,
            "position":              (self.row, self.col),
            "health":                self.health,
            "energy":                self.energy,
            "knowledge_score":       self.knowledge_score,
            "taumoeba_viability":    round(self.taumoeba_viability * 100, 1),
            "astrophage_samples":    self.astrophage_samples,
            "taumoeba_samples":      self.taumoeba_samples,
            "beetle_probes_left":    self.beetle_probes,
            "probes_deployed":       self.probes_deployed,
            "mission_progress":      self.mission_progress,
            "memory_restored":       self.memory_restored,
            "equipment_degradation": self.equipment_degradation,
            "rocky_trust":           self.rocky_trust,
            "in_tunnel":             self.in_tunnel,
            "eva_count":             self.eva_count,
        }


# ─────────────────────────────────────────────
#  ROCKY
# ─────────────────────────────────────────────
class Rocky(Agent):
    """
    Rocky — Eridian alien agent aboard the Blip-A.

    A five-limbed alien from 40 Eridani whose home star faces the same
    Astrophage threat as Earth. Communicates through sonar chord patterns
    that Grace progressively learns to understand. Cannot survive in Grace's
    oxygen atmosphere without the pressurised xenonite tunnel.

    Rocky's goals are aligned but not identical to Grace's — saving Erid
    matters as much to Rocky as saving Earth matters to Grace.
    """

    # Sonar chord vocabulary — unlocks progressively as translation improves
    CHORD_LIBRARY = [
        (0,   "♪♩♫",  "???  ???  ???"),
        (5,   "♫♩♪",  "Danger... star... sick."),
        (10,  "♩♫♩",  "Same problem. My star. Also sick."),
        (18,  "♪♫♩♪", "I help you. You help me. Deal?"),
        (25,  "♩♩♫♫", "Xenonite tunnel — safe passage between ships."),
        (35,  "♫♪♩♫", "Astrophage data from Erid — sharing now."),
        (45,  "♪♩♪♩", "Taumoeba! I have seen similar. Erid atmosphere different."),
        (55,  "♫♫♩♩", "My tools better for repair. I fix your ship."),
        (65,  "♩♪♫♪", "Fuel low. But I share. Friend more important."),
        (80,  "♪♪♩♫", "Earth and Erid both saved. This good outcome."),
        (100, "♫♩♩♪", "You are good human, Grace. Rocky trust you completely."),
    ]

    def __init__(self, row, col):
        super().__init__("Rocky (Eridian)", row, col)
        self.engineering_skill = 80
        self.fuel_reserves     = 120  # Rocky starts with more fuel
        self.shared_knowledge  = 0
        self.cooperation_level = 0
        self.translation_level = 0   # 0-100: shared language progress
        self.repairs_done      = 0
        self.energy_shared     = 0
        self.tunnel_built      = False
        self.chord_log         = []  # full record of all communications

    # ── sonar chord communication ─────────────
    def _get_chord(self):
        """Return most advanced chord Rocky can currently express"""
        best = self.CHORD_LIBRARY[0]
        for min_trans, chord, meaning in self.CHORD_LIBRARY:
            if self.translation_level >= min_trans:
                best = (min_trans, chord, meaning)
        return best

    def communicate(self, grace):
        """
        Rocky sends a sonar chord pattern.
        Translation improves each exchange — shared language builds over time.
        """
        _, chord, meaning = self._get_chord()
        self.translation_level = min(100, self.translation_level + 6)
        grace.rocky_trust      = min(100, grace.rocky_trust + 5)
        self.cooperation_level = min(100, self.cooperation_level + 4)
        grace.knowledge_score += 2
        entry = f"{chord}  [{meaning}]"
        self.chord_log.append(entry)
        return entry

    # ── xenonite tunnel ───────────────────────
    def build_tunnel(self, grace):
        """
        Rocky engineers the pressurised xenonite tunnel connecting both ships.
        Enables Grace to visit Rocky's ship safely despite atmospheric incompatibility.
        """
        if self.tunnel_built:
            return "Tunnel already established."
        if self.fuel_reserves < 20:
            return "Insufficient fuel reserves to build tunnel."
        self.fuel_reserves    -= 15
        self.tunnel_built      = True
        self.cooperation_level = min(100, self.cooperation_level + 20)
        grace.rocky_trust      = min(100, grace.rocky_trust + 15)
        grace.knowledge_score += 8
        return ("Rocky engineers a pressurised xenonite tunnel connecting "
                "Blip-A to Hail Mary. Grace can now visit Rocky's ship safely!")

    # ── knowledge sharing ─────────────────────
    def share_knowledge(self, grace):
        """Share Eridian star maps and Astrophage research data with Grace"""
        if self.fuel_reserves < 10:
            return "Rocky: energy too low to transmit data."
        gained = random.randint(8, 20)
        grace.knowledge_score  += gained
        self.shared_knowledge  += gained
        self.cooperation_level  = min(100, self.cooperation_level + 8)
        grace.rocky_trust       = min(100, grace.rocky_trust + 5)
        self.use_energy(5)
        return f"Rocky shares Eridian star maps and Astrophage research. +{gained} knowledge!"

    # ── engineering repair ────────────────────
    def perform_repair(self, grace):
        """Rocky performs precision xenonite repair on Grace's equipment"""
        if self.fuel_reserves < 15:
            return "Rocky: fuel reserves too low for repair tools."
        self.fuel_reserves    -= 10
        self.repairs_done     += 1
        amt = random.randint(20, 40)
        grace.equipment_degradation = max(0, grace.equipment_degradation - amt)
        self.cooperation_level = min(100, self.cooperation_level + 10)
        return f"Rocky performs precision xenonite repair. Equipment improved by {amt} points!"

    # ── fuel sharing ──────────────────────────
    def share_fuel(self, grace):
        """Transfer Astrophage fuel to Grace's ship"""
        if self.fuel_reserves < 20:
            return "Rocky: not enough fuel reserves to share safely."
        amount = min(30, self.fuel_reserves - 10)
        self.fuel_reserves -= amount
        grace.energy        = min(120, grace.energy + amount)
        self.energy_shared += amount
        self.cooperation_level = min(100, self.cooperation_level + 12)
        grace.rocky_trust      = min(100, grace.rocky_trust + 8)
        return f"Rocky transfers {amount} units of Astrophage fuel to Hail Mary!"

    # ── autonomous turn logic ─────────────────
    def autonomous_action(self, grace, environment):
        """
        Rocky's priority-based autonomous decision making each turn.
        Priorities reflect Rocky's aligned-but-distinct goals:
        1. Build tunnel (enables cooperation)
        2. Communicate (build shared language)
        3. Emergency fuel transfer (keep Grace alive)
        4. Share knowledge (advance science)
        5. Repair equipment (maintain capability)
        """
        actions = []

        # Priority 1: Build xenonite tunnel as soon as cooperation allows
        if not self.tunnel_built and self.cooperation_level >= 8:
            msg = self.build_tunnel(grace)
            actions.append(f"[ROCKY — ENGINEERING] {msg}")

        # Priority 2: Communicate to develop shared language
        if self.translation_level < 70 and random.random() < 0.60:
            msg = self.communicate(grace)
            actions.append(f"[ROCKY — SONAR CHORD] {msg}")

        # Priority 3: Emergency fuel transfer if Grace critically low
        if grace.energy < 30 and self.fuel_reserves > 25 and random.random() < 0.85:
            msg = self.share_fuel(grace)
            actions.append(f"[ROCKY — FUEL TRANSFER] {msg}")

        # Priority 4: Share scientific knowledge when trust established
        if self.cooperation_level >= 20 and random.random() < 0.40:
            msg = self.share_knowledge(grace)
            actions.append(f"[ROCKY — DATA SHARE] {msg}")

        # Priority 5: Repair Grace's equipment when degraded
        if (grace.equipment_degradation > 45
                and self.fuel_reserves > 20
                and random.random() < 0.70):
            msg = self.perform_repair(grace)
            actions.append(f"[ROCKY — REPAIR] {msg}")

        return actions

    def get_status(self):
        return {
            "name":              self.name,
            "position":          (self.row, self.col),
            "health":            self.health,
            "energy":            self.energy,
            "fuel_reserves":     self.fuel_reserves,
            "engineering_skill": self.engineering_skill,
            "cooperation_level": self.cooperation_level,
            "translation_level": self.translation_level,
            "tunnel_built":      self.tunnel_built,
            "shared_knowledge":  self.shared_knowledge,
            "repairs_done":      self.repairs_done,
            "energy_shared":     self.energy_shared,
            "chord_log":         self.chord_log[-5:],
        }


# ─────────────────────────────────────────────
#  BEETLE PROBES
# ─────────────────────────────────────────────
class BeetleProbe(Agent):
    """
    Autonomous data-relay drone — one of four (John, Paul, George, Ringo).

    Navigates the grid using stellar positioning, moving toward the
    transmission zone representing Earth. Avoids Astrophage clouds to
    protect data integrity. Carries a knowledge payload and Taumoeba
    viability reading at time of deployment.
    """

    NAMES = ["John", "Paul", "George", "Ringo"]

    def __init__(self, name, row, col, knowledge_payload, taumoeba_viability):
        super().__init__(name, row, col)
        self.knowledge_payload  = knowledge_payload
        self.taumoeba_viability = taumoeba_viability
        self.deployed           = True
        self.progress           = 0      # 0-100% journey to Earth
        self.turns_in_flight    = 0
        self.data_intact        = True
        self.stellar_position   = (row, col)

    def navigate(self, environment):
        """
        Stellar positioning navigation — moves toward top-left corner
        representing Earth transmission direction.
        Detours around Astrophage and radiation hazards to protect payload.
        """
        from src.environment import ASTROPHAGE, RADIATION
        self.turns_in_flight += 1

        # Primary direction: toward top-left (Earth)
        dr = -1 if self.row > 0 else 0
        dc = -1 if self.col > 0 else 0

        # Check for hazard in primary path — detour if needed
        next_cell = environment.get_cell(
            (self.row + dr) % environment.height,
            (self.col + dc) % environment.width,
        )
        if next_cell in (ASTROPHAGE, RADIATION):
            dr, dc = random.choice([(-1, 0), (0, -1), (1, 0), (0, 1)])

        self.row = (self.row + dr) % environment.height
        self.col = (self.col + dc) % environment.width

        # Data integrity check — Astrophage exposure corrupts payload
        cell = environment.get_cell(self.row, self.col)
        if cell == ASTROPHAGE:
            self.data_intact = False

        # Progress toward Earth — advances each turn
        self.progress = min(100, self.progress + random.randint(5, 12))

    def transmit(self, environment):
        """Navigate one step and check if probe has reached Earth"""
        self.navigate(environment)
        if self.progress >= 100:
            status = "INTACT" if self.data_intact else "PARTIAL"
            return (True,
                    f"Probe '{self.name}' reached Earth! "
                    f"Payload: {self.knowledge_payload} knowledge pts, "
                    f"Viability: {self.taumoeba_viability:.1f}% — Data {status}.")
        return (False,
                f"Probe '{self.name}' in flight: {self.progress}% to Earth.")