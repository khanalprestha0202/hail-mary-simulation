class BeetleProbe:
    NAMES = ["John", "Paul", "George", "Ringo"]

    def __init__(self, probe_id, x, y, knowledge_payload):
        self.name = self.NAMES[probe_id % 4]
        self.x = x
        self.y = y
        self.knowledge_payload = knowledge_payload
        self.deployed = True
        self.reached_earth = False
        self.stellar_heading = -1  # Moving toward Earth
        self.turns_in_flight = 0
        self.data_integrity = 100

    def configure(self, heading=-1, payload_boost=0):
        """Configure probe trajectory before deployment"""
        self.stellar_heading = heading
        self.knowledge_payload += payload_boost
        print(f"Probe {self.name} configured: "
              f"heading {heading}, "
              f"payload {self.knowledge_payload}")

    def navigate(self):
        """Probe navigates using stellar positioning"""
        if self.reached_earth:
            return

        self.turns_in_flight += 1
        self.x += self.stellar_heading

        # Small data degradation over long journeys
        if self.turns_in_flight > 10:
            self.data_integrity = max(
                80, self.data_integrity - 1
            )

        if self.x <= 0:
            self.reached_earth = True
            effective_payload = int(
                self.knowledge_payload
                * self.data_integrity / 100
            )
            print(f"Probe {self.name} reached Earth!")
            print(f"Data delivered: "
                  f"{effective_payload} knowledge units")
            print(f"Data integrity: {self.data_integrity}%")

    def status(self):
        print(f"Probe {self.name}: "
              f"Pos ({self.x},{self.y}) | "
              f"Payload: {self.knowledge_payload} | "
              f"Integrity: {self.data_integrity}% | "
              f"Reached Earth: {self.reached_earth}")