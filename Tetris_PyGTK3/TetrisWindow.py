import gi
import TetrisGame
import Element
import InfoWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Pango

SQUARE_SIDE = 25
WINDOW_WIDTH = int(SQUARE_SIDE * 24)
WINDOW_HEIGHT = int(SQUARE_SIDE * 28)
BOARD_PART_WIDTH = int(SQUARE_SIDE * 14.5)
SPACING = 1


class TetrisWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Tetris")
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_resizable(False)
        self.game = TetrisGame.TetrisGame()
        self.second_window = None

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.box)
        self.createInterface()

        self.connect("key_press_event", self.key_events)
        self.objectDown()

    def key_events(self, widget, event):
        key = event.keyval
        if not self.game.endGame:
            # if game is paused
            if self.game.paused:
                # P
                if key == 112:
                    self.pauseGame(None)
            # if game is unpaused
            else:
                # W
                if key == 119:
                    self.game.move(TetrisGame.MoveType.TURN)
                # L
                elif key == 97:
                    self.game.move(TetrisGame.MoveType.LEFT)
                # R
                elif key == 100:
                    self.game.move(TetrisGame.MoveType.RIGHT)
                # S
                elif key == 115:
                    self.game.move(TetrisGame.MoveType.DOWNDOWN)
                # P
                elif key == 112:
                    self.pauseGame(None)
            self.update()

    def objectDown(self):
        if not self.game.paused and not self.game.endGame:
            self.game.move(TetrisGame.MoveType.DOWN)
            self.update()
        GLib.timeout_add(self.game.waitTime, self.objectDown)

    def drawBoard(self, widgt, cr):
        # black background - lines between squares
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(SQUARE_SIDE * 2, 0,
                     SQUARE_SIDE * (TetrisGame.BOARD_COLUMN_NR + 2), SQUARE_SIDE * (TetrisGame.BOARD_ROW_NR + 2))
        cr.fill()

        for row in range(TetrisGame.BOARD_ROW_NR + 2):
            for col in range(TetrisGame.BOARD_COLUMN_NR + 2):
                color = Element.Color(60, 60, 60)
                if not(row == 0 or row == TetrisGame.BOARD_ROW_NR + 1) and \
                        not(col == 0 or col == TetrisGame.BOARD_COLUMN_NR + 1):
                    color = self.game.board[row - 1 + Element.MINI_BOARD_SIZE][col - 1]
                cr.set_source_rgb(color.red, color.green, color.blue)
                cr.rectangle(SQUARE_SIDE * (col + 2) + SPACING, SQUARE_SIDE * row + SPACING,
                             SQUARE_SIDE - 2 * SPACING, SQUARE_SIDE - 2 * SPACING)
                cr.fill()

    def createInterface(self):
        self.upper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.addMenu()
        self.addTetrisLabel()
        self.box.pack_start(self.upper, False, False, 0)

        self.leftBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.rightBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.mainBoard = Gtk.DrawingArea()
        self.mainBoard.connect("draw", self.drawBoard)
        self.mainBoard.set_size_request(BOARD_PART_WIDTH, WINDOW_HEIGHT - 5 * SQUARE_SIDE)
        self.leftBox.pack_start(self.mainBoard, False, False, 0)

        self.addRightPanel()
        self.bottom.pack_start(self.leftBox, False, False, 0)
        self.bottom.pack_start(self.rightBox, False, False, 0)
        self.box.pack_start(self.bottom, False, False, 0)

    def addTetrisLabel(self):
        self.tetrisLabel = Gtk.Label(label="Tetris")
        self.tetrisLabel.override_font(Pango.FontDescription("Arial 24"))
        self.tetrisLabel.set_halign(Gtk.Align.CENTER)
        self.tetrisLabel.set_margin_top(SQUARE_SIDE // 2)
        self.tetrisLabel.set_margin_bottom(SQUARE_SIDE // 2)
        self.tetrisLabel.set_size_request(WINDOW_WIDTH, SQUARE_SIDE * 2)
        self.upper.pack_start(self.tetrisLabel, False, False, 0)

    def addRightPanel(self):
        self.addNextElementLabel()
        self.miniBoard = Gtk.DrawingArea()
        self.miniBoard.connect("draw", self.drawMiniBoard)
        self.miniBoard.set_size_request(WINDOW_WIDTH - BOARD_PART_WIDTH, 4 * SQUARE_SIDE + 2 * SPACING)
        self.rightBox.pack_start(self.miniBoard, False, False, 0)

        self.addInfoLabel()
        self.addScoreLabel()
        self.addResetButton()
        self.addEndButton()

    def addNextElementLabel(self):
        self.nextElementLabel = Gtk.Label(label="Następny element")
        self.nextElementLabel.override_font(Pango.FontDescription("Arial 12"))
        self.nextElementLabel.set_halign(Gtk.Align.END)
        self.nextElementLabel.set_margin_top(SQUARE_SIDE)
        self.nextElementLabel.set_size_request(WINDOW_WIDTH - BOARD_PART_WIDTH, SQUARE_SIDE)
        self.rightBox.pack_start(self.nextElementLabel, False, False, 0)

    def drawMiniBoard(self, widgt, cr):
        # black background - lines between squares
        boardX = int(SQUARE_SIDE * 2.8)
        boardY = SPACING
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(boardX - SPACING, boardY - SPACING,
                     SQUARE_SIDE * Element.MINI_BOARD_SIZE + 2 * SPACING,
                     SQUARE_SIDE * Element.MINI_BOARD_SIZE + 2 * SPACING)
        cr.fill()

        for row in range(Element.MINI_BOARD_SIZE):
            for col in range(Element.MINI_BOARD_SIZE):
                if self.game.nextElement.squares[row][col] == 1:
                    color = self.game.nextElement.color
                else:
                    color = Element.NEUTRAL_COLOR
                cr.set_source_rgb(color.red, color.green, color.blue)
                cr.rectangle(boardX + SQUARE_SIDE * col + SPACING, boardY + SQUARE_SIDE * row + SPACING,
                             SQUARE_SIDE - 2 * SPACING, SQUARE_SIDE - 2 * SPACING)
                cr.fill()


    def addScoreLabel(self):
        self.scoreLabelText = "Wynik: " + str(self.game.score)
        self.scoreLabel = Gtk.Label(label=self.scoreLabelText)
        self.scoreLabel.override_font(Pango.FontDescription("Arial 14"))
        self.scoreLabel.set_halign(Gtk.Align.END)
        self.scoreLabel.set_size_request(WINDOW_WIDTH - BOARD_PART_WIDTH, SQUARE_SIDE * 2)
        self.rightBox.pack_start(self.scoreLabel, False, False, 0)

    def addResetButton(self):
        self.resetButton = Gtk.Button(label="RESET")
        self.resetButton.connect("clicked", self.resetGame)
        self.resetButton.set_halign(Gtk.Align.END)
        self.resetButton.set_margin_top(SQUARE_SIDE * 2)
        self.resetButton.set_margin_right((WINDOW_WIDTH - BOARD_PART_WIDTH) // 4)
        self.resetButton.set_size_request((WINDOW_WIDTH - BOARD_PART_WIDTH) // 2, SQUARE_SIDE * 2)
        self.rightBox.pack_start(self.resetButton, False, False, 0)

    def addEndButton(self):
        self.endButton = Gtk.Button(label="ZAKOŃCZ")
        self.endButton.connect("clicked", self.close)
        self.endButton.set_halign(Gtk.Align.END)
        self.endButton.set_margin_top(SQUARE_SIDE)
        self.endButton.set_margin_right((WINDOW_WIDTH - BOARD_PART_WIDTH) // 4)
        self.endButton.set_size_request((WINDOW_WIDTH - BOARD_PART_WIDTH) // 2, SQUARE_SIDE * 2)
        self.rightBox.pack_start(self.endButton, False, False, 0)

    def addInfoLabel(self):
        self.infoLabel = Gtk.Label(label="P A U Z A")
        self.infoLabel.override_font(Pango.FontDescription("Arial 28"))
        self.infoLabel.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))
        self.infoLabel.set_halign(Gtk.Align.END)
        self.infoLabel.set_size_request(WINDOW_WIDTH - BOARD_PART_WIDTH, SQUARE_SIDE * 4)
        self.rightBox.pack_start(self.infoLabel, False, False, 0)

    def resetGame(self, button):
        self.game.newGame()
        self.update()

    def pauseGame(self, button):
        self.game.pause()
        self.showPauseEndText()

    def close(self, button):
        Gtk.main_quit()

    def update(self):
        self.mainBoard.queue_draw()
        self.miniBoard.queue_draw()
        self.scoreLabelText = "Wynik: " + str(self.game.score)
        self.scoreLabel.set_text(self.scoreLabelText)
        self.showPauseEndText()

    def showPauseEndText(self):
        if self.game.endGame:
            self.infoLabel.set_text("KONIEC GRY")
            self.infoLabel.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 0, 1))
            self.infoLabel.show()
            self.scoreLabel.set_margin_top(0)
        else:
            if self.game.paused:
                self.infoLabel.set_text("P A U Z A")
                self.infoLabel.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))
                self.infoLabel.show()
                self.scoreLabel.set_margin_top(0)
            else:
                self.infoLabel.hide()
                self.scoreLabel.set_margin_top(SQUARE_SIDE * 4)

    def addMenu(self):
        self.menu_bar = Gtk.MenuBar()
        self.menu_bar.set_size_request(WINDOW_WIDTH, SQUARE_SIDE)

        options_menu = Gtk.Menu()
        options = Gtk.MenuItem("Opcje")
        options.set_submenu(options_menu)
        self.pause_game_action = Gtk.MenuItem("Pauza")
        self.pause_game_action.connect("activate", self.pauseGame)
        options_menu.append(self.pause_game_action)
        new_game_action = Gtk.MenuItem("Nowa gra")
        new_game_action.connect("activate", self.resetGame)
        options_menu.append(new_game_action)
        end_game_action = Gtk.MenuItem("Koniec gry")
        end_game_action.connect("activate", self.close)
        options_menu.append(end_game_action)

        game_menu = Gtk.Menu()
        game = Gtk.MenuItem("Gra")
        game.set_submenu(game_menu)
        rules_action = Gtk.MenuItem("Zasady gry")
        rules_action.connect("activate", self.openRules)
        game_menu.append(rules_action)
        informations_action = Gtk.MenuItem("Informacje")
        informations_action.connect("activate", self.openInformations)
        game_menu.append(informations_action)

        self.menu_bar.append(options)
        self.menu_bar.append(game)
        self.upper.add(self.menu_bar)

    def openRules(self, button):
        self.second_window = InfoWindow.InfoWindow(self, InfoWindow.WindowType.RULES)
        self.second_window.run()
        self.second_window.destroy()

    def openInformations(self, button):
        self.second_window = InfoWindow.InfoWindow(self, InfoWindow.WindowType.INFORMATIONS)
        self.second_window.run()
        self.second_window.destroy()


win = TetrisWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
