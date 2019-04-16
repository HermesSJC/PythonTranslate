from PySide2.QtWidgets import QMainWindow,QWidget,QToolBar,QStatusBar,QAction,QGridLayout,QLabel,QLineEdit,QComboBox,QTextEdit,QFileDialog
from PySide2.QtCore import Qt, QDateTime,QDir,QSettings,QFile,QTextStream,QByteArray
from PySide2.QtGui import QIcon

import http.client
import hashlib
import json
import urllib
import random


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # 设置时间
        self.__time = QDateTime()

        # 创建图形界面
        self.__SetupUI()

        self.__ConfigureFileToolBar()

        self.__ConfigureTranslateToolBar()

        self.__ConfigureMainLayout()

        # 设置ComboBox的显示内容
        self.__ConfigureComboBox()

        # 设置保存文件的信息
        self.__currentPath = QDir.currentPath()

        self.__ConfigureSysIniFile()

        self.__ConfigureHistoryFile()

        salt = random.randint(1466000000,1467000000)
        self.__salt = str(salt)

        self.__httpClient = None

        self.__statusBar.showMessage(self.__GetCurrentTime() + " - Please choose a file or enter data!", 2000)

        self.show()


    def __del__(self):
        self.__historyFile.close()


    def __SetupUI(self):
        self.__mainWidget = QWidget()
        self.setCentralWidget(self.__mainWidget)

        self.__fileToolBar = QToolBar("File")
        self.addToolBar(self.__fileToolBar)
        self.__translateToolBar = QToolBar("Translate")
        self.addToolBar(self.__translateToolBar)

        self.__statusBar = QStatusBar()
        self.setStatusBar(self.__statusBar)

        self.setWindowIcon(QIcon("./image/translate.png"))

    def __ConfigureFileToolBar(self):
        self.__openFileAction = QAction(QIcon("./image/open.png"),"Open File")
        self.__fileToolBar.addAction(self.__openFileAction)
        self.__openFileAction.triggered.connect(self.__on_triggered_openFileAction)

        self.__saveFileAction = QAction(QIcon("./image/save.png"),"Save File")
        self.__fileToolBar.addAction(self.__saveFileAction)
        self.__saveFileAction.triggered.connect(self.__on_triggered_saveFileAction)

    def __ConfigureTranslateToolBar(self):
        self.__translateAction = QAction(QIcon("./image/translate.png"),"Translate")
        self.__translateToolBar.addAction(self.__translateAction)
        self.__translateAction.triggered.connect(self.__on_triggered_translateAction)

        self.__clearAction = QAction(QIcon("./image/clear.png"),"Clear")
        self.__translateToolBar.addAction(self.__clearAction)
        self.__clearAction.triggered.connect(self.__on_triggered_clearAction)

    def __ConfigureMainLayout(self):
        self.__appIDLabel = QLabel("AppID:")
        self.__appIDLineEdit = QLineEdit(self)
        self.__appIDLineEdit.returnPressed.connect(self.__on_returnPressed_appIDLineEdit)

        self.__keyLabel = QLabel("Key:")
        self.__keyLineEdit = QLineEdit(self)
        self.__keyLineEdit.returnPressed.connect(self.__on_returnPressed_keyLineEdit)

        self.__fromLabel = QLabel("From:")
        self.__fromComboBox = QComboBox(self)
        self.__toLabel = QLabel("To:")
        self.__toComboBox = QComboBox(self)

        self.__srcLabel = QLabel("Src Text:")
        self.__srcTextEdit = QTextEdit(self)

        self.__translateLabel = QLabel("Translate Text:")
        self.__translateTextEdit = QTextEdit(self)

        self.__mainLayout = QGridLayout()
        self.__mainLayout.addWidget(self.__appIDLabel,0,0)
        self.__mainLayout.addWidget(self.__appIDLineEdit,0,1,1,3)
        self.__mainLayout.addWidget(self.__keyLabel,1,0)
        self.__mainLayout.addWidget(self.__keyLineEdit,1,1,1,3)
        self.__mainLayout.addWidget(self.__fromLabel,2,0)
        self.__mainLayout.addWidget(self.__fromComboBox,2,1)
        self.__mainLayout.addWidget(self.__toLabel,2,2)
        self.__mainLayout.addWidget(self.__toComboBox,2,3)
        self.__mainLayout.addWidget(self.__srcLabel,3,0)
        self.__mainLayout.addWidget(self.__srcTextEdit,3,1,1,3)
        self.__mainLayout.addWidget(self.__translateLabel,4,0)
        self.__mainLayout.addWidget(self.__translateTextEdit,4,1,1,3)

        self.__mainWidget.setLayout(self.__mainLayout)

    def __ConfigureComboBox(self):
        self.__fromComboBox.clear()
        self.__fromComboBox.addItem("English","en")
        self.__fromComboBox.addItem("Chinese","zh")
        self.__fromComboBox.addItem("Auto","auto")
        self.__fromComboBox.setCurrentIndex(2)

        self.__toComboBox.clear()
        self.__toComboBox.addItem("English", "en")
        self.__toComboBox.addItem("Chinese", "zh")
        self.__toComboBox.setCurrentIndex(1)

    def __ConfigureSysIniFile(self):
        iniFile = QFile("info.ini")

        if iniFile.exists():
            self.__infoSettings = QSettings("info.ini", QSettings.IniFormat)

            self.__appIDLineEdit.setText(self.__infoSettings.value("info/appid"))
            self.__keyLineEdit.setText(self.__infoSettings.value("info/key"))

        else:
            if iniFile.open(QFile.ReadWrite):
                self.__infoSettings = QSettings("info.ini", QSettings.IniFormat)

                self.__infoSettings.beginGroup("info")

                self.__infoSettings.setValue("appid", "00000000000000000")
                self.__infoSettings.setValue("key", "00000000000000000")
                self.__infoSettings.endGroup()

                iniFile.close()

                self.__appIDLineEdit.setText("00000000000000000")
                self.__keyLineEdit.setText("00000000000000000")

    def __ConfigureHistoryFile(self):
        self.__historyFile = QFile("history.txt")
        if self.__historyFile.open(QFile.ReadWrite or QFile.Append):
            self.__historyFileStream = QTextStream(self.__historyFile)

        else:
            self.__statusBar.showMessage(self.__GetCurrentTime() + " - History fie create failed!", 2000)

    def __GetCurrentTime(self, format = "hh:mm:ss"):
        return self.__time.currentDateTime().toString(format)

    def __GetSign(self,srcData,appid,key):
        sign = appid + srcData + self.__salt+ key
        mymd5 = hashlib.md5(sign.encode()).hexdigest()
        return mymd5

    def __on_triggered_openFileAction(self):
        filePath = QFileDialog.getOpenFileName(self, "open", self.__currentPath, "* txt")
        if filePath[0].strip():
            file = QFile(filePath[0])
            if file.open(QFile.ReadOnly):

                readData = str(file.readAll())
                fileData = readData[2:readData.__len__() - 1].replace(r"\r\n",r" ")
                self.__srcTextEdit.insertPlainText(fileData)
            else:
                self.__statusBar.showMessage(self.__GetCurrentTime() + " - open file failed!", 2000)
        else:
            self.__statusBar.showMessage(self.__GetCurrentTime() + " - Choose file failed!", 2000)
            return



    def __on_triggered_saveFileAction(self):
        self.__historyFile.close()
        self.__historyFile.open(QFile.ReadWrite or QFile.Append)

        self.__statusBar.showMessage(self.__GetCurrentTime() + " - Save file successful!", 2000)

    def __on_triggered_translateAction(self):
        srcData = self.__srcTextEdit.toPlainText()
        if srcData.strip():
            self.__translateTextEdit.clear()
            self.__translateTextEdit.document().clear()

            dstData = srcData.replace("\n", " ")

        else:
            self.__statusBar.showMessage(self.__GetCurrentTime() + " - There is no data!", 2000)
            return

        myurl = "/api/trans/vip/translate"

        appid = self.__appIDLineEdit.text()
        key = self.__keyLineEdit.text()
        strFrom = self.__fromComboBox.currentData()
        strTo = self.__toComboBox.currentData()
        mymd5 = self.__GetSign(dstData, appid, key)

        myurl = myurl + "?appid=" + appid + "&q=" + urllib.parse.quote(srcData) + "&from=" + strFrom + "&to=" + strTo + "&salt=" + self.__salt + "&sign=" + mymd5

        httpClient = http.client.HTTPConnection("api.fanyi.baidu.com")
        httpClient.request("GET", myurl)

        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")

        js = json.loads(jsonResponse)
        translate = str(js["trans_result"][0]["dst"])

        self.__translateTextEdit.insertPlainText(translate)
        self.__historyFileStream << translate + "\r\n"

        self.__statusBar.showMessage(self.__GetCurrentTime() + " - Translate successful!", 2000)


    def __on_triggered_clearAction(self):
        self.__srcTextEdit.clear()
        self.__translateTextEdit.clear()

        self.__statusBar.showMessage(self.__GetCurrentTime() + " - Clear successful!", 2000)


    def __on_returnPressed_appIDLineEdit(self):
        appid = self.__appIDLineEdit.text()
        if not appid.strip():
            self.__statusBar.showMessage(self.__GetCurrentTime() + " - There is no appid!", 2000)
            return

        self.__infoSettings.beginGroup("info")
        self.__infoSettings.setValue("appid",appid)
        self.__infoSettings.endGroup()
        self.__statusBar.showMessage(self.__GetCurrentTime() + " - Enter appid successful!", 2000)


    def __on_returnPressed_keyLineEdit(self):
        key = self.__keyLineEdit.text()
        if not key.strip():
            self.__statusBar.showMessage(self.__GetCurrentTime() + " - There is no key!", 2000)
            return

        self.__infoSettings.beginGroup("info")
        self.__infoSettings.setValue("key",key)
        self.__infoSettings.endGroup()
        self.__statusBar.showMessage(self.__GetCurrentTime() + " - Enter key successful!", 2000)