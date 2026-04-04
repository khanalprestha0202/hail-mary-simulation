import random

class Agent:
    """Base class for all agents in the simulation"""
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col
        self.health = 100
        self.energy = 100
        self.alive = True

    def is_alive(self):
        return self.alive and self.health > 0 and self.energy > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def use_energy(self, amount):
        self.energy -= amount
        if self.energy <= 0:
            self.energy = 0
            self.alive = False

    def rest(self):
        self.energy = min(100, self.energy + 15)
        self.health = min(100, self.health + 5)


class Grace(Agent):
    """Dr. Ryland Grace - the central human agent"""

    FLASHBACK_EVENTS = [
        (10,  "FLASHBACK: You remember Eva Stratt briefing you on the Astrophage threat. Earth has decades left."),
        (20,  "FLASHBACK: You recall being chosen because you were the only volunteer willing to die for humanity."),
        (35,  "FLASHBACK: You remember the Hail Mary launch. Billions watched. You were already in your coma."),
        (50,  "FLASHBACK: Eva's voice: 'Grace, if you find a solution - anything - transmit it. Don't come home empty handed.'"),
        (70,  "FLASHBACK: You remember your students. You promised them there would still be a world to grow up in."),
        (90,  "FLASHBACK: Full memory restored. You are Dr. Ryland Grace. You are humanity's last hope."),
    ]

    def __init__(self, row, col):
        super().__init__("Dr. Ryland Grace", row, col)
        self.knowledge_score = 0
        self.astrophage_samples = 0
        self.taumoeba_samples = 0
        self.taumoeba_viability = 0.0   # 0.0 to 1.0 - how close to a viable strain
        self.beetle_probes = 4
        self.probes_deployed = 0
        self.mission_progress = 0
        self.memory_restored = 0        # 0-100
        self.experiment_log = []
        self.flashbacks_triggered = set()
        self.rocky_trust = 0            # trust level with Rocky
        self.in_tunnel = False          # whether Grace is in the xenonite tunnel
        self.equipment_degradation = 0  # 0-100, higher = worse equipment

    def move(self, direction, environment):
        """Move Grace in a direction, costs energy"""
        dr, dc = {"up": (-1,0), "down": (1,0), "left": (0,-1), "right": (0,1)}.get(direction, (0,0))
        new_row = (self.row + dr) % environment.height
        new_col = (self.col + dc) % environment.width
        drain = environment.get_energy_drain(new_row, new_col)
        self.use_energy(2 + drain)
        self.health -= drain // 2
        self.row = new_row
        self.col = new_col
        return drain

    def collect_sample(self, environment):
        """Collect Astrophage or Taumoeba samples from current cell"""
        cell = environment.get_cell(self.row, self.col)
        from src.environment import ASTROPHAGE, ADRIAN, TAUMOEBA
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

    def conduct_experiment(self, rocky=None):
        """Run a scientific experiment - outcome depends on knowledge and samples"""
        if self.taumoeba_samples == 0 and self.astrophage_samples == 0:
            return "experiment_fail", "No samples to experiment with."

        self.use_energy(10)
        self.equipment_degradation += 2

        # Base success chance improves with knowledge and Rocky's help
        base_chance = 0.3 + (self.knowledge_score / 300)
        if rocky and rocky.is_alive():
            base_chance += 0.15 + (rocky.engineering_skill / 200)

        roll = random.random()
        if roll < base_chance * 0.4:
            outcome = "failure"
            result = "Experiment failed. Taumoeba sample degraded in Earth atmosphere simulation."
            self.knowledge_score += 1
        elif roll < base_chance * 0.8:
            outcome = "partial"
            result = "Partial success! Taumoeba survived briefly. Adjusting nitrogen ratios."
            self.knowledge_score += 4
            self.taumoeba_viability += 0.05
        else:
            outcome = "success"
            result = "SUCCESS! Taumoeba strain showing strong viability in Earth atmosphere!"
            self.knowledge_score += 10
            self.taumoeba_viability += 0.15
            self.mission_progress += 5

        self.taumoeba_viability = min(1.0, self.taumoeba_viability)
        self.experiment_log.append({
            "turn": len(self.experiment_log) + 1,
            "outcome": outcome,
            "viability": round(self.taumoeba_viability, 2),
            "knowledge": self.knowledge_score,
        })
        return outcome, result

    def deploy_beetle_probe(self, knowledge_threshold=30):
        """Deploy a beetle probe to transmit findings to Earth"""
        if self.beetle_probes == 0:
            return False, "No beetle probes remaining."
        if self.knowledge_score < knowledge_threshold:
            return False, f"Insufficient knowledge to deploy. Need {knowledge_threshold} points."
        self.beetle_probes -= 1
        self.probes_deployed += 1
        self.mission_progress += 15
        self.use_energy(8)
        names = ["John", "Paul", "George", "Ringo"]
        name = names[self.probes_deployed - 1] if self.probes_deployed <= 4 else f"Probe-{self.probes_deployed}"
        return True, f"Beetle probe '{name}' deployed! Transmitting {self.knowledge_score} knowledge points to Earth."

    def check_flashbacks(self):
        """Trigger flashback events based on knowledge score"""
        messages = []
        for threshold, message in self.FLASHBACK_EVENTS:
            if self.knowledge_score >= threshold and threshold not in self.flashbacks_triggered:
                self.flashbacks_triggered.add(threshold)
                self.memory_restored = min(100, self.memory_restored + 15)
                messages.append(message)
        return messages

    def repair_equipment(self, rocky=None):
        """Repair degraded equipment"""
        self.use_energy(12)
        if rocky and rocky.is_alive():
            repair = random.randint(15, 30)
            self.equipment_degradation = max(0, self.equipment_degradation - repair)
            return f"Rocky helped repair equipment. Degradation reduced by {repair}."
        repair = random.randint(5, 15)
        self.equipment_degradation = max(0, self.equipment_degradation - repair)
        return f"Self-repair attempt. Degradation reduced by {repair}."

    def get_status(self):
        return {
            "name": self.name,
            "position": (self.row, self.col),
            "health": self.health,
            "energy": self.energy,
            "knowledge_score": self.knowledge_score,
            "taumoeba_viability": round(self.taumoeba_viability * 100, 1),
            "astrophage_samples": self.astrophage_samples,
            "taumoeba_samples": self.taumoeba_samples,
            "beetle_probes_left": self.beetle_probes,
            "probes_deployed": self.probes_deployed,
            "mission_progress": self.mission_progress,
            "memory_restored": self.memory_restored,
            "equipment_degradation": self.equipment_degradation,
            "rocky_trust": self.rocky_trust,
        }


