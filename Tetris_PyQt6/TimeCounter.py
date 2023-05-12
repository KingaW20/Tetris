from PyQt6 import QtCore


class TimeCounter(QtCore.QThread):
    def __init__(self, tetris):
        super().__init__()
        self.tetrisGame = tetris

    def run(self):
        while True:
            if not self.tetrisGame.game.paused and not self.tetrisGame.game.endGame:
                self.msleep(self.tetrisGame.game.waitTime)
                self.tetrisGame.objectDown()
