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

    State space: (knowledge_band, viability_band, cooperation_band)
    - knowledge_band:    0-4  (grace.knowledge_score // 25, capped at 4)
    - viability_band:    0-4  (taumoeba_viability * 5, capped at 4)
    - cooperation_band:  0-2  (rocky.cooperation_level // 34)

    Actions:
    - 0: conservative — lower risk, lower reward
    - 1: balanced     — moderate risk, moderate reward
    - 2: aggressive   — higher risk, higher reward

    Update rule: Q(s,a) = Q(s,a) + alpha * (r + gamma * max(Q(s')) - Q(s,a))
    Exploration: epsilon-greedy with decay from 1.0 to 0.10
    """

    ACTIONS        = ["conservative", "balanced", "aggressive"]
    LEARNING_RATE  = 0.15   # alpha
    DISCOUNT       = 0.90   # gamma
    EPSILON_START  = 1.0    # fully exploratory at start
    EPSILON_MIN    = 0.10   # always retain 10% exploration
    EPSILON_DECAY  = 0.95   # faster decay for more exploitation over time

    def __init__(self):
        self.q_table      = {}   # state -> [q_val_conservative, q_val_balanced, q_val_aggressive]
        self.epsilon      = self.EPSILON_START
        self.last_state   = None
        self.last_action  = None
        self.total_reward = 0.0
        self.update_count = 0

    def _get_state(self, grace, rocky):
        """Discretise continuous values into state bands for Q-table lookup"""
        k_band    = min(4, grace.knowledge_score // 25)        # 0-4
        v_band    = min(4, int(grace.taumoeba_viability * 5))  # 0-4
        coop_band = min(2, rocky.cooperation_level // 34)      # 0-2
        return (k_band, v_band, coop_band)

    def _ensure_state(self, state):
        """Initialise Q-values to zero if state not yet visited"""
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0]

    def choose_action(self, grace, rocky):
        """
        Epsilon-greedy action selection.
        Explores randomly with probability epsilon, otherwise exploits best known action.
        """
        state = self._get_state(grace, rocky)
        self._ensure_state(state)
        if random.random() < self.epsilon:
            action = random.randint(0, 2)  # explore
        else:
            action = self.q_table[state].index(max(self.q_table[state]))  # exploit
        self.last_state  = state
        self.last_action = action
        return action, self.ACTIONS[action]

    def update(self, grace, rocky, outcome, viability_gained):
        """
        Temporal difference update after observing experiment outcome.
        Reward is shaped to strongly encourage viability gains.
        """
        if self.last_state is None:
            return

        # Reward shaping — viability gains weighted heavily
        if outcome == "success":
            reward = 12.0 + viability_gained * 60
        elif outcome == "partial_success":
            reward = 4.0 + viability_gained * 25
        else:
            reward = -1.0  # failure still records useful data

        new_state = self._get_state(grace, rocky)
        self._ensure_state(new_state)

        # Temporal difference Q-update
        old_q    = self.q_table[self.last_state][self.last_action]
        max_next = max(self.q_table[new_state])
        new_q    = old_q + self.LEARNING_RATE * (
            reward + self.DISCOUNT * max_next - old_q
        )
        self.q_table[self.last_state][self.last_action] = new_q

        # Decay epsilon — shift from exploration toward exploitation
        self.epsilon      = max(self.EPSILON_MIN, self.epsilon * self.EPSILON_DECAY)
        self.total_reward += reward
        self.update_count += 1

    def get_best_action_per_state(self):
        """Return the greedy best action for each explored state — shows learned policy"""
        policy = {}
        for state, q_vals in self.q_table.items():
            best = q_vals.index(max(q_vals))
            policy[state] = self.ACTIONS[best]
        return policy

    def get_policy_summary(self):
        """Human-readable summary of Q-table learning progress"""
        if not self.q_table:
            return "No learning data yet."
        policy = self.get_best_action_per_state()
        action_counts = {"conservative": 0, "balanced": 0, "aggressive": 0}
        for a in policy.values():
            action_counts[a] += 1
        dominant = max(action_counts, key=action_counts.get)
        return (f"Q-table states explored: {len(self.q_table)} | "
                f"Total reward: {self.total_reward:.1f} | "
                f"Epsilon: {self.epsilon:.3f} | "
                f"Updates: {self.update_count} | "
                f"Dominant strategy: {dominant}")


class ExperimentManager:
    """
    Manages all scientific experiments throughout the simulation.

    Uses Q-learning to adaptively choose experimental strategy based on
    current knowledge, Taumoeba viability, and Rocky's cooperation level.

    Scientific integrity: ALL outcomes including failures are recorded
    and contribute to the knowledge base — failed experiments inform
    future strategy just as successes do.
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
        "Atmospheric Pressure Calibration",
        "Eridian Biochemistry Comparison",
    ]

    def __init__(self):
        self.results           = []
        self.successes         = 0
        self.partial_successes = 0
        self.failures          = 0
        self.q_learner         = QLearningStrategy()

    def run_experiment(self, grace, rocky=None, turn=0):
        """
        Run one experiment using Q-learning to select strategy.
        Outcome depends on knowledge score, Rocky cooperation, and strategy chosen.
        All results recorded regardless of outcome (scientific integrity).
        """
        if grace.taumoeba_samples == 0 and grace.astrophage_samples == 0:
            return None, "No samples available for experimentation."

        dummy = _DummyRocky()
        active_rocky = rocky if (rocky and rocky.is_alive()) else dummy

        # Q-learner selects strategy based on current state
        action_idx, strategy = self.q_learner.choose_action(grace, active_rocky)

        exp_type = random.choice(self.EXPERIMENT_TYPES)
        grace.use_energy(8)
        grace.equipment_degradation = min(100, grace.equipment_degradation + 1)

        # Base success probability — improves with knowledge and cooperation
        base = 0.28 + (grace.knowledge_score / 220)
        if rocky and rocky.is_alive():
            base += 0.10 + (rocky.cooperation_level / 350)
            exp_type = "Cross-Species " + exp_type

        # Strategy modifiers — conservative is safer, aggressive is riskier
        if strategy == "conservative":
            s_mod, p_mod = 0.05, 0.25
        elif strategy == "aggressive":
            s_mod, p_mod = 0.20, 0.10
        else:  # balanced
            s_mod, p_mod = 0.12, 0.18

        roll = random.random()

        if roll < base + s_mod:
            outcome        = "success"
            knowledge_gain = random.randint(10, 22)
            vgain          = random.uniform(0.12, 0.25)
            notes          = "Taumoeba strain showing strong viability!"
            self.successes += 1
            grace.mission_progress += 5

        elif roll < base + s_mod + p_mod:
            outcome        = "partial_success"
            knowledge_gain = random.randint(4, 10)
            vgain          = random.uniform(0.05, 0.12)
            notes          = "Partial viability detected. Adjusting experimental parameters."
            self.partial_successes += 1

        else:
            outcome        = "failure"
            knowledge_gain = random.randint(1, 4)
            vgain          = -0.01
            notes          = "Sample degraded. Failure recorded for future analysis."
            self.failures  += 1

        grace.knowledge_score    += knowledge_gain
        grace.taumoeba_viability  = min(1.0, max(0.0,
            grace.taumoeba_viability + vgain))

        # Update Q-table with outcome
        self.q_learner.update(
            grace, active_rocky, outcome, max(0.0, vgain)
        )

        result = ExperimentResult(
            turn=turn,
            exp_type=exp_type,
            outcome=outcome,
            viability=grace.taumoeba_viability,
            knowledge=grace.knowledge_score,
            strategy=strategy,
            notes=notes,
        )
        self.results.append(result)
        return result, notes

    def get_statistics(self):
        """Return statistical summary of all experiments conducted"""
        if not self.results:
            return {}
        total       = len(self.results)
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
        """Formatted experiment summary report for console output"""
        stats = self.get_statistics()
        if not stats:
            return "No experiments conducted yet."
        lines = [
            "=" * 58,
            "        SCIENTIFIC EXPERIMENT SUMMARY REPORT",
            "=" * 58,
            f"  Total Experiments:     {stats['total_experiments']}",
            f"  Successes:             {stats['successes']} ({stats['success_rate']}%)",
            f"  Partial Successes:     {stats['partial_successes']} ({stats['partial_rate']}%)",
            f"  Failures:              {stats['failures']} ({stats['failure_rate']}%)",
            f"  Final Viability:       {stats['final_viability']*100:.1f}%",
            f"  Q-Learning Policy:     {stats['q_policy']}",
            f"  Q-Table States:        {stats['q_table_size']}",
            f"  Epsilon (exploration): {stats['epsilon']}",
            "=" * 58,
        ]
        return "\n".join(lines)


class _DummyRocky:
    """Placeholder Rocky used when real Rocky is not yet available"""
    cooperation_level = 0
    is_alive = lambda self: False