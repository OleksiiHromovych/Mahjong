from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, \
    QVBoxLayout, QListWidget, QLabel


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()

        self.allQVBoxLayout = QtWidgets.QVBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()

        self.allQVBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQVBoxLayout.addWidget(self.label, 1)
        self.setLayout(self.allQVBoxLayout)

    def setText(self, text):
        self.label.setText(text)

    def setIcon(self, imagePath):
        pixmap = QtGui.QPixmap(imagePath)
        pixmap = pixmap.scaled(180,130)
        self.iconQLabel.setPixmap(pixmap)


class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFlow(0)
        self.itemClicked.connect(self.on_item_clicked)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._mouse_button = event.button()

    def on_item_clicked(self, item):
        self.parent.map = item.text


class Menu(QDialog):
    def __init__(self, info):
        super(Menu, self).__init__()
        self.setGeometry(400, 200, 650, 500)
        self.setFixedSize(650, 500)
        self.info = info
        self.label = QLabel("New Game", self)

        self.maps = MyListWidget(self)
        self.map = "Turtle"
        self.button = QPushButton('Start', self)
        self.button.clicked.connect(self.onClicked)

        self.design()
        for text, icon in zip(["Turtle", "Diamond", "Bridge"],
                              ["res/maps/turtle.png", "res/maps/diamand.png", "res/maps/bridge.png"]):

            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setIcon(icon)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.maps)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            myQListWidgetItem.text = text.lower()
            self.maps.addItem(myQListWidgetItem)
            self.maps.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        # self.backgrounds = MyListWidget()
        #
        # for icon in ["table-background.png"]:
        #     iconWidget = QCustomQWidget()
        #     iconWidget.setIcon(icon, (80, 100))
        #     iconWidgetItem = QtWidgets.QListWidgetItem(self.backgrounds)
        #     iconWidgetItem.setSizeHint(iconWidget.sizeHint())
        #     iconWidgetItem.text = icon
        #     self.backgrounds.addItem(iconWidgetItem)
        #     self.backgrounds.setItemWidget(iconWidgetItem, iconWidget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.maps)
        # layout.addWidget(self.backgrounds)
        layout.addWidget(self.button)

    def design(self):

        self.label.setMaximumHeight(50)
        self.label.setAlignment(Qt.AlignHCenter)
        self.maps.setMaximumHeight(200)
        self.button.setMaximumHeight(100)

    def onClicked(self):
        self.info.map = self.map
        self.close()

