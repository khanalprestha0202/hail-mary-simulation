import random


class Rocky:
    def __init__(self, x=10, y=15):
        self.x = x
        self.y = y
        self.health = 100
        self.energy = 100
        self.knowledge = 50  # Rocky arrives with existing knowledge
        self.name = "Rocky"
        self.species = "Eridian"
        self.astrophage_fuel = 80
        self.trust_level = 0  # builds up over time with Grace
        self.shared_data = []
        self.translation_level = 0  # 0=none, 100=fluent

    def communicate(self, grace):
        """Rocky communicates via sonar chord patterns"""
        self.translation_level = min(100, self.translation_level + 10)
        grace.knowledge += 5
        self.trust_level = min(100, self.trust_level + 10)
        chords = ["♪♫♪", "♫♪♫", "♪♪♫", "♫♫♪"]
        chord = random.choice(chords)
        print(f"Rocky: {chord} (Translation level: {self.translation_level}%)")
        if self.translation_level >= 30:
            print("Rocky communicates: 'My star also threatened. We help each other!'")
        if self.translation_level >= 60:
            print("Rocky shares star map data! Grace knowledge +5")
        self.shared_data.append(f"Communication at translation {self.translation_level}%")

    def share_knowledge(self, grace):
        """Rocky shares scientific data with Grace"""
        if self.trust_level < 20:
            print("Rocky not yet trusting enough to share knowledge.")
            return
        knowledge_gain = random.randint(10, 25)
        grace.knowledge += knowledge_gain
        self.energy -= 5
        print(f"Rocky shares Astrophage data! Grace knowledge +{knowledge_gain}")
        self.shared_data.append(f"Shared knowledge: +{knowledge_gain}")

    def perform_repair(self, grace):
        """Rocky performs engineering repairs Grace cannot do alone"""
        if self.trust_level < 40:
            print("Rocky needs more trust before performing repairs.")
            return
        grace.energy = min(100, grace.energy + 30)
        self.energy -= 20
        print("Rocky repairs Hail Mary systems! Grace energy +30")

    def transfer_fuel(self, grace_ship_energy):
        """Rocky shares Astrophage fuel reserves"""
        if self.astrophage_fuel >= 20 and self.trust_level >= 50:
            self.astrophage_fuel -= 20
            grace_ship_energy = min(100, grace_ship_energy + 20)
            print(f"Rocky transfers fuel! Rocky fuel: {self.astrophage_fuel}")
            return grace_ship_energy
        else:
            print("Rocky cannot transfer fuel yet.")
            return grace_ship_energy

    def assist_experiment(self, grace):
        """Rocky assists Grace with Taumoeba experiments"""
        if self.trust_level < 30:
            print("Rocky not ready to assist experiments yet.")
            return
        if grace.taumoeba_samples < 1:
            print("No Taumoeba samples to experiment with!")
            return
        self.energy -= 10
        bonus = random.randint(5, 15)
        grace.knowledge += bonus
        print(f"Rocky assists experiment! Extra knowledge +{bonus}")

    def rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"Rocky rested. Energy: {self.energy}")

    def status(self):
        print(f"\n--- {self.name} ({self.species}) ---")
        print(f"Position: ({self.x}, {self.y})")
        print(f"Health: {self.health} | Energy: {self.energy}")
        print(f"Knowledge: {self.knowledge}")
        print(f"Trust with Grace: {self.trust_level}%")
        print(f"Translation level: {self.translation_level}%")
        print(f"Astrophage fuel: {self.astrophage_fuel}\n")