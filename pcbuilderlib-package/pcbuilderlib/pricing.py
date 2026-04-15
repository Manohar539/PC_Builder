class PriceCalculator:

    def __init__(self):
        self.total_price = 0

    def add_component(self, price):

        if price:
            self.total_price += int(price)

    def get_total_price(self):
        return self.total_price


def calculate_price(components):

    calculator = PriceCalculator()

    for component in components:

        calculator.add_component(component.get("price", 0))

    return calculator.get_total_price()