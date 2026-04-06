import random
import statistics


class ExperimentResult:
    """Records a single experiment outcome — all results kept for scientific integrity"""
    def __init__(self, turn, exp_type, outcome, viability, knowledge, strategy, notes=""):
        self.turn      = turn
        self.exp_type  = exp_type
        self.outcome   = outcome
        self.viability = viability
        self.knowledge = knowledge
        self.strategy  = strategy
        self.notes     = notes

    def __repr__(self):
        return (f"Turn {self.turn} | {self.exp_type} | {self.outcome} | "
                f"Viability: {self.viability:.2f} | Knowledge: {self.knowledge} | "
                f"Strategy: {self.strategy}")


class QLearningStrategy:
    """
    Q-Learning agent that learns the best experimental strategy.
    States  = (knowledge_band, viability_band, rocky_cooperation_band)
    Actions = 0:conservative  1:balanced  2:aggressive
    """

    ACTIONS      = ["conservative", "balanced", "aggressive"]
    LEARNING_RATE  = 0.15
    DISCOUNT       = 0.90
    EPSILON_START  = 1.0   # start fully exploratory
    EPSILON_MIN    = 0.10
    EPSILON_DECAY  = 0.97

    def __init__(self):
        self.q_table = {}          # state -> [q_val_0, q_val_1, q_val_2]
        self.epsilon = self.EPSILON_START
        self.last_state  = None
        self.last_action = None
        self.total_reward = 0.0
        self.update_count = 0

    def _get_state(self, grace, rocky):
        """Discretise continuous values into state bands"""
        k_band    = min(4, grace.knowledge_score // 25)       # 0-4
        v_band    = min(4, int(grace.taumoeba_viability * 5)) # 0-4
        coop_band = min(2, rocky.cooperation_level // 34)     # 0-2
        return (k_band, v_band, coop_band)

    def _ensure_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0]

    def choose_action(self, grace, rocky):
        """Epsilon-greedy action selection"""
        state = self._get_state(grace, rocky)
        self._ensure_state(state)
        if random.random() < self.epsilon:
            action = random.randint(0, 2)   # explore
        else:
            action = self.q_table[state].index(max(self.q_table[state]))  # exploit
        self.last_state  = state
        self.last_action = action
        return action, self.ACTIONS[action]

    def update(self, grace, rocky, outcome, viability_gained):
        """Update Q-table based on experiment outcome"""
        if self.last_state is None:
            return

        # Reward function
        if outcome == "success":
            reward = 10.0 + viability_gained * 50
        elif outcome == "partial_success":
            reward = 3.0  + viability_gained * 20
        else:
            reward = -1.0

        new_state = self._get_state(grace, rocky)
        self._ensure_state(new_state)

        # Q-learning update rule
        old_q    = self.q_table[self.last_state][self.last_action]
        max_next = max(self.q_table[new_state])
        new_q    = old_q + self.LEARNING_RATE * (
            reward + self.DISCOUNT * max_next - old_q
        )
        self.q_table[self.last_state][self.last_action] = new_q

        # Decay epsilon
        self.epsilon     = max(self.EPSILON_MIN, self.epsilon * self.EPSILON_DECAY)
        self.total_reward += reward
        self.update_count += 1

    def get_policy_summary(self):
        """Return a human-readable summary of what the Q-table has learned"""
        if not self.q_table:
            return "No learning data yet."
        lines = [f"Q-table states explored: {len(self.q_table)}",
                 f"Total reward accumulated: {self.total_reward:.1f}",
                 f"Current epsilon: {self.epsilon:.3f}",
                 f"Updates: {self.update_count}"]
        return " | ".join(lines)


class ExperimentManager:
    """
    Manages all scientific experiments.
    Uses Q-learning to adapt strategy based on outcomes.
    Records ALL results — including failures — for scientific integrity.
    """

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
        self.results         = []
        self.successes       = 0
        self.partial_successes = 0
        self.failures        = 0
        self.q_learner       = QLearningStrategy()

    def run_experiment(self, grace, rocky=None, turn=0):
        """
        Run one experiment.
        Q-learner chooses the strategy; outcome updates the Q-table.
        """
        if grace.taumoeba_samples == 0 and grace.astrophage_samples == 0:
            return None, "No samples available."

        # Q-learner picks strategy
        action_idx, strategy = self.q_learner.choose_action(grace, rocky or _DummyRocky())

        exp_type = random.choice(self.EXPERIMENT_TYPES)
        grace.use_energy(8)
        grace.equipment_degradation = min(100, grace.equipment_degradation + 1)

        # Base success probability
        base = 0.30 + (grace.knowledge_score / 250)
        if rocky and rocky.is_alive():
            base += 0.12 + (rocky.cooperation_level / 400)
            exp_type = "Cross-Species " + exp_type

        # Strategy modifiers
        if strategy == "conservative":
            s_mod, p_mod = 0.04, 0.22
        elif strategy == "aggressive":
            s_mod, p_mod = 0.18, 0.08
        else:  # balanced
            s_mod, p_mod = 0.10, 0.15

        roll = random.random()

        if roll < base + s_mod:
            outcome        = "success"
            knowledge_gain = random.randint(8, 18)
            vgain          = random.uniform(0.10, 0.22)
            notes          = "Taumoeba strain showing strong viability!"
            self.successes += 1
            grace.mission_progress += 5
        elif roll < base + s_mod + p_mod:
            outcome        = "partial_success"
            knowledge_gain = random.randint(3, 8)
            vgain          = random.uniform(0.03, 0.09)
            notes          = "Partial viability. Adjusting parameters."
            self.partial_successes += 1
        else:
            outcome        = "failure"
            knowledge_gain = random.randint(1, 3)
            vgain          = -0.01
            notes          = "Sample degraded. Failure recorded for analysis."
            self.failures  += 1

        grace.knowledge_score     += knowledge_gain
        grace.taumoeba_viability   = min(1.0, max(0.0,
            grace.taumoeba_viability + vgain))

        # Update Q-table
        self.q_learner.update(grace, rocky or _DummyRocky(), outcome, max(0, vgain))

        result = ExperimentResult(
            turn=turn, exp_type=exp_type, outcome=outcome,
            viability=grace.taumoeba_viability,
            knowledge=grace.knowledge_score,
            strategy=strategy, notes=notes,
        )
        self.results.append(result)
        return result, notes

    def get_statistics(self):
        if not self.results:
            return {}
        total      = len(self.results)
        viabilities = [r.viability for r in self.results]
        knowledge   = [r.knowledge for r in self.results]
        return {
            "total_experiments":  total,
            "successes":          self.successes,
            "partial_successes":  self.partial_successes,
            "failures":           self.failures,
            "success_rate":       round(self.successes / total * 100, 1),
            "partial_rate":       round(self.partial_successes / total * 100, 1),
            "failure_rate":       round(self.failures / total * 100, 1),
            "avg_viability":      round(statistics.mean(viabilities), 3),
            "max_viability":      round(max(viabilities), 3),
            "final_viability":    round(viabilities[-1], 3),
            "avg_knowledge":      round(statistics.mean(knowledge), 1),
            "current_strategy":   self.q_learner.ACTIONS[
                                      self.q_learner.last_action
                                      if self.q_learner.last_action is not None else 1],
            "q_policy":           self.q_learner.get_policy_summary(),
            "epsilon":            round(self.q_learner.epsilon, 3),
            "q_table_size":       len(self.q_learner.q_table),
        }

    def get_summary_report(self):
        stats = self.get_statistics()
        if not stats:
            return "No experiments conducted yet."
        lines = [
            "=" * 55,
            "     SCIENTIFIC EXPERIMENT SUMMARY REPORT",
            "=" * 55,
            f"Total Experiments:     {stats['total_experiments']}",
            f"Successes:             {stats['successes']} ({stats['success_rate']}%)",
            f"Partial Successes:     {stats['partial_successes']} ({stats['partial_rate']}%)",
            f"Failures:              {stats['failures']} ({stats['failure_rate']}%)",
            f"Final Viability:       {stats['final_viability']*100:.1f}%",
            f"Q-Learning Policy:     {stats['q_policy']}",
            f"Q-Table States:        {stats['q_table_size']}",
            f"Epsilon (exploration): {stats['epsilon']}",
            "=" * 55,
        ]
        return "\n".join(lines)


class _DummyRocky:
    """Placeholder when Rocky is not yet available"""
    cooperation_level = 0
    is_alive = lambda self: False