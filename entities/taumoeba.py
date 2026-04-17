import random


class Taumoeba:
    def __init__(self):
        self.strain = "wild"
        self.survival_rate_earth = 0.0
        self.survival_rate_erid = 0.0
        self.generation = 0
        self.breeding_log = []
        self.astrophage_consumed = 0
        # Mutation rate changes procedurally
        self.mutation_rate = random.uniform(0.1, 0.3)

    def analyse(self, grace):
        """Grace analyses Taumoeba biology"""
        if grace.taumoeba_samples < 1:
            print("No Taumoeba samples!")
            return
        grace.energy -= 8
        grace.knowledge += 15
        print(f"Taumoeba analysis complete! "
              f"Knowledge +15")
        print(f"Earth survival: "
              f"{self.survival_rate_earth:.1%}")
        print(f"Erid survival: "
              f"{self.survival_rate_erid:.1%}")
        print(f"Mutation rate: {self.mutation_rate:.2f}")

    def breed_for_earth(self, grace, rocky=None):
        """Breed Taumoeba strain for Earth's atmosphere"""
        if grace.taumoeba_samples < 2:
            print("Need 2+ Taumoeba samples!")
            return False
        if grace.knowledge < 20:
            print("Not enough knowledge!")
            return False

        grace.energy -= 15
        grace.taumoeba_samples -= 1
        self.generation += 1

        # Procedurally varied mutation rate
        self.mutation_rate = random.uniform(0.1, 0.4)

        # Rocky assistance improves success
        success_chance = 0.3 + self.mutation_rate * 0.5
        if rocky and rocky.trust_level >= 30:
            success_chance = min(0.7, success_chance + 0.2)
            print("Rocky assists with breeding!")

        # Online learning adjusts success chance
        if grace.experiment_history["with_rocky"]["total"] > 0:
            success_rate = grace.get_success_rate("with_rocky")
            success_chance = min(
                0.8,
                success_chance + success_rate * 0.1
            )

        outcome = random.random()
        if outcome < success_chance * 0.5:
            gain = 0.2 + self.mutation_rate * 0.1
            self.survival_rate_earth = min(
                1.0, self.survival_rate_earth + gain
            )
            self.strain = "adapted"
            grace.knowledge += 20
            result = "SUCCESS"
            print(f"Breeding SUCCESS! "
                  f"Earth survival: "
                  f"{self.survival_rate_earth:.1%}")
        elif outcome < success_chance:
            gain = 0.05 + self.mutation_rate * 0.05
            self.survival_rate_earth = min(
                1.0, self.survival_rate_earth + gain
            )
            grace.knowledge += 8
            result = "PARTIAL"
            print(f"Partial progress. Earth survival: "
                  f"{self.survival_rate_earth:.1%}")
        else:
            grace.knowledge += 2
            result = "FAILURE"
            print("Breeding failed. Recording data...")

        self.breeding_log.append({
            "generation": self.generation,
            "result": result,
            "survival_rate_earth": self.survival_rate_earth,
            "survival_rate_erid": self.survival_rate_erid,
            "mutation_rate": self.mutation_rate
        })
        return self.survival_rate_earth >= 0.8

    def breed_for_erid(self, grace, rocky):
        """
        Breed Taumoeba strain for Rocky's planet Erid.
        Requires higher trust and knowledge.
        """
        if rocky.trust_level < 50:
            print("Need higher trust to breed for Erid!")
            return False
        if grace.taumoeba_samples < 2:
            print("Need 2+ Taumoeba samples!")
            return False
        if grace.knowledge < 40:
            print("Need more knowledge for Erid strain!")
            return False

        grace.energy -= 15
        grace.taumoeba_samples -= 1
        rocky.energy -= 10

        success_chance = 0.4
        if rocky.trust_level >= 70:
            success_chance = 0.6

        outcome = random.random()
        if outcome < success_chance * 0.5:
            self.survival_rate_erid = min(
                1.0, self.survival_rate_erid + 0.2
            )
            grace.knowledge += 25
            rocky.knowledge += 20
            result = "SUCCESS"
            print(f"Erid breeding SUCCESS! "
                  f"Erid survival: "
                  f"{self.survival_rate_erid:.1%}")
        elif outcome < success_chance:
            self.survival_rate_erid = min(
                1.0, self.survival_rate_erid + 0.05
            )
            grace.knowledge += 10
            result = "PARTIAL"
            print(f"Erid partial progress: "
                  f"{self.survival_rate_erid:.1%}")
        else:
            grace.knowledge += 3
            result = "FAILURE"
            print("Erid breeding failed. Recording...")

        return self.survival_rate_erid >= 0.8

    def consume_astrophage(self, environment, x, y):
        """Taumoeba naturally consumes Astrophage"""
        cell = environment.get_cell(x, y)
        if cell.astrophage_level > 0:
            consumed = min(2, cell.astrophage_level)
            cell.astrophage_level -= consumed
            self.astrophage_consumed += consumed
            environment.apply_taumoeba_resistance(x, y)

    def is_viable_earth(self):
        return self.survival_rate_earth >= 0.8

    def is_viable_erid(self):
        return self.survival_rate_erid >= 0.8

    def is_fully_viable(self):
        return self.is_viable_earth() and self.is_viable_erid()

    def status(self):
        print(f"\n--- Taumoeba Status ---")
        print(f"Strain: {self.strain}")
        print(f"Generation: {self.generation}")
        print(f"Mutation rate: {self.mutation_rate:.2f}")
        print(f"Earth survival: "
              f"{self.survival_rate_earth:.1%}")
        print(f"Erid survival: "
              f"{self.survival_rate_erid:.1%}")
        print(f"Viable for Earth: {self.is_viable_earth()}")
        print(f"Viable for Erid: {self.is_viable_erid()}")
        print(f"Astrophage consumed: "
              f"{self.astrophage_consumed}")
        print(f"Breeding log: {self.breeding_log}\n")