from enum import Enum
from typing import Tuple

class Color(Enum):
    RED = 0
    BLUE = 1

class Card:
    def __init__(self, color: Color, num: int, id: int = None):
        self.num = num
        self.color = color
        self.id = id or num
        self.value = VALUES[self.color][self.num]
        self.coords: Tuple[int, int, int, int] = tuple()
        self.mult_odds = 1
        self.button = None

    def getValue(self):
        value = self.value*self.mult_odds
        return value

    def get_color_tuple(self):
        return COLOR_TUPLE[self.color]
    
    def alter_odds(self, n):
        self.mult_odds = n
    
    def get_coords(self):
        return self.coords
    
    def get_button(self):
        return self.button

    def determine_coords(self):
        y_level = self.id // 6
        x_order = self.id%6

        y_factor = y_level*(3/5) + 1/3
        x_factor = (x_order+1)*(1/7) 
        height= 250
        width = 150

        self.coords = (x_factor, y_factor, width, height)

COLOR_TUPLE = {
    Color.RED: (224, 49, 70),
    Color.BLUE: (45, 45, 227)
}

VALUES = {
    Color.RED: {1: 55, 2: 10, 3: -5, 4: -25, 5: -50, 0: 0.1},
    Color.BLUE: {1: -269, 2: -169, 3: -101.1, 4: 2.5, 5: 500, 0: -0.1}
}