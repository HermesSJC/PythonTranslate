from PySide2.QtWidgets import QPushButton,QWidget,QGridLayout,QLabel,QLineEdit,QTextEdit,QComboBox,QFileDialog
from PySide2.QtCore import Qt,QDateTime,Signal
import json
import urllib
from hashlib import md5
import http.client as httplib
import random

class Widget(QWidget):
    def __init__(self):

        QWidget.__init__(self)

        self.__time = QDateTime()

        self.__appIDLabel = QLabel("AppID:")
        self.__appIDLineEdit = QLineEdit()

        self.__keyLabel = QLabel("Key:")
        self.__keyLineEdit = QLineEdit()

        self.__fromLabel = QLabel("From:")
        self.__fromComboBox = QComboBox()
        self.__fromComboBox.clear()
        self.__fromComboBox.addItem("English","en")
        self.__fromComboBox.addItem("Chinese","zh")
        self.__fromComboBox.addItem("Auto","auto")
        self.__fromComboBox.setCurrentIndex(0)

        self.__toLabel = QLabel("To:")
        self.__toComboBox = QComboBox()
        self.__toComboBox.clear()
        self.__toComboBox.addItem("English","en")
        self.__toComboBox.addItem("Chinese","zh")
        self.__toComboBox.setCurrentIndex(1)

        self.__srcLabel = QLabel("Src Text:")
        self.__srcTextEdit = QTextEdit()

        self.__chooseFileButton = QPushButton("Choose File")
        self.__translateButton = QPushButton("Translate")
        self.__clearButton = QPushButton("Clear")
        self.__historyButton = QPushButton("History")

        self.__translateLabel = QLabel("Translate Text:")
        self.__translateTextEdit = QTextEdit()

        self.__statusLabel = QLabel(self.__GetCurrentTime() + " - Please choose a file or enter the text")

        self.__mainLayout = QGridLayout()
        self.__mainLayout.addWidget(self.__appIDLabel, 0, 0)
        self.__mainLayout.addWidget(self.__appIDLineEdit, 0, 1, 1, 3)
        self.__mainLayout.addWidget(self.__keyLabel, 1, 0)
        self.__mainLayout.addWidget(self.__keyLineEdit, 1, 1, 1, 3)
        self.__mainLayout.addWidget(self.__fromLabel,2, 0)
        self.__mainLayout.addWidget(self.__fromComboBox, 2, 1)
        self.__mainLayout.addWidget(self.__toLabel, 2, 2)
        self.__mainLayout.addWidget(self.__toComboBox, 2, 3)
        self.__mainLayout.addWidget(self.__srcLabel, 3, 0)
        self.__mainLayout.addWidget(self.__srcTextEdit, 3, 1, 1, 3)
        self.__mainLayout.addWidget(self.__chooseFileButton, 4, 0)
        self.__mainLayout.addWidget(self.__translateButton, 4, 1)
        self.__mainLayout.addWidget(self.__clearButton, 4, 2)
        self.__mainLayout.addWidget(self.__historyButton, 4, 3)
        self.__mainLayout.addWidget(self.__translateLabel, 5, 0)
        self.__mainLayout.addWidget(self.__translateTextEdit, 5 ,1, 1 ,3)
        self.__mainLayout.addWidget(self.__statusLabel, 6, 0, 1, 4)
        self.setLayout(self.__mainLayout)

        self.show()

    def __GetCurrentTime(self,format = "hh:mm:ss"):
        return self.__time.currentDateTime().toString(format)

    def __on_clicked_chooseFileButton(self):
        pass

    def __on_clicked_translateButton(self):
        pass

    def __on_clicked_clearButton(self):
        pass

    def __on_clicked_historyButton(self):
        pass