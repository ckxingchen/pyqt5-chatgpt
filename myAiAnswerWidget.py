import sys
import openai
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit
from QCandyUi.CandyWindow import colorful
from PyQt5 import QtCore, QtWidgets


class Ui_aiAnswerWidget(object):
    def setupUi(self, aiAnswerWidget):
        aiAnswerWidget.setObjectName("aiAnswerWidget")
        aiAnswerWidget.resize(518, 528)
        self.horizontalLayout = QtWidgets.QHBoxLayout(aiAnswerWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.aiAnswerFrame = QtWidgets.QFrame(aiAnswerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aiAnswerFrame.sizePolicy().hasHeightForWidth())
        self.aiAnswerFrame.setSizePolicy(sizePolicy)
        self.aiAnswerFrame.setMinimumSize(QtCore.QSize(500, 0))
        self.aiAnswerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.aiAnswerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.aiAnswerFrame.setObjectName("aiAnswerFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.aiAnswerFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.setGroupBox = QtWidgets.QGroupBox(self.aiAnswerFrame)
        self.setGroupBox.setObjectName("setGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.setGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.apiKeyLabel = QtWidgets.QLabel(self.setGroupBox)
        self.apiKeyLabel.setObjectName("apiKeyLabel")
        self.gridLayout.addWidget(self.apiKeyLabel, 0, 0, 1, 1)
        self.apiKeyLineEdit = QtWidgets.QLineEdit(self.setGroupBox)
        self.apiKeyLineEdit.setObjectName("apiKeyLineEdit")
        self.gridLayout.addWidget(self.apiKeyLineEdit, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.setGroupBox)
        self.answerGroupBox = QtWidgets.QGroupBox(self.aiAnswerFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.answerGroupBox.sizePolicy().hasHeightForWidth())
        self.answerGroupBox.setSizePolicy(sizePolicy)
        self.answerGroupBox.setMinimumSize(QtCore.QSize(0, 200))
        self.answerGroupBox.setObjectName("answerGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.answerGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.answerTextBrowser = QtWidgets.QTextBrowser(self.answerGroupBox)
        self.answerTextBrowser.setObjectName("answerTextBrowser")
        self.verticalLayout_2.addWidget(self.answerTextBrowser)
        self.verticalLayout_3.addWidget(self.answerGroupBox)
        self.askGroupBox = QtWidgets.QGroupBox(self.aiAnswerFrame)
        self.askGroupBox.setObjectName("askGroupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.askGroupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.askLineEdit = QtWidgets.QLineEdit(self.askGroupBox)
        self.askLineEdit.setObjectName("askLineEdit")
        self.horizontalLayout_2.addWidget(self.askLineEdit)
        self.askPushButton = QtWidgets.QPushButton(self.askGroupBox)
        self.askPushButton.setObjectName("askPushButton")
        self.horizontalLayout_2.addWidget(self.askPushButton)
        self.verticalLayout_3.addWidget(self.askGroupBox)
        self.horizontalLayout.addWidget(self.aiAnswerFrame)

        self.retranslateUi(aiAnswerWidget)
        QtCore.QMetaObject.connectSlotsByName(aiAnswerWidget)

    def retranslateUi(self, aiAnswerWidget):
        _translate = QtCore.QCoreApplication.translate
        aiAnswerWidget.setWindowTitle(_translate("aiAnswerWidget", "AI???????????????"))
        self.setGroupBox.setTitle(_translate("aiAnswerWidget", "??????"))
        self.apiKeyLabel.setText(_translate("aiAnswerWidget", "API_KEY"))
        self.answerGroupBox.setTitle(_translate("aiAnswerWidget", "AI??????"))
        self.askGroupBox.setTitle(_translate("aiAnswerWidget", "????????????"))
        self.askPushButton.setText(_translate("aiAnswerWidget", "??????"))


class AiAnswerThread(QThread):
    """ai??????????????????"""

    replySignal = pyqtSignal(str)

    def __init__(self, widget):
        self.widget = widget
        super(AiAnswerThread, self).__init__()

    def run(self):
        try:
            openai.api_key = self.widget.api_keys
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=self.widget.question,
                temperature=1,
                max_tokens=1024,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer_msg = response["choices"][0]["text"].strip()
            self.replySignal.emit(answer_msg)
        except Exception as e:
            print(e)


@colorful('blueDeep')
class QmyAiAnswerWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)           # ????????????????????????????????????QWidget??????
        self.ui = Ui_aiAnswerWidget()      # ??????UI??????
        self.ui.setupUi(self)              # ??????UI
        self.api_keys = "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"
        self.question = ""                 # ??????
        self.thread = None
        self.customConfigUI()

    def customConfigUI(self):
        """?????????UI"""
        self.ui.apiKeyLineEdit.setText(self.api_keys)
        # self.ui.apiKeyLineEdit.setEchoMode(QLineEdit.Password)
        self.ui.answerTextBrowser.setReadOnly(True)
        self.ui.answerTextBrowser.setFontFamily("Microsoft YaHei")
        self.ui.apiKeyLineEdit.setPlaceholderText('??????????????????API?????????')
        self.ui.askLineEdit.setPlaceholderText('?????????????????????????????????')

    def on_apiKeyLineEdit_editingFinished(self):
        """??????apikey-?????????"""
        try:
            text = self.ui.apiKeyLineEdit.text()
            if text:
                self.api_keys = text
            else:
                QMyMessageBox(self).msgBoxCritical('??????', '?????????API?????????')
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("??????", "???????????????\n??????:{}".format(e))

    def on_askLineEdit_editingFinished(self):
        """????????????-?????????"""
        try:
            text = self.ui.askLineEdit.text()
            if text:
                self.question = text
            else:
                QMyMessageBox(self).msgBoxCritical('??????', '????????????????????????')
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("??????", "???????????????\n??????:{}".format(e))

    def on_askLineEdit_returnPressed(self):
        """????????????-?????????"""
        try:
            text = self.ui.askLineEdit.text()
            if text:
                self.question = text
                self.on_askPushButton_clicked()
            else:
                QMyMessageBox(self).msgBoxCritical('??????', '????????????????????????')
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("??????", "???????????????\n??????:{}".format(e))

    @pyqtSlot(bool)
    def on_askPushButton_clicked(self):
        """????????????-?????????"""
        try:
            self.ui.answerTextBrowser.setText('?????????,?????????...')
            self.thread = AiAnswerThread(self)
            self.thread.replySignal.connect(self.showText)
            self.thread.start()
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("??????", "?????????????????????\n??????:{}".format(e))

    def showText(self, text):
        """??????????????????"""
        self.ui.answerTextBrowser.clear()
        self.ui.answerTextBrowser.setText(text)


class QMyMessageBox(QMessageBox):

    def __init__(self, parent=None):
        super().__init__(parent)

    def msgBoxCritical(self, title, text):
        msgBoxC = QMessageBox(QMessageBox.Critical, title, text, QMessageBox.Ok, self)
        msgBoxC.button(QMessageBox.Ok).setText("??????")
        msgBoxC.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = QmyAiAnswerWidget()
    myWidget.setWindowTitle("AI???????????????")
    myWidget.show()
    sys.exit(app.exec_())
