class PositionManager:

    def __init__(self):
        self.position = None
        self.entry_price = None

    def open_long(self, price):
        self.position = "LONG"
        self.entry_price = price

    def open_short(self, price):
        self.position = "SHORT"
        self.entry_price = price

    def close_position(self):
        self.position = None
        self.entry_price = None

    def get_position(self):
        return self.position