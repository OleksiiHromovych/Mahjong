import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QTextBrowser, QVBoxLayout, QLabel, QPushButton


class EndGame(QDialog):

    def __init__(self, parent):
        super(EndGame, self).__init__()
        self.setGeometry(400, 200, 600, 600)
        self.setFixedSize(600, 500)
        self.parent = parent
        self.setWindowIcon(QIcon("res/icons/icon.png"))

        vlayout = QVBoxLayout(self)
        hlayout = QHBoxLayout()
        self.label = QLabel(self)

        exit = QPushButton("Exit", self)
        restart = QPushButton("Restart", self)
        self.main_text = QTextBrowser(self)

        hlayout.addWidget(exit)
        hlayout.addWidget(restart)
        vlayout.addWidget(self.label)
        vlayout.addWidget(self.main_text)
        vlayout.addLayout(hlayout)
        restart.clicked.connect(self.parent.restart_game)
        restart.clicked.connect(self.close)
        exit.clicked.connect(lambda: sys.exit(self.parent))

        self.label.setAlignment(Qt.AlignHCenter)
        self.main_text.setMaximumHeight(100)
        self.main_text.setStyleSheet('font-size: 58pt; font-family: Courier;')

    def setContent(self, win: bool = True, message: str = "Nice game"):
        if win:
            self.label.setPixmap(QPixmap("res/icons/win.png"))

        else:
            self.label.setPixmap(QPixmap("res/icons/lose.png"))

        self.main_text.setText(message)

