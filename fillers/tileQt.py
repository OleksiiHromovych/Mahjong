from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QIcon


class Tile(QtWidgets.QLabel):

    def __init__(self, parent, value, posxyz, icon, function, card_size=(40, 60)):
        super().__init__(parent)
        self.n = 9
        self.value = value
        self.x = posxyz[0] + 150
        self.y = posxyz[1]
        self.z = posxyz[2]
        self.setWindowIcon(QIcon("res/icons/icon.png"))

        self.function = function

        self.card_size = (card_size[0], card_size[1])
        self.setGeometry(QRect(self.x - self.z * 3, self.y - self.z * 3, self.card_size[0]+self.n,
                                      self.card_size[1]+self.n))
        self.set_image(icon)

        self.setObjectName("label")

    def set_image(self, value="1.png"):
        pixmap = QPixmap("res/tiles/" + value)
        pixmap = pixmap.scaled(self.card_size[0] + self.n, self.card_size[1] + self.n)
        self.setStyleSheet("background-color: transparent;")
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.function(self)

    def is_active(self, tiles: list):
        """
        Tile active if it is free left and right, and above. Left and right False on default - free.
        """
        left = False
        right = False
        half_x = self.card_size[0] / 2
        half_y = self.card_size[1] / 2

        for tile in tiles:
            # When tile on half of another tile
            if tile.z > self.z:
                if ((tile.x + half_x == self.x or tile.x - half_x == self.x) and
                    (tile.y + half_y == self.y or tile.y - half_y == self.y)) or \
                        (tile.x == self.x and tile.y == self.y) or \
                        (tile.x == self.x and (tile.y + half_y == self.y or tile.y - half_y == self.y)) or \
                        (tile.y == self.y and (tile.x + half_x == self.x or tile.x - half_x == self.x)):

                    return False
            # Check against even-level touching pieces.
            if tile.z == self.z:
                if tile.y == self.y:
                    if tile.x - 2 * half_x == self.x:
                        right = True
                    if tile.x + 2 * half_x == self.x:
                        left = True

                if (tile.y + half_y == self.y and tile.x - 2 * half_x == self.x) or \
                        (tile.y - half_y == self.y and tile.x - 2 * half_x == self.x):
                    right = True
                if (tile.y - half_y == self.y and tile.x + 2 * half_x == self.x) or \
                        (tile.y + half_y == self.y and tile.x + 2 * half_x == self.x):
                    left = True

        return not (left and right)
