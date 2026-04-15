class PowerCalculator:

    def __init__(self):
        self.total_power = 0

    def add_component(self, power):

        if power:
            self.total_power += int(power)

    def get_total_power(self):
        return self.total_power

    def recommend_psu(self):
        return self.total_power + 200


def calculate_power(components):

    calculator = PowerCalculator()

    for component in components:

        calculator.add_component(component.get("power", 0))

    return {
        "total_power": calculator.get_total_power(),
        "recommended_psu": calculator.recommend_psu()
    }