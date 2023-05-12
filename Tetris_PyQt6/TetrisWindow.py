from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QAction
import sys
import TetrisGame
import Element
import TimeCounter
import InfoWindow

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 560
BOARD_PART_WIDTH = 290
SQUARE_SIDE = 20


class TetrisWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.game = TetrisGame.TetrisGame()
        self.secondWindow = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tetris')
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.addMenu()
        self.addLabels()
        self.addButtons()
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawBoard(qp)
        self.drawMiniBoard(qp)
        self.scoreLabel.setText("Wynik: " + str(self.game.score))
        self.pause_action.setChecked(self.game.paused)
        self.showPauseEndText()
        qp.end()

    def showPauseEndText(self):
        if self.game.endGame:
            self.endGameLabel.show()
        else:
            self.endGameLabel.hide()
            if self.game.paused:
                self.pauseLabel.show()
            else:
                self.pauseLabel.hide()

    def keyPressEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        if not self.game.endGame:
            # if game is paused
            if self.game.paused:
                if key == Qt.Key.Key_P:
                    self.game.paused = False
            # if game is unpaused
            else:
                if key == Qt.Key.Key_W:
                    self.game.move(TetrisGame.MoveType.TURN)
                elif key == Qt.Key.Key_A:
                    self.game.move(TetrisGame.MoveType.LEFT)
                elif key == Qt.Key.Key_D:
                    self.game.move(TetrisGame.MoveType.RIGHT)
                elif key == Qt.Key.Key_S:
                    self.game.move(TetrisGame.MoveType.DOWNDOWN)
                elif key == Qt.Key.Key_P:
                    self.game.paused = True
            self.update()

    def objectDown(self):
        if not self.game.paused and not self.game.endGame:
            self.game.move(TetrisGame.MoveType.DOWN)
            self.update()

    def drawRectangle(self, qp, col, x, y):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(col)
        qp.drawRect(x, y, SQUARE_SIDE, SQUARE_SIDE)

    def drawBoard(self, qp):
        for row in range(TetrisGame.BOARD_ROW_NR + 2):
            for col in range(TetrisGame.BOARD_COLUMN_NR + 2):
                color = QColor(60, 60, 60)
                if not(row == 0 or row == TetrisGame.BOARD_ROW_NR + 1) and \
                        not(col == 0 or col == TetrisGame.BOARD_COLUMN_NR + 1):
                    color = self.game.board[row - 1 + Element.MINI_BOARD_SIZE][col - 1]
                self.drawRectangle(qp, color, 40+SQUARE_SIDE*col, 80+SQUARE_SIDE*row)

    def drawMiniBoard(self, qp):
        halfRightPart = BOARD_PART_WIDTH + (WINDOW_WIDTH - BOARD_PART_WIDTH)//2
        miniBoardWidth = Element.MINI_BOARD_SIZE * SQUARE_SIDE
        for row in range(Element.MINI_BOARD_SIZE):
            for col in range(Element.MINI_BOARD_SIZE):
                if self.game.nextElement.squares[row][col] == 1:
                    color = self.game.nextElement.color
                else:
                    color = Element.NEUTRAL_COLOR
                self.drawRectangle(
                    qp, color, halfRightPart - miniBoardWidth//2 + SQUARE_SIDE * col, 140 + SQUARE_SIDE * row)

    def addMenu(self):
        self.pause_action = QAction("&Pauza", self)
        self.pause_action.triggered.connect(self.game.pause)
        self.pause_action.setCheckable(True)
        self.pause_action.setChecked(self.game.paused)
        new_game_action = QAction("&Nowa gra", self)
        new_game_action.triggered.connect(self.resetGame)
        end_game_action = QAction("&Koniec gry", self)
        end_game_action.triggered.connect(self.close)

        menu = self.menuBar()
        file_menu = menu.addMenu("&Opcje")
        file_menu.addAction(self.pause_action)
        file_menu.addSeparator()
        file_menu.addAction(new_game_action)
        file_menu.addSeparator()
        file_menu.addAction(end_game_action)

        rules_action = QAction("&Zasady gry", self)
        rules_action.triggered.connect(self.openRules)
        informations_action = QAction("&Informacje", self)
        informations_action.triggered.connect(self.openInformations)

        file_menu = menu.addMenu("&Gra")
        file_menu.addAction(rules_action)
        file_menu.addSeparator()
        file_menu.addAction(informations_action)

    def addLabels(self):
        tetrisLabel = QLabel("Tetris", parent=self)
        tetrisLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tetrisLabel.setStyleSheet("QLabel{font-size: 24pt; font-weight: bold;}")
        tetrisLabel.resize(WINDOW_WIDTH, 2*SQUARE_SIDE)
        tetrisLabel.move(0, 20)

        elementNrLabel = QLabel("Następny element", parent=self)
        elementNrLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        elementNrLabel.resize(WINDOW_WIDTH - BOARD_PART_WIDTH, SQUARE_SIDE)
        elementNrLabel.setStyleSheet("QLabel{font-size: 12pt;}")
        elementNrLabel.move(BOARD_PART_WIDTH, 100)

        scoreString = "Wynik: " + str(self.game.score)
        self.scoreLabel = QLabel(scoreString, parent=self)
        self.scoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scoreLabel.resize(WINDOW_WIDTH - BOARD_PART_WIDTH, 2*SQUARE_SIDE)
        self.scoreLabel.setStyleSheet("QLabel{font-size: 14pt;}")
        self.scoreLabel.move(BOARD_PART_WIDTH, 300)

        self.pauseLabel = QLabel("P A U Z A", parent=self)
        self.pauseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pauseLabel.resize(WINDOW_WIDTH - BOARD_PART_WIDTH, 4*SQUARE_SIDE)
        self.pauseLabel.setStyleSheet("QLabel{font-size: 28pt; color: red}")
        self.pauseLabel.move(BOARD_PART_WIDTH, 220)

        self.endGameLabel = QLabel("Koniec gry", parent=self)
        self.endGameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.endGameLabel.resize(WINDOW_WIDTH - BOARD_PART_WIDTH, 4*SQUARE_SIDE)
        self.endGameLabel.setStyleSheet("QLabel{font-size: 20pt; color: green}")
        self.endGameLabel.move(BOARD_PART_WIDTH, 220)

    def addButtons(self):
        halfRightPart = BOARD_PART_WIDTH + (WINDOW_WIDTH - BOARD_PART_WIDTH)//2
        buttonWidth = (WINDOW_WIDTH - BOARD_PART_WIDTH)//2

        resetButton = QPushButton("RESET", parent=self)
        resetButton.resize(buttonWidth, 2*SQUARE_SIDE)
        resetButton.move(halfRightPart - buttonWidth//2, 380)
        resetButton.clicked.connect(self.resetGame)

        endButton = QPushButton("ZAKOŃCZ", parent=self)
        endButton.resize(buttonWidth, 2*SQUARE_SIDE)
        endButton.move(halfRightPart - buttonWidth//2, 440)
        endButton.clicked.connect(self.close)

    def resetGame(self):
        self.game.newGame()
        self.update()

    def openRules(self):
        self.secondWindow = InfoWindow.InfoWindow(InfoWindow.WindowType.RULES)

    def openInformations(self):
        self.secondWindow = InfoWindow.InfoWindow(InfoWindow.WindowType.INFORMATIONS)


if __name__ == '__main__':
    app = QApplication([])
    tetris = TetrisWindow()

    thread = TimeCounter.TimeCounter(tetris=tetris)
    thread.finished.connect(app.quit)
    thread.start()
    sys.exit(app.exec())