class Rocky(Agent):
    """Rocky - the Eridian alien agent"""

    CHORD_MESSAGES = [
        "♪♩♫ (Rocky: Astrophage bad. My star also sick.)",
        "♫♪♩ (Rocky: I help you. You help me. Deal?)",
        "♩♫♪ (Rocky: Xenonite tunnel strong. You visit safe.)",
        "♪♫♩ (Rocky: My ship has more fuel. I share.)",
        "♩♩♫ (Rocky: Taumoeba - I see similar organism in Erid system!)",
        "♫♫♪ (Rocky: Experiment! I bring my tools. Together faster.)",
        "♪♪♩ (Rocky: Earth and Erid both saved. Good outcome.)",
        "♩♫♫ (Rocky: You are good human. Rocky trust you.)",
    ]

    def __init__(self, row, col):
        super().__init__("Rocky (Eridian)", row, col)
        self.engineering_skill = 80
        self.fuel_reserves = 100
        self.shared_knowledge = 0
        self.chord_index = 0
        self.cooperation_level = 0      # increases as Grace and Rocky work together
        self.translation_level = 0      # how well they understand each other (0-100)
        self.repairs_done = 0
        self.energy_shared = 0

    def communicate(self, grace):
        """Rocky sends a chord-based message, improving translation"""
        if self.chord_index < len(self.CHORD_MESSAGES):
            message = self.CHORD_MESSAGES[self.chord_index]
            self.chord_index += 1
        else:
            message = "♪♩♫♪ (Rocky: We are friends. We will succeed.)"

        self.translation_level = min(100, self.translation_level + 8)
        grace.rocky_trust = min(100, grace.rocky_trust + 6)
        self.cooperation_level = min(100, self.cooperation_level + 5)
        grace.knowledge_score += 3
        return message

    def share_knowledge(self, grace):
        """Rocky shares scientific data from the Eridian database"""
        if self.fuel_reserves < 10:
            return "Rocky has insufficient energy to share data."
        knowledge_gained = random.randint(8, 20)
        grace.knowledge_score += knowledge_gained
        self.shared_knowledge += knowledge_gained
        self.cooperation_level = min(100, self.cooperation_level + 8)
        grace.rocky_trust = min(100, grace.rocky_trust + 5)
        self.use_energy(5)
        return f"Rocky shares Eridian star maps and Astrophage data. +{knowledge_gained} knowledge!"

    def perform_repair(self, grace):
        """Rocky repairs Grace's ship equipment"""
        if self.fuel_reserves < 15:
            return "Rocky's fuel too low to power repair tools."
        self.fuel_reserves -= 10
        self.repairs_done += 1
        repair_amount = random.randint(20, 40)
        grace.equipment_degradation = max(0, grace.equipment_degradation - repair_amount)
        self.cooperation_level = min(100, self.cooperation_level + 10)
        return f"Rocky performs engineering repair. Equipment improved by {repair_amount} points!"

    def share_fuel(self, grace):
        """Rocky shares Astrophage fuel with Grace"""
        if self.fuel_reserves < 20:
            return "Rocky: Not enough fuel to share safely."
        amount = min(30, self.fuel_reserves - 10)
        self.fuel_reserves -= amount
        grace.energy = min(100, grace.energy + amount)
        self.energy_shared += amount
        self.cooperation_level = min(100, self.cooperation_level + 12)
        grace.rocky_trust = min(100, grace.rocky_trust + 8)
        return f"Rocky shares {amount} units of Astrophage fuel. Grace energy restored!"

    def autonomous_action(self, grace, environment):
        """Rocky acts independently each turn based on situation"""
        actions = []
        # Rocky communicates early to build translation
        if self.translation_level < 40 and random.random() < 0.5:
            msg = self.communicate(grace)
            actions.append(f"[ROCKY COMMUNICATES] {msg}")
        # Rocky shares fuel if Grace is low
        if grace.energy < 30 and self.fuel_reserves > 25 and random.random() < 0.7:
            msg = self.share_fuel(grace)
            actions.append(f"[ROCKY SHARES FUEL] {msg}")
        # Rocky shares knowledge when cooperation is high
        if self.cooperation_level > 30 and random.random() < 0.4:
            msg = self.share_knowledge(grace)
            actions.append(f"[ROCKY SHARES DATA] {msg}")
        # Rocky repairs when equipment is bad
        if grace.equipment_degradation > 50 and self.fuel_reserves > 20 and random.random() < 0.6:
            msg = self.perform_repair(grace)
            actions.append(f"[ROCKY REPAIRS] {msg}")
        return actions

    def get_status(self):
        return {
            "name": self.name,
            "position": (self.row, self.col),
            "health": self.health,
            "energy": self.energy,
            "fuel_reserves": self.fuel_reserves,
            "engineering_skill": self.engineering_skill,
            "cooperation_level": self.cooperation_level,
            "translation_level": self.translation_level,
            "shared_knowledge": self.shared_knowledge,
            "repairs_done": self.repairs_done,
            "energy_shared": self.energy_shared,
        }


class BeetleProbe(Agent):
    """Autonomous data-relay drone"""
    NAMES = ["John", "Paul", "George", "Ringo"]

    def __init__(self, name, row, col, knowledge_payload):
        super().__init__(name, row, col)
        self.knowledge_payload = knowledge_payload
        self.deployed = True
        self.destination = "Earth"
        self.progress = 0       # 0-100% journey to Earth

    def transmit(self):
        self.progress = min(100, self.progress + random.randint(5, 15))
        if self.progress >= 100:
            return f"Probe '{self.name}' has reached Earth! {self.knowledge_payload} knowledge units transmitted!"
        return f"Probe '{self.name}' en route to Earth: {self.progress}% complete."