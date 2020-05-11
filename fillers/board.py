from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1150, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.mask = QtWidgets.QLabel(self.centralwidget)
        self.mask.setObjectName("mask")
        self.first_prompt = QtWidgets.QLabel(self.centralwidget)
        self.second_prompt = QtWidgets.QLabel(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1154, 26))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuPoints")

        self.restart = QtWidgets.QAction(MainWindow)
        self.restart.setObjectName("restart")
        self.goMenu = QtWidgets.QAction(MainWindow)
        self.goMenu.setObjectName("goMenu")
        self.change_color = QtWidgets.QAction(MainWindow)
        self.change_color.setObjectName("change_color")
        self.showInfo = QtWidgets.QAction(MainWindow)
        self.showInfo.setObjectName("goMenu")
        self.prompt = QtWidgets.QAction(MainWindow)
        self.prompt.setObjectName("prompt")

        self.menuOptions.addAction(self.restart)
        self.menuOptions.addAction(self.prompt)
        self.menuOptions.addAction(self.goMenu)
        self.menuOptions.addAction(self.change_color)
        self.menuOptions.addAction(self.showInfo)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuOptions.setTitle(_translate("MainWindow", "Option"))

        self.restart.setText(_translate("MainWindow", "Restart"))
        self.goMenu.setText(_translate("MainWindow", "Menu"))
        self.prompt.setText(_translate("MainWindow", "Prompt"))
        self.showInfo.setText(_translate("MainWindow", "Info"))
        self.change_color.setText(_translate("MainWindow", "Color of card"))
