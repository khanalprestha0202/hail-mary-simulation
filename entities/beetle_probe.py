class BeetleProbe:
    NAMES = ["John", "Paul", "George", "Ringo"]

    def __init__(self, probe_id, x, y, knowledge_payload):
        self.name = self.NAMES[probe_id]
        self.x = x
        self.y = y
        self.knowledge_payload = knowledge_payload
        self.deployed = True
        self.reached_earth = False

    def navigate(self):
        """Probe travels toward Earth"""
        self.x -= 1
        if self.x <= 0:
            self.reached_earth = True
            print(f"Probe {self.name} has reached Earth!")
            print(f"Data delivered: {self.knowledge_payload} knowledge units")

    def status(self):
        print(f"Probe {self.name}: Position ({self.x},{self.y}) | "
              f"Payload: {self.knowledge_payload} | "
              f"Reached Earth: {self.reached_earth}")