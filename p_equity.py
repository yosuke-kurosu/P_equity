import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication, \
                            QVBoxLayout, QPushButton, QTableView, \
                            QLabel, QProgressBar
from widget_board import Widgetboard
from widget_range import Widgetrange
from widget_pandas import PandasModel
from util import rank_of_seven_card, rank_of_five_card, run


class Pequity(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 400)
        self.mainlayout = QVBoxLayout()
        # villianのレンジ, board, hollcardの設定
        self.prelayout = QHBoxLayout()
        self.handrange = Widgetrange()
        self.handrange.setFixedSize(800, 500)
        self.board = Widgetboard()
        self.board.setFixedSize(800, 500)
        self.prelayout.addWidget(self.handrange)
        self.prelayout.addWidget(self.board)
        self.mainlayout.addLayout(self.prelayout)
        # equityを計算して表示する画面の作成
        self.calclayout = QHBoxLayout()
        # calc button layout
        self.calcbuttonlayout = QVBoxLayout()
        self.calcbutton = QPushButton("calc equity")
        self.calcbutton.clicked.connect(self.calcequity)
        self.calcbutton.setFixedSize(800, 250)
        # self.calcbutton.resize(600, 200)
        self.pbar = QProgressBar()
        self.pbar.setFixedSize(800, 30)
        self.calcbuttonlayout.addWidget(self.calcbutton)
        self.calcbuttonlayout.addWidget(self.pbar)
        self.pandasTv = QTableView()
        self.pandasTv.setFixedSize(310, 400)
        self.calcresult = QVBoxLayout()
        self.calcresult_wincombo = QLabel("win combo")
        self.calcresult_losecombo = QLabel("lose combo")
        self.calcresult.addWidget(self.calcresult_wincombo)
        self.calcresult.addWidget(self.calcresult_losecombo)
        # calc layout
        self.calclayout.addLayout(self.calcbuttonlayout)
        self.calclayout.addWidget(self.pandasTv)
        self.calclayout.addLayout(self.calcresult)
        self.mainlayout.addLayout(self.calclayout)
        # メイン画面の設定
        self.setLayout(self.mainlayout)
        self.show()

    def calcequity(self):
        # hollcardとboardからレンジをキャップする。
        cr = self.caprange(self.handrange.hand,
                           herohand=self.board.boardcardlist,
                           board=self.board.hollcardlist)
        # equityの計算ループ
        self.pbar.setMaximum(len(cr))
        result = []
        for i, h in enumerate(cr):
            result.append(run((tuple(self.board.hollcardlist), h),
                          flop=self.board.boardcardlist,))
            # QApplication.processEvents()
            self.pbar.setValue(i+1)
        he = np.round(np.array(result)[:, 0], decimals=2)
        ve = np.round(np.array(result)[:, 1], decimals=2)
        df = pd.DataFrame({
            "hand": cr,
            "hero_equity": he,
            "villain_equity": ve
        })
        model = PandasModel(df)
        self.pandasTv.setModel(model)
        wincombo = sum(he > 0.5)
        losecombo = sum(ve > 0.5)
        self.calcresult_wincombo.setText(f"win combo {wincombo} ({wincombo/len(he)})")
        self.calcresult_losecombo.setText(f"lose combo {losecombo} ({losecombo/len(ve)})")

    def caprange(self, openrange, herohand=None, board=None):
        """
        hollcardとboardと重複するカードをレンジから削除する
        """
        remain = openrange.copy()
        if herohand != None:  # 要改善
            for hand in openrange:
                if len(set(herohand) & set(hand)) != 0:
                    remain.remove(hand)
        if board != None:  # 要改善
            for hand in openrange:
                if len(set(board) & set(hand)) != 0:
                    remain.remove(hand)
        return remain


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ew = Pequity()
    sys.exit(app.exec_())
