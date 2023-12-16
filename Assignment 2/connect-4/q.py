from collections import defaultdict
import pickle

class Q:
    def __init__(self, learning_rate=0.5, discount_factor=0.5):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_values = defaultdict(lambda: defaultdict(lambda: 0.0))

    def update(self, s, act, n_s, reward):
        current_value = self.q_values[s][act]
        n_s_values = list(self.q_values[n_s].values())
        max_n_q_value = max(n_s_values) if n_s_values else 0
        updated_value = current_value + self.learning_rate * (reward + self.discount_factor * max_n_q_value - current_value)
        self.q_values[s][act] = updated_value

    def get_best_action(self, s):
        act = list(self.q_values[s].keys())
        if not act:
            return None
        return max(act, key=lambda x: self.q_values[s][x])

    def print_values(self, n=10):
        for i, (s, action_values) in enumerate(self.q_values.items()):
            if i == n:
                break
            print(f"{s}: {action_values}")

    def save_values(self, filename="q_values.pkl"):
        with open(filename, "wb") as f:
            pickle.dump({s: dict(action_values) for s, action_values in self.q_values.items()}, f)

    def load_values(self, filename="q_values.pkl"):
        try:
            with open(filename, "rb") as f:
                loaded_values = pickle.load(f)
                self.q_values = defaultdict(lambda: defaultdict(float), {s: defaultdict(float, action_values) for s, action_values in loaded_values.items()})
        except FileNotFoundError:
            print("File not found. Starting with an empty Q values table.")
