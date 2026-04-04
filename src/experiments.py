import random
import statistics

class ExperimentResult:
    """Records a single experiment outcome"""
    def __init__(self, turn, exp_type, outcome, viability, knowledge, notes=""):
        self.turn = turn
        self.exp_type = exp_type
        self.outcome = outcome
        self.viability = viability
        self.knowledge = knowledge
        self.notes = notes

    def __repr__(self):
        return f"Turn {self.turn} | {self.exp_type} | {self.outcome} | Viability: {self.viability:.2f} | Knowledge: {self.knowledge}"


class ExperimentManager:
    """Manages all scientific experiments - maintains scientific integrity"""

    EXPERIMENT_TYPES = [
        "Taumoeba Atmosphere Test",
        "Astrophage Energy Analysis",
        "Nitrogen Ratio Adjustment",
        "Taumoeba Breeding Attempt",
        "Cross-Species Data Analysis",
        "Xenonite Compatibility Test",
        "Stellar Energy Mapping",
        "Taumoeba Mutation Study",
    ]

    def __init__(self):
        self.results = []           # ALL results including failures
        self.successes = 0
        self.partial_successes = 0
        self.failures = 0
        self.current_strategy = "random"    # random, conservative, aggressive
        self.strategy_scores = {
            "random": 0,
            "conservative": 0,
            "aggressive": 0,
        }
        self.learning_rate = 0.1

    def run_experiment(self, grace, rocky=None, turn=0):
        """
        Run a scientific experiment with reinforcement-based learning.
        Strategy adapts based on previous outcomes.
        """
        if grace.taumoeba_samples == 0 and grace.astrophage_samples == 0:
            return None, "No samples available."

        exp_type = random.choice(self.EXPERIMENT_TYPES)
        grace.use_energy(10)
        grace.equipment_degradation += 2

        # Calculate success probability based on strategy and learning
        base_prob = 0.25 + (grace.knowledge_score / 400)

        if self.current_strategy == "conservative":
            success_mod = 0.05
            partial_mod = 0.25
        elif self.current_strategy == "aggressive":
            success_mod = 0.20
            partial_mod = 0.10
        else:  # random
            success_mod = 0.12
            partial_mod = 0.18

        # Rocky's assistance improves success chances
        if rocky and rocky.is_alive():
            base_prob += 0.12 + (rocky.cooperation_level / 500)
            exp_type = "Cross-Species " + exp_type

        roll = random.random()
        total_prob = base_prob + success_mod

        if roll > total_prob + partial_mod:
            outcome = "failure"
            knowledge_gain = random.randint(1, 3)
            viability_change = -0.02
            notes = "Sample degraded. Recording failure data for future reference."
            self.failures += 1
            self.strategy_scores[self.current_strategy] -= 1
        elif roll > total_prob:
            outcome = "partial_success"
            knowledge_gain = random.randint(3, 7)
            viability_change = random.uniform(0.03, 0.08)
            notes = "Partial viability detected. Adjusting parameters."
            self.partial_successes += 1
            self.strategy_scores[self.current_strategy] += 1
        else:
            outcome = "success"
            knowledge_gain = random.randint(8, 18)
            viability_change = random.uniform(0.10, 0.20)
            notes = "Strong viability! Taumoeba adapting to target atmosphere."
            self.successes += 1
            self.strategy_scores[self.current_strategy] += 3
            grace.mission_progress += 5

        # Apply results
        grace.knowledge_score += knowledge_gain
        grace.taumoeba_viability = min(1.0, max(0.0, grace.taumoeba_viability + viability_change))

        result = ExperimentResult(
            turn=turn,
            exp_type=exp_type,
            outcome=outcome,
            viability=grace.taumoeba_viability,
            knowledge=grace.knowledge_score,
            notes=notes,
        )
        self.results.append(result)

        # Reinforcement learning - adapt strategy based on outcomes
        self._adapt_strategy()

        return result, notes

    def _adapt_strategy(self):
        """
        Reinforcement-based strategy adaptation.
        Switches to the strategy with the highest score.
        """
        if len(self.results) % 5 == 0 and len(self.results) > 0:
            best = max(self.strategy_scores, key=self.strategy_scores.get)
            if best != self.current_strategy:
                self.current_strategy = best

    def get_statistics(self):
        """Returns statistical summary of all experiments"""
        if not self.results:
            return {}
        total = len(self.results)
        viabilities = [r.viability for r in self.results]
        knowledge_vals = [r.knowledge for r in self.results]
        return {
            "total_experiments": total,
            "successes": self.successes,
            "partial_successes": self.partial_successes,
            "failures": self.failures,
            "success_rate": round(self.successes / total * 100, 1),
            "partial_rate": round(self.partial_successes / total * 100, 1),
            "failure_rate": round(self.failures / total * 100, 1),
            "avg_viability": round(statistics.mean(viabilities), 3),
            "max_viability": round(max(viabilities), 3),
            "final_viability": round(viabilities[-1], 3),
            "avg_knowledge_gain": round(statistics.mean(knowledge_vals), 1),
            "current_strategy": self.current_strategy,
            "strategy_scores": self.strategy_scores,
        }

    def get_summary_report(self):
        """Human-readable experiment summary"""
        stats = self.get_statistics()
        if not stats:
            return "No experiments conducted yet."
        lines = [
            "=" * 50,
            "     SCIENTIFIC EXPERIMENT SUMMARY REPORT",
            "=" * 50,
            f"Total Experiments:     {stats['total_experiments']}",
            f"Successes:             {stats['successes']} ({stats['success_rate']}%)",
            f"Partial Successes:     {stats['partial_successes']} ({stats['partial_rate']}%)",
            f"Failures:              {stats['failures']} ({stats['failure_rate']}%)",
            f"Final Viability:       {stats['final_viability'] * 100:.1f}%",
            f"Avg Viability:         {stats['avg_viability'] * 100:.1f}%",
            f"Current Strategy:      {stats['current_strategy']}",
            "=" * 50,
        ]
        return "\n".join(lines)