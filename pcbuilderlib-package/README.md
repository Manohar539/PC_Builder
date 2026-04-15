# pcbuilderlib

A simple Python library for PC building calculations.

## Features

- Calculate total price
- Calculate power usage
- Recommend PSU wattage
- Check CPU and motherboard compatibility
- Estimate PC performance

## Installation

pip install pcbuilderlib

## Example

```python
from pcbuilderlib import calculate_price, calculate_power

components = [
    {"price": 300, "power": 95},
    {"price": 500, "power": 250}
]

print(calculate_price(components))
print(calculate_power(components))