import sys
import itertools
from PyQt5.QtCore import QTimer, QStringListModel, QSize, QRect, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QButtonGroup, QGridLayout,\
                            QLabel, QApplication, QMainWindow, QHBoxLayout, \
                            QVBoxLayout


class Widgetboard(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        # イベントループ

    def initUI(self):
        self.resize(400, 400)  # 横, 縦
        # self.move(300, 300)  
        self.setWindowTitle('sample')
        self.mainlayout = QHBoxLayout()
        self.mode = "board"
        # 画面左側のレイアウト
        self.rightlayout = QVBoxLayout()
        self.setallcard()
        # 画面右側のレイアウト
        self.leftlayout = QVBoxLayout()
        # ボードに関するレイアウト
        self.boardlayout = QHBoxLayout()
        self.boardtoplayout = QHBoxLayout()
        self.boardtitle = QLabel("board")
        self.boardsetbutton = QPushButton("setboard")
        self.boardsetbutton.clicked.connect(self.setmode)
        self.boardclearbutton = QPushButton("clearboard")
        self.boardclearbutton.clicked.connect(self.clearmethod)
        self.boardtoplayout.addWidget(self.boardtitle)
        self.boardtoplayout.addWidget(self.boardsetbutton)
        self.boardtoplayout.addWidget(self.boardclearbutton)
        # ホールカードの関するレイアウト
        self.holllayout = QHBoxLayout()
        self.holltoplayout = QHBoxLayout()
        self.holltitle = QLabel("hollcard")
        self.hollsetbutton = QPushButton("sethollcard")
        self.hollsetbutton.clicked.connect(self.setmode)
        self.hollclearbutton = QPushButton("clearhollcard")
        self.hollclearbutton.clicked.connect(self.clearmethod)
        self.holltoplayout.addWidget(self.holltitle)
        self.holltoplayout.addWidget(self.hollsetbutton)
        self.holltoplayout.addWidget(self.hollclearbutton)
        # 全体レイアウト
        self.leftlayout.addLayout(self.boardtoplayout)
        self.leftlayout.addLayout(self.boardlayout)
        self.leftlayout.addLayout(self.holltoplayout)
        self.leftlayout.addLayout(self.holllayout)
        self.boardcardlist = []
        self.hollcardlist = []
        # メインのレイアウトを作る
        self.mainlayout.addLayout(self.rightlayout)
        self.mainlayout.addLayout(self.leftlayout)
        self.setLayout(self.mainlayout)
        self.show()

    def setallcard(self):
        rank = ["2", "3", "4", "5", "6", "7", "8",
                "9", "T", "J", "Q", "K", "A"]
        suit = ["s", "h", "d", "c"]
        for r in rank:
            layout = QHBoxLayout()
            for s in suit:
                exec(f"self.button{r}{s} = QPushButton('{r}{s}')")
                exec(f"self.button{r}{s}.setIcon(QIcon('./PNG/{r}{s}.png'))")
                exec(f"self.button{r}{s}.setIconSize(QSize(40, 40))")
                exec(f"self.button{r}{s}.clicked.connect(self.button_clicked)")
                exec(f"layout.addWidget(self.button{r}{s})")
            self.rightlayout.addLayout(layout)

    def button_clicked(self):
        sender = self.sender()
        text = sender.text()
        if self.mode == "board":
            if len(self.boardcardlist) < 5:
                self.boardcardlist.append(text)
                self.addcard(text)
        elif self.mode == "hollcard":
            if len(self.hollcardlist) < 2:
                self.hollcardlist.append(text)
                self.addcard(text)
        # print(f"board: {self.boardcardlist}")
        # print(f"hollcard: {self.hollcardlist}")

    def setmode(self):
        sender = self.sender()
        text = sender.text()
        if text == "setboard":
            self.mode = "board"
        elif text == "sethollcard":
            self.mode = "hollcard"

    def addcard(self, text):
        pixmap = QPixmap(f'./PNG/{text}.png').scaled(QSize(150, 150),
                                                    Qt.KeepAspectRatio,
                                                    Qt.FastTransformation)
        imagelabel = QLabel()
        imagelabel.setPixmap(pixmap)
        if self.mode == "board":
            self.boardlayout.addWidget(imagelabel)
        elif self.mode == "hollcard":
            self.holllayout.addWidget(imagelabel)

    def clearmethod(self):
        sender = self.sender()
        text = sender.text()
        if text == "clearboard":
            self.boardcardlist = []
            for i in reversed(range(self.boardlayout.count())):
                self.boardlayout.itemAt(i).widget().setParent(None)
        elif text == "clearhollcard":
            self.hollcardlist = []
            for i in reversed(range(self.holllayout.count())):
                self.holllayout.itemAt(i).widget().setParent(None)
        else:
            pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ew = Makeboard()
    sys.exit(app.exec_())
