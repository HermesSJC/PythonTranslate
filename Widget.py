from PySide2.QtWidgets import QPushButton,QWidget,QGridLayout,QLabel,QLineEdit,QTextEdit,QComboBox,QFileDialog
from PySide2.QtCore import Qt,QDateTime,Signal,QDir,QSettings,QFile,QTextStream

import http.client
import hashlib
import json
import urllib
import random


class Widget(QWidget):
    def __init__(self):

        QWidget.__init__(self)

        self.__salt = "1466355502"

        self.__httpClient = None

        self.__time = QDateTime()

        self.__currentPath = QDir.currentPath()

        self.__appIDLabel = QLabel("AppID:")
        self.__appIDLineEdit = QLineEdit()
        self.__appIDLineEdit.returnPressed.connect(self.__on_appIDLineEdit_returnPressed)

        self.__keyLabel = QLabel("Key:")
        self.__keyLineEdit = QLineEdit()
        self.__keyLineEdit.returnPressed.connect(self.__on_keyLineEdit_returnPressed)

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
        self.__chooseFileButton.clicked.connect(self.__on_clicked_chooseFileButton)

        self.__translateButton = QPushButton("Translate")
        self.__translateButton.clicked.connect(self.__on_clicked_translateButton)

        self.__clearButton = QPushButton("Clear")
        self.__clearButton.clicked.connect(self.__on_clicked_clearButton)

        self.__historyButton = QPushButton("History")
        self.__historyButton.clicked.connect(self.__on_clicked_historyButton)

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

        iniFile = QFile("info.ini")
        if iniFile.exists():
            self.__infoSettings = QSettings("info.ini", QSettings.IniFormat)

            self.__appIDLineEdit.setText(self.__infoSettings.value("info/appid"))
            self.__keyLineEdit.setText(self.__infoSettings.value("info/key"))

        else:
            if iniFile.open(QFile.ReadWrite):
                self.__infoSettings = QSettings("info.ini", QSettings.IniFormat)

                self.__infoSettings.beginGroup("info")

                self.__infoSettings.setValue("appid","00000000000000000")
                self.__infoSettings.setValue("key","00000000000000000")
                self.__infoSettings.endGroup()

                iniFile.close()

        self.__historyFile = QFile("history.txt")
        if self.__historyFile.open(QFile.ReadWrite or QFile.Append):
            self.__historyFileStream = QTextStream(self.__historyFile)

        else:
            self.__statusLabel = QLabel(self.__GetCurrentTime() + " - History fie create failed!")

    def __del__(self):
        self.__historyFile.close()


    def __GetCurrentTime(self,format = "hh:mm:ss"):
        return self.__time.currentDateTime().toString(format)

    def __on_clicked_chooseFileButton(self):
        pass
        """
        filePath = QFileDialog.getOpenFileName(self,"open",self.__currentPath,"* txt")
        if filePath.strip():
            file = QFile(filePath)
            if file.open(QFile.ReadOnly):
                self.__srcTextEdit.insertPlainText(file.readAll())
            else:
                self.__statusLabel = QLabel(self.__GetCurrentTime() + " - open file failed!")

        else:
            self.__statusLabel = QLabel(self.__GetCurrentTime() + " - Choose file failed!")
            return
        """
        
        
        

    def __on_clicked_translateButton(self):

        srcData = self.__srcTextEdit.toPlainText()
        if srcData.strip():
            self.__translateTextEdit.clear()
            self.__translateTextEdit.document().clear()

            dstData = srcData.replace("\n"," ")

        else:
            self.__statusLabel = QLabel(self.__GetCurrentTime() + " - There is no data!")
            return

        myurl = "/api/trans/vip/translate"

        appid = self.__appIDLineEdit.text()
        key = self.__keyLineEdit.text()
        strFrom = self.__fromComboBox.currentData()
        strTo = self.__toComboBox.currentData()
        mymd5 = self.__GetSign(dstData,appid,key)

        myurl = myurl + "?appid=" + appid + "&q=" + urllib.parse.quote(srcData) + "&from=" + strFrom +"&to=" + strTo + "&salt=" + self.__salt + "&sign=" + mymd5

        httpClient = http.client.HTTPConnection("api.fanyi.baidu.com")
        httpClient.request("GET",myurl)

        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")

        js = json.loads(jsonResponse)
        translate = str(js["trans_result"][0]["dst"])

        self.__translateTextEdit.insertPlainText(translate)
        self.__historyFileStream << translate + "\r\n"

        self.__statusLabel = QLabel(self.__GetCurrentTime() + " - Translate successful!")    

    def __on_clicked_clearButton(self):
        self.__srcTextEdit.clear()
        self.__translateTextEdit.clear()

        self.__statusLabel = QLabel(self.__GetCurrentTime() + " - Clear successful!")   

    def __on_clicked_historyButton(self):
        self.__historyFile.close()
        self.__historyFile.open(QFile.ReadWrite or QFile.Append)

        self.__statusLabel = QLabel(self.__GetCurrentTime() + " - Save file successful!") 

    def __on_appIDLineEdit_returnPressed(self):
        appid = self.__appIDLineEdit.text()
        if not appid.strip():
            self.__statusLabel.setText(self.__GetCurrentTime() + " - There is no appid!")
            return

        self.__infoSettings.beginGroup("info")
        self.__infoSettings.setValue("appid",appid)
        self.__infoSettings.endGroup()
        self.__statusLabel.setText(self.__GetCurrentTime() + " - Enter AppID successful!!")


    def __on_keyLineEdit_returnPressed(self):
        key = self.__keyLineEdit.text()
        if not key.strip():
            self.__statusLabel.setText(self.__GetCurrentTime() + " - There is no key!")
            return

        self.__infoSettings.beginGroup("info")
        self.__infoSettings.setValue("key",key)
        self.__infoSettings.endGroup()
        self.__statusLabel.setText(self.__GetCurrentTime() + " - Enter key successful!!")


    def __GetSign(self,srcData,appid,key):
        sign = appid + srcData + self.__salt+ key
        mymd5 = hashlib.md5(sign.encode()).hexdigest()
        return mymd5


