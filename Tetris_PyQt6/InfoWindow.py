from PyQt6.QtWidgets import QLabel, QWidget
from enum import Enum

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 350
INFO_WINDOW_HEIGHT = 200


class WindowType(Enum):
    RULES = 1
    INFORMATIONS = 2


class InfoWindow(QWidget):

    def __init__(self, windowType=WindowType.INFORMATIONS):
        super().__init__()
        self.windowType = windowType
        if self.windowType == WindowType.RULES:
            self.height = WINDOW_HEIGHT
        else:
            self.height = INFO_WINDOW_HEIGHT
        self.setGeometry(140, 220, WINDOW_WIDTH, self.height)
        self.setFixedSize(WINDOW_WIDTH, self.height)
        self.addText()
        self.show()

    def addText(self):
        if self.windowType == WindowType.RULES:
            title = "Zasady gry"
        else:
            title = "Informacje"
        self.setWindowTitle(title)

        if self.windowType == WindowType.RULES:
            text = "Zadaniem gracza jest obracanie i przesuwanie elementów w poziomie tak, aby kwadraty, " \
                   "z których się składają, utworzyły wiersz na całej szerokości planszy, który zostanie " \
                   "usunięty oraz zwiększy wynik gracza o 10 punktów.\n\n" \
                   "Gracz porusza się prawo-lewo przy pomocy odpowiednio D oraz A, natomiast obraca " \
                   "obiekt klawiszem W. Dodatkowo ma możliwość przyspieszenia obiektu dzięki naciśnięciu na S.\n\n" \
                   "Dodatkowo istnieje możliwość zatrzymania gry przyciskiem P i jej wznowienia poprzez " \
                   "ponowne przyciśnięcie tego klawisza."
        else:
            text = "Gra została wytworzona w ramach projektu z przedmiotu Języki Skryptowe\n\n" \
                   "Wykorzystano bibliotekę PyQt6\n\n" \
                   "Autorka: Kinga Widła"

        tetrisLabel = QLabel(text, parent=self)
        tetrisLabel.setWordWrap(True)
        tetrisLabel.setStyleSheet("QLabel{font-size: 10pt;}")
        tetrisLabel.resize(WINDOW_WIDTH * 3 // 4, self.height * 3 // 4)
        tetrisLabel.move(WINDOW_WIDTH // 8, self.height // 8)
