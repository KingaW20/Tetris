import random
from enum import Enum
from PyQt6.QtGui import QColor

MINI_BOARD_SIZE = 4
NEUTRAL_COLOR = QColor(220, 220, 220)


class ElementType(Enum):
    I = 1
    T = 2
    O = 3
    L = 4
    J = 5
    S = 6
    Z = 7


class Element:
    def __init__(self):
        r = random.randrange(7)
        self.type = ElementType(r + 1)
        self.squares = [0] * MINI_BOARD_SIZE
        self.color = NEUTRAL_COLOR
        for row in range(MINI_BOARD_SIZE):
            self.squares[row] = [0] * MINI_BOARD_SIZE
        self.setProperties()

    def setProperties(self):
        if self.type == ElementType.I:
            self.color = QColor(255, 0, 0)
            for row in range(MINI_BOARD_SIZE):
                self.squares[row][1] = 1
        elif self.type == ElementType.T:
            self.color = QColor(120, 120, 120)
            self.squares[1][0] = 1
            self.squares[1][1] = 1
            self.squares[1][2] = 1
            self.squares[2][1] = 1
        elif self.type == ElementType.O:
            self.color = QColor(26, 255, 255)
            self.squares[1][1] = 1
            self.squares[1][2] = 1
            self.squares[2][1] = 1
            self.squares[2][2] = 1
        elif self.type == ElementType.L:
            self.color = QColor(255, 255, 0)
            self.squares[0][1] = 1
            self.squares[1][1] = 1
            self.squares[2][1] = 1
            self.squares[2][2] = 1
        elif self.type == ElementType.J:
            self.color = QColor(255, 51, 204)
            self.squares[0][2] = 1
            self.squares[1][2] = 1
            self.squares[2][2] = 1
            self.squares[2][1] = 1
        elif self.type == ElementType.S:
            self.color = QColor(0, 0, 255)
            self.squares[1][1] = 1
            self.squares[1][2] = 1
            self.squares[2][0] = 1
            self.squares[2][1] = 1
        elif self.type == ElementType.Z:
            self.color = QColor(0, 255, 0)
            self.squares[1][0] = 1
            self.squares[1][1] = 1
            self.squares[2][1] = 1
            self.squares[2][2] = 1

    def getTurnedElement(self):
        new_squares = [[self.squares[j][i] for j in range(MINI_BOARD_SIZE)] for i in range(MINI_BOARD_SIZE - 1, -1, -1)]
        return new_squares
