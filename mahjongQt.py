import random
import re
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QColorDialog

from fillers import board
from fillers.endgame import EndGame
from fillers.menu import Menu
from fillers.tileQt import Tile


class Mahjong(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = board.Ui_MainWindow()
        self.ui.setupUi(self)

        self.tiles = []
        self.chosen_tile = None
        self.map = None
        self.dialog = Menu(self)
        self.end_game = EndGame(self)
        self.setup_board_element()
        self.dialog.exec_()
        if self.map is None:
            sys.exit()

    def setup_board_element(self):
        self.setWindowTitle("Mahjong")

        self.setWindowIcon(QIcon("res/icons/icon.png"))
        self.ui.label.setPixmap(QPixmap("res/background/table-background.png").scaled(self.width(), self.height()))
        self.ui.mask.setStyleSheet("background-color: rgba(20,250,20, 70)")
        self.ui.mask.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.ui.first_prompt.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.ui.second_prompt.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.ui.restart.triggered.connect(self.restart_game)
        self.ui.restart.setShortcut("Ctrl+R")
        self.ui.goMenu.triggered.connect(self.dialog.exec_)
        self.ui.showInfo.triggered.connect(self.show_info)
        self.ui.prompt.triggered.connect(self.prompt)
        self.ui.prompt.setShortcut("Ctrl+P")
        self.ui.change_color.triggered.connect(self.openColorDialog)

    def __get_map(self, file="bridge", level=5):

        with open("levels/" + file) as f:
            if f:
                text = f.read()
                tiles = [[] for _ in range(level)]

                for x, y, z in re.findall('[(](\d+),(\d+),(\d+)[))]', text):
                    tiles[int(z) - 1].append((int(x), int(y), int(z)))

        for i in tiles:
            i.sort(key=lambda tile: (tile[0], -tile[1]))

        icon_list = []
        with open("res/text/icon_name.txt", "r") as f:
            phantom_list = f.read().split("\n")

        icon_list.extend(phantom_list[0].split(","))
        icon_list = [val for val in icon_list for _ in range(2)]
        random.shuffle(icon_list)
        icon_list = [val for val in icon_list for _ in range(2)]

        unique_icon = phantom_list[1].split(",")

        for icon_index in range(0, len(unique_icon), 2):
            index = random.randint(0, len(icon_list))
            if index % 2:
                index -= 1
            icon_list.insert(index, unique_icon[icon_index])
            icon_list.insert(index, unique_icon[icon_index + 1])

        start_index = 0
        for tiles_row in tiles:

            icon_row = icon_list[start_index:len(tiles_row) + start_index]
            random.shuffle(icon_row)
            start_index += len(tiles_row)
            for x, y, z in tiles_row:
                icon = icon_row.pop()
                if icon in unique_icon[:4]:
                    self.tiles.append(Tile(self.ui.centralwidget, "flower", (int(x), int(y), int(z)),
                                           icon, self.check))
                elif icon in unique_icon[4:]:
                    self.tiles.append(Tile(self.ui.centralwidget, "season", (int(x), int(y), int(z)),
                                           icon, self.check))
                else:
                    self.tiles.append(Tile(self.ui.centralwidget, icon, (int(x), int(y), int(z)),
                                           icon, self.check))
        sorted(self.tiles, key=lambda tile: tile.x)

    def prompt(self):
        for tile in self.tiles[::-1]:

            for tile2 in self.tiles[::-1]:
                if tile.value == tile2.value and tile is not tile2 and \
                        tile.is_active(self.tiles) and tile2.is_active(self.tiles):
                    self.ui.first_prompt.move(tile.pos())
                    self.ui.second_prompt.move(tile2.pos())
                    self.ui.first_prompt.show()
                    self.ui.second_prompt.show()

                    return
        else:
            self.end_game.setContent(False, f"You time is {time.time() - self.time_start},"
                                            f" tiles left {len(self.tiles)}")
            self.end_game.exec_()

    def start_game(self):
        self.tiles.clear()
        self.__get_map(self.map)
        self.time_start = time.time()
        self.ui.mask.setFixedSize(self.tiles[0].size())

        self.ui.first_prompt.setPixmap(QPixmap("res/icons/prompt.png").scaled(self.tiles[0].size()))
        self.ui.first_prompt.hide()

        self.ui.second_prompt.setPixmap(QPixmap("res/icons/prompt.png").scaled(self.tiles[0].size()))
        self.ui.second_prompt.hide()

        self.ui.mask.hide()
        self.ui.first_prompt.raise_()
        self.ui.second_prompt.raise_()
        self.ui.mask.raise_()
        for tile in self.tiles:
            tile.show()

    def restart_game(self):

        for tile in self.tiles:
            tile.deleteLater()
        self.tiles.clear()
        self.__get_map(self.map)
        self.time_start = time.time()
        self.ui.mask.hide()
        self.ui.first_prompt.hide()
        self.ui.first_prompt.raise_()
        self.ui.second_prompt.hide()
        self.ui.second_prompt.raise_()
        self.ui.mask.raise_()
        for tile in self.tiles:
            tile.show()

    def show_info(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Info")
        with open("res/text/info.txt", 'r') as f:
            text = f.read()
        msg.setWindowIcon(QIcon("res/icons/icon.png"))

        msg.setText(text)

        msg.exec_()

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.ui.mask.setStyleSheet("background-color: rgba" + str((*color.getRgb()[:3], 70)))

    def check(self, tile):
        if self.chosen_tile:
            if self.chosen_tile is tile:
                self.chosen_tile = None
                self.ui.mask.hide()
                return

            if tile.is_active(self.tiles):
                if tile.value == self.chosen_tile.value:

                    self.tiles.remove(self.chosen_tile)
                    self.chosen_tile.hide()
                    self.tiles.remove(tile)
                    tile.hide()
                    self.ui.mask.hide()
                    self.chosen_tile = None

                    if self.ui.first_prompt.isVisible() or self.ui.second_prompt.isVisible():
                        self.ui.first_prompt.hide()
                        self.ui.second_prompt.hide()

                else:
                    self.ui.mask.move(tile.pos())
                    self.chosen_tile = tile

        else:

            if tile.is_active(self.tiles):
                self.ui.mask.move(tile.pos())
                self.ui.mask.show()

                self.chosen_tile = tile

        if not self.tiles:
            utime = int(time.time() - self.time_start)
            self.end_game.setContent(True,
                                     f"You time is {utime // 60}m. {utime % 60}s.")
            self.end_game.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Mahjong()
    application.show()

    sys.exit(app.exec())
