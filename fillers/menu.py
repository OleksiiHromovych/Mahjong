from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDialog, QPushButton, \
    QVBoxLayout, QListWidget, QLabel, QListWidgetItem


class QCustomQWidget(QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.label = QLabel()

        self.allQVBoxLayout = QVBoxLayout()
        self.iconQLabel = QLabel()

        self.allQVBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQVBoxLayout.addWidget(self.label, 1)
        self.setLayout(self.allQVBoxLayout)

    def setText(self, text):
        self.label.setText(text)

    def setIcon(self, imagePath):
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaled(180, 130)
        self.iconQLabel.setPixmap(pixmap)


class MyListWidget(QListWidget):
    def __init__(self, parent=None, click="standard"):
        super().__init__(parent)
        self.parent = parent
        self.click = click
        self.setFlow(0)
        self.itemClicked.connect(self.on_item_clicked)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._mouse_button = event.button()

    def on_item_clicked(self, item):
        if self.click == "maps":
            self.parent.map = item.text


class Menu(QDialog):
    def __init__(self, parent):
        super(Menu, self).__init__()
        self.setGeometry(400, 200, 650, 500)
        self.setFixedSize(650, 500)
        self.parent = parent
        self.setWindowIcon(QIcon("res/icons/icon.png"))

        self.label = QLabel("New Game", self)

        self.maps = MyListWidget(self, "maps")
        self.map = "Turtle"
        self.button = QPushButton('Start', self)
        self.interface()

    def interface(self):

        self.button.clicked.connect(self.onClicked)

        self.design()
        for text, icon in zip(["Turtle", "Diamond", "Bridge"],
                              ["res/maps/turtle.png", "res/maps/diamand.png", "res/maps/bridge.png"]):

            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setIcon(icon)
            myQListWidgetItem = QListWidgetItem(self.maps)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            myQListWidgetItem.text = text.lower()
            self.maps.addItem(myQListWidgetItem)
            self.maps.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        self.backgrounds = MyListWidget()

        for icon in ["res/background/table-background.png"]:
            iconWidget = QCustomQWidget()
            iconWidget.setIcon(icon)
            iconWidgetItem = QListWidgetItem(self.backgrounds)
            iconWidgetItem.setSizeHint(iconWidget.sizeHint())
            iconWidgetItem.text = icon
            self.backgrounds.addItem(iconWidgetItem)
            self.backgrounds.setItemWidget(iconWidgetItem, iconWidget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.maps)
        layout.addWidget(self.backgrounds)
        layout.addWidget(self.button)

    def design(self):
        self.setStyleSheet("background-color: rgb(24,135,103);")
        self.label.setStyleSheet('font-size: 58pt; font-family: Courier;')
        self.label.setMaximumHeight(50)
        self.label.setAlignment(Qt.AlignHCenter)
        self.maps.setMaximumHeight(200)
        self.button.setMaximumHeight(100)
        self.button.setStyleSheet('font-size: 58pt; font-family: Courier;')

    def onClicked(self):
        self.parent.map = self.map
        self.parent.restart_game()
        self.close()

