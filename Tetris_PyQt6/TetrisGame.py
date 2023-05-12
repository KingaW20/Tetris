import Element
from enum import Enum

BOARD_COLUMN_NR = 10
BOARD_ROW_NR = 20


class MoveType(Enum):
    TURN = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4
    DOWNDOWN = 5


class TetrisGame:

    def __init__(self):
        self.board = []
        self.newGame()

    def createEmptyBoard(self):
        self.board = [0] * (BOARD_ROW_NR + Element.MINI_BOARD_SIZE * 2)
        for i in range(BOARD_ROW_NR + Element.MINI_BOARD_SIZE * 2):
            self.board[i] = [Element.NEUTRAL_COLOR] * BOARD_COLUMN_NR

    def newGame(self):
        self.createEmptyBoard()
        self.score = 0
        self.paused = True
        self.endGame = False
        self.waitTime = 800
        self.currentElement = Element.Element()
        self.currentElementCol = (BOARD_COLUMN_NR - Element.MINI_BOARD_SIZE) // 2
        self.currentElementRow = 0
        self.nextElement = Element.Element()

    def pause(self):
        self.paused = not self.paused

    def speedUp(self):
        self.waitTime -= 20
        if self.waitTime < 200:
            self.waitTime = 200

    def changeElement(self):
        self.checkIfEndGame()
        self.currentElement = self.nextElement
        self.currentElementCol = (BOARD_COLUMN_NR - Element.MINI_BOARD_SIZE) // 2
        self.currentElementRow = 0
        self.nextElement = Element.Element()
        self.checkIfRow()

    def checkIfEndGame(self):
        self.endGame = self.currentElementRow < Element.MINI_BOARD_SIZE

    def checkIfRow(self):
        for row in range(BOARD_ROW_NR):
            rowCompleted = True
            for col in range(BOARD_COLUMN_NR):
                if self.board[Element.MINI_BOARD_SIZE + row][col] == Element.NEUTRAL_COLOR:
                    rowCompleted = False
            if rowCompleted:
                self.destroyRow(row)

    def destroyRow(self, rowToDestroy):
        for row in range(rowToDestroy):
            for col in range(BOARD_COLUMN_NR):
                self.board[Element.MINI_BOARD_SIZE + rowToDestroy - row][col] = \
                    self.board[Element.MINI_BOARD_SIZE + rowToDestroy - row - 1][col]
        self.score += 10
        self.speedUp()

    def addNewElementToArray(self):
        for row in range(Element.MINI_BOARD_SIZE):
            for col in range(Element.MINI_BOARD_SIZE):
                if self.currentElement.squares[row][col] == 1:
                    self.board[self.currentElementRow + row][self.currentElementCol + col] = self.currentElement.color

    def clearCurrentElementFromArray(self):
        for row in range(Element.MINI_BOARD_SIZE):
            for col in range(Element.MINI_BOARD_SIZE):
                if self.currentElement.squares[row][col] == 1:
                    self.board[self.currentElementRow + row][self.currentElementCol + col] = Element.NEUTRAL_COLOR

    def move(self, moveType):
        if moveType != MoveType.DOWN or not self.stopCondition(1):
            self.clearCurrentElementFromArray()

        if moveType == MoveType.TURN:
            self.turnIfCan()
        elif moveType == MoveType.LEFT and self.leftCondition():
            self.currentElementCol -= 1
        elif moveType == MoveType.RIGHT and self.rightCondition():
            self.currentElementCol += 1
        elif moveType == MoveType.DOWN:
            self.currentElementRow += 1
            if self.stopCondition():
                self.changeElement()
        elif moveType == MoveType.DOWNDOWN:
            self.moveToTheBottom()
            self.addNewElementToArray()
            self.changeElement()

        self.addNewElementToArray()

    def leftCondition(self):
        canMove = True
        for row in range(Element.MINI_BOARD_SIZE):
            for col in range(Element.MINI_BOARD_SIZE):
                # the leftmost square
                if self.currentElement.squares[row][col] == 1:
                    boardElementCol = self.currentElementCol + col
                    # if it is not the most left column of board
                    if boardElementCol > 0:
                        if self.board[self.currentElementRow + row][boardElementCol - 1] != Element.NEUTRAL_COLOR:
                            canMove = False
                        else:
                            break
                    else:
                        canMove = False
        return canMove

    def rightCondition(self):
        canMove = True
        for row in range(Element.MINI_BOARD_SIZE):
            for col in range(Element.MINI_BOARD_SIZE):
                # the rightmost square
                if self.currentElement.squares[row][Element.MINI_BOARD_SIZE - col - 1] == 1:
                    boardElementCol = self.currentElementCol + Element.MINI_BOARD_SIZE - col - 1
                    # if it is not the most right column of board
                    if boardElementCol < BOARD_COLUMN_NR - 1:
                        if self.board[self.currentElementRow + row][boardElementCol + 1] != Element.NEUTRAL_COLOR:
                            canMove = False
                        else:
                            break
                    else:
                        canMove = False
        return canMove

    def stopCondition(self, addToRow=0):
        stop = False
        for col in range(Element.MINI_BOARD_SIZE):
            for row in range(Element.MINI_BOARD_SIZE):
                # lowest square in column
                if self.currentElement.squares[Element.MINI_BOARD_SIZE - row - 1][col] == 1:
                    boardElementRow = self.currentElementRow + addToRow + Element.MINI_BOARD_SIZE - row - 1
                    # if it is not the last row on board
                    if boardElementRow < BOARD_ROW_NR + Element.MINI_BOARD_SIZE:
                        # if there is an occupied square below
                        if self.board[boardElementRow][self.currentElementCol + col] != Element.NEUTRAL_COLOR:
                            stop = True
                        else:
                            break
                    else:
                        stop = True
        return stop

    def moveToTheBottom(self):
        i = 0
        while not self.stopCondition(i):
            i += 1
        self.currentElementRow += i - 1

    def turnIfCan(self):
        new_element_squares = self.currentElement.getTurnedElement()
        canTurn = True
        for col in range(Element.MINI_BOARD_SIZE):
            for row in range(Element.MINI_BOARD_SIZE):
                boardRow = self.currentElementRow + row
                boardCol = self.currentElementCol + col
                # if new element has here squere
                if new_element_squares[row][col] == 1:
                    if boardCol < 0 or boardCol >= BOARD_COLUMN_NR:
                        canTurn = False
                    elif boardRow >= BOARD_ROW_NR + Element.MINI_BOARD_SIZE:
                        canTurn = False
                    elif self.board[boardRow][boardCol] != Element.NEUTRAL_COLOR:
                        canTurn = False

        if canTurn:
            self.currentElement.squares = new_element_squares
