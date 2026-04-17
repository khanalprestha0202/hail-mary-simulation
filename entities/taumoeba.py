import random


class Taumoeba:
    def __init__(self):
        self.strain = "wild"
        self.survival_rate_earth = 0.0
        self.survival_rate_erid = 0.0
        self.generation = 0
        self.breeding_log = []

    def analyse(self, grace):
        """Grace analyses Taumoeba biology"""
        if grace.taumoeba_samples < 1:
            print("No Taumoeba samples to analyse!")
            return
        grace.energy -= 8
        grace.knowledge += 15
        print(f"Taumoeba analysis complete! Knowledge +15")
        print(f"Current Earth survival rate: {self.survival_rate_earth:.1%}")

    def breed(self, grace, rocky=None):
        """Attempt to breed a Taumoeba strain for Earth atmosphere"""
        if grace.taumoeba_samples < 2:
            print("Need at least 2 Taumoeba samples to breed!")
            return False
        if grace.knowledge < 20:
            print("Not enough knowledge to attempt breeding!")
            return False

        grace.energy -= 15
        grace.taumoeba_samples -= 1
        self.generation += 1

        # Rocky assistance improves success chance
        success_chance = 0.3
        if rocky and rocky.trust_level >= 30:
            success_chance = 0.5
            print("Rocky assists with breeding — success chance improved!")

        outcome = random.random()
        if outcome < success_chance:
            self.survival_rate_earth = min(1.0, self.survival_rate_earth + 0.2)
            self.strain = "adapted"
            grace.knowledge += 20
            result = "SUCCESS"
            print(f"Breeding SUCCESS! Earth survival: {self.survival_rate_earth:.1%}")
        elif outcome < success_chance + 0.4:
            self.survival_rate_earth = min(1.0, self.survival_rate_earth + 0.05)
            result = "PARTIAL"
            grace.knowledge += 8
            print(f"Partial progress. Earth survival: {self.survival_rate_earth:.1%}")
        else:
            result = "FAILURE"
            grace.knowledge += 2
            print("Breeding failed. Recording data for next attempt...")

        self.breeding_log.append({
            "generation": self.generation,
            "result": result,
            "survival_rate": self.survival_rate_earth
        })
        return self.survival_rate_earth >= 0.8

    def is_viable(self):
        """Check if Taumoeba is ready to save Earth"""
        return self.survival_rate_earth >= 0.8

    def status(self):
        print(f"\n--- Taumoeba Status ---")
        print(f"Strain: {self.strain}")
        print(f"Generation: {self.generation}")
        print(f"Earth survival rate: {self.survival_rate_earth:.1%}")
        print(f"Viable for Earth: {self.is_viable()}")
        print(f"Breeding log: {self.breeding_log}\n")