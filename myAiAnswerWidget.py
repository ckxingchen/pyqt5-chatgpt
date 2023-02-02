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
        aiAnswerWidget.setWindowTitle(_translate("aiAnswerWidget", "AI问答机器人"))
        self.setGroupBox.setTitle(_translate("aiAnswerWidget", "设置"))
        self.apiKeyLabel.setText(_translate("aiAnswerWidget", "API_KEY"))
        self.answerGroupBox.setTitle(_translate("aiAnswerWidget", "AI回答"))
        self.askGroupBox.setTitle(_translate("aiAnswerWidget", "人工提问"))
        self.askPushButton.setText(_translate("aiAnswerWidget", "提交"))


class AiAnswerThread(QThread):
    """ai智能问答线程"""

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
        super().__init__(parent)           # 调用父类的构造函数，创建QWidget窗体
        self.ui = Ui_aiAnswerWidget()      # 创建UI对象
        self.ui.setupUi(self)              # 构造UI
        self.api_keys = "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"
        self.question = ""                 # 问题
        self.thread = None
        self.customConfigUI()

    def customConfigUI(self):
        """自定义UI"""
        self.ui.apiKeyLineEdit.setText(self.api_keys)
        # self.ui.apiKeyLineEdit.setEchoMode(QLineEdit.Password)
        self.ui.answerTextBrowser.setReadOnly(True)
        self.ui.answerTextBrowser.setFontFamily("Microsoft YaHei")
        self.ui.apiKeyLineEdit.setPlaceholderText('请在此处输入API密钥！')
        self.ui.askLineEdit.setPlaceholderText('请在此处输入你的问题！')

    def on_apiKeyLineEdit_editingFinished(self):
        """输入apikey-槽函数"""
        try:
            text = self.ui.apiKeyLineEdit.text()
            if text:
                self.api_keys = text
            else:
                QMyMessageBox(self).msgBoxCritical('编辑', '请输入API密钥！')
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("编辑", "编辑出错！\n错误:{}".format(e))

    def on_askLineEdit_editingFinished(self):
        """输入问题-槽函数"""
        try:
            text = self.ui.askLineEdit.text()
            if text:
                self.question = text
            else:
                QMyMessageBox(self).msgBoxCritical('编辑', '请输入你的问题！')
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("编辑", "编辑出错！\n错误:{}".format(e))

    def on_askLineEdit_returnPressed(self):
        """输入问题-槽函数"""
        try:
            text = self.ui.askLineEdit.text()
            if text:
                self.question = text
                self.on_askPushButton_clicked()
            else:
                QMyMessageBox(self).msgBoxCritical('编辑', '请输入你的问题！')
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("编辑", "编辑出错！\n错误:{}".format(e))

    @pyqtSlot(bool)
    def on_askPushButton_clicked(self):
        """提交问题-槽函数"""
        try:
            self.ui.answerTextBrowser.setText('思考中,请稍后...')
            self.thread = AiAnswerThread(self)
            self.thread.replySignal.connect(self.showText)
            self.thread.start()
        except Exception as e:
            QMyMessageBox(self).msgBoxCritical("提交", "提交问题出错！\n错误:{}".format(e))

    def showText(self, text):
        """显示回复文本"""
        self.ui.answerTextBrowser.clear()
        self.ui.answerTextBrowser.setText(text)


class QMyMessageBox(QMessageBox):

    def __init__(self, parent=None):
        super().__init__(parent)

    def msgBoxCritical(self, title, text):
        msgBoxC = QMessageBox(QMessageBox.Critical, title, text, QMessageBox.Ok, self)
        msgBoxC.button(QMessageBox.Ok).setText("确定")
        msgBoxC.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = QmyAiAnswerWidget()
    myWidget.setWindowTitle("AI问答机器人")
    myWidget.show()
    sys.exit(app.exec_())
