from enum import Enum
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 250
INFO_WINDOW_HEIGHT = 150


class WindowType(Enum):
    RULES = 1
    INFORMATIONS = 2


class InfoWindow(Gtk.Dialog):

    def __init__(self, parent, windowType=WindowType.INFORMATIONS):
        self.windowType = windowType
        if self.windowType == WindowType.RULES:
            title = "Zasady gry"
            self.height = WINDOW_HEIGHT
        else:
            title = "Informacje"
            self.height = INFO_WINDOW_HEIGHT
        Gtk.Dialog.__init__(self, title, parent)
        self.set_default_size(WINDOW_WIDTH, self.height)
        self.set_resizable(False)

        self.addText()
        self.show_all()

    def addText(self):

        if self.windowType == WindowType.RULES:
            text = "Zadaniem gracza jest obracanie i przesuwanie elementów w poziomie tak,\naby kwadraty, " \
                   "z których się składają, utworzyły wiersz\nna całej szerokości planszy,który zostanie " \
                   "usunięty\noraz zwiększy wynik gracza o 10 punktów.\n\n" \
                   "Gracz porusza się prawo-lewo przy pomocy odpowiednio D oraz A,\nnatomiast obraca " \
                   "obiekt klawiszem W. Dodatkowo ma możliwość\nprzyspieszenia obiektu dzięki naciśnięciu na S.\n\n" \
                   "Dodatkowo istnieje możliwość zatrzymania gry przyciskiem P\ni jej wznowienia poprzez " \
                   "ponowne przyciśnięcie tego klawisza."
        else:
            text = "Gra została wytworzona w ramach projektu z przedmiotu Języki Skryptowe\n\n" \
                   "Wykorzystano bibliotekę PyGTK3\n\n" \
                   "Autorka: Kinga Widła"

        tetrisLabel = Gtk.Label(text)
        tetrisLabel.set_size_request(WINDOW_WIDTH, self.height)

        box = self.get_content_area()
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_left(20)
        box.set_margin_right(20)
        box.add(tetrisLabel)
