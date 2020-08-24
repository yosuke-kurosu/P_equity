import sys
import itertools
from PyQt5.QtCore import QTimer, QStringListModel
from PyQt5.QtWidgets import QWidget, QPushButton, QButtonGroup, QGridLayout,\
                            QLabel, QApplication, QMainWindow, QHBoxLayout, \
                            QVBoxLayout, QListView


class Widgetrange(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        # イベントループ
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self._run)

    def _run(self):
        # ハンドリストの更新
        self.showhand = [str(h) for h in self.hand]  # 一時的にタプル→ストリング
        self.model = QStringListModel(self.showhand, self)
        self.listView.setModel(self.model)
        # ハンド数の更新
        if self.prehand != self.hand:
            self.total_combo.setText(f"total combo: {len(self.hand)}")
            self.num_A = self.check_num("A")
            self.num_K = self.check_num("K")
            self.num_Q = self.check_num("Q")
            self.num_J = self.check_num("J")
            self.num_p = self.check_pair()
            if len(self.hand) > 0:
                self.total_A.setText(f"include A: {self.num_A} ({round(self.num_A*100/len(self.hand), 2)}%)")
                self.total_K.setText(f"include K: {self.num_K} ({round(self.num_K*100/len(self.hand), 2)}%)")
                self.total_Q.setText(f"include Q: {self.num_Q} ({round(self.num_Q*100/len(self.hand), 2)}%)")
                self.total_J.setText(f"include J: {self.num_J} ({round(self.num_J*100/len(self.hand), 2)}%)")
                self.total_P.setText(f"include pair is {self.num_p} ({round(self.num_p*100/len(self.hand), 2)}%)")
            self.prehand = self.hand.copy()
        self.timer.start(1000)

    def initUI(self):
        self.resize(400, 400)  # 横, 縦
        # self.move(300, 300)
        self.setWindowTitle('sample')

        self.hand = []
        self.prehand = []
        self.group = QButtonGroup(self)
        self.mainlayout = QHBoxLayout()
        self.sublayout1 = QVBoxLayout()
        self.sublayout2 = QVBoxLayout()
        # handの一覧
        handsA = ["AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s",
                  "A7s", "A6s", "A5s", "A4s", "A3s", "A2s"]
        handsK = ["AKo", "KK", "KQs", "KJs", "KTs", "K9s", "K8s",
                  "K7s", "K6s", "K5s", "K4s", "K3s", "K2s"]
        handsQ = ["AQo", "KQo", "QQ", "QJs", "QTs", "Q9s", "Q8s",
                  "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s"]
        handsJ = ["AJo", "KJo", "QJo", "JJ", "JTs", "J9s", "J8s",
                  "J7s", "J6s", "J5s", "J4s", "J3s", "J2s"]
        handsT = ["ATo", "KTo", "QTo", "JTo", "TT", "T9s", "T8s",
                  "T7s", "T6s", "T5s", "T4s", "T3s", "T2s"]
        hands9 = ["A9o", "K9o", "Q9o", "J9o", "T9o", "99", "98s",
                  "97s", "96s", "95s", "94s", "93s", "92s"]
        hands8 = ["A8o", "K8o", "Q8o", "J8o", "T8o", "98o", "88",
                  "87s", "86s", "85s", "84s", "83s", "82s"]
        hands7 = ["A7o", "K7o", "Q7o", "J7o", "T7o", "97o", "87o",
                  "77", "76s", "75s", "74s", "73s", "72s"]
        hands6 = ["A6o", "K6o", "Q6o", "J6o", "T6o", "96o", "86o",
                  "76o", "66", "65s", "64s", "63s", "62s"]
        hands5 = ["A5o", "K5o", "Q5o", "J5o", "T5o", "95o", "85o",
                  "75o", "65o", "55", "54s", "53s", "52s"]
        hands4 = ["A4o", "K4o", "Q4o", "J4o", "T4o", "94o", "84o",
                  "74o", "64o", "54o", "44", "43s", "42s"]
        hands3 = ["A3o", "K3o", "Q3o", "J3o", "T3o", "93o", "83o",
                  "73o", "63o", "53o", "43o", "33", "32s"]
        hands2 = ["A2o", "K2o", "Q2o", "J2o", "T2o", "92o", "82o",
                  "72o", "62o", "52o", "42o", "43o", "22"]

        for hands in [handsA, handsK, handsQ, handsJ, handsT, hands9, hands8,
                      hands7, hands6, hands5, hands4, hands3, hands2]:
            layout = self.makelayout(hands)
            self.sublayout1.addLayout(layout)
        self.model = QStringListModel(self.hand, self)
        self.listView = QListView()
        self.listView.setModel(self.model)
        self.total_combo = QLabel(f"total combo is {len(self.hand)}")
        self.total_A = QLabel(f"include A is {len(self.hand)}")
        self.total_K = QLabel(f"include K is {len(self.hand)}")
        self.total_Q = QLabel(f"include Q is {len(self.hand)}")
        self.total_J = QLabel(f"include J is {len(self.hand)}")
        self.total_P = QLabel(f"include pair is {len(self.hand)}")
        self.sublayout2.addWidget(self.listView)
        self.sublayout2.addWidget(self.total_combo)
        self.sublayout2.addWidget(self.total_A)
        self.sublayout2.addWidget(self.total_K)
        self.sublayout2.addWidget(self.total_Q)
        self.sublayout2.addWidget(self.total_J)
        self.sublayout2.addWidget(self.total_P)
        self.mainlayout.addLayout(self.sublayout1)
        self.mainlayout.addLayout(self.sublayout2)
        self.setLayout(self.mainlayout)
        self.show()

    def makelayout(self, hands):
        """
        handsのボタンをselfで作成してボタンを入れたlayoutを返す
        """
        layout = QHBoxLayout()
        for h in hands:
            exec(f"self.button{h} = QPushButton('{h}')")
            exec(f"self.button{h}.setCheckable(True)")
            exec(f"self.button{h}.toggled.connect(self.button_toggled)")
            exec(f"layout.addWidget(self.button{h})")
        return layout

    def button_toggled(self, checked):
        button = self.sender()
        c = button.text()
        if checked:
            if "s" in c:
                self.sender().setStyleSheet("background-color: blue")
            elif "o" in c:
                self.sender().setStyleSheet("background-color: red")
            else:
                self.sender().setStyleSheet("background-color: green")
            self.hand.extend(self.comb2hand(c))
        else:
            self.sender().setStyleSheet("background-color: white")
            for comb in self.comb2hand(c):
                self.hand.remove(comb)

    def comb2hand(self, comb):
        """
        AKo、AKs、AA等の表記の仕方から実際のcombに変換する。
        input:
            str
        return
            list
        """
        marks = ['s', 'd', 'c', 'h']
        if len(comb) == 3:  # ポケットじゃない場合
            if comb[2] == "s":  # 同スートの場合
                return [(f'{comb[0]}{i}', f'{comb[1]}{j}') for i, j in zip(marks, marks)]

            else:  # 別スートの場合
                hands = []
                for i in marks:
                    for j in [s for s in marks if i not in s]:
                        hands.append((f'{comb[0]}{i}', f'{comb[1]}{j}')) 
                return hands
        else:  # ポケットの場合
            return [(f'{comb[0]}{i[0]}', f'{comb[0]}{i[1]}') for i in itertools.combinations(marks, 2)]

    def check_num(self, rank):
        num = 0
        for h in self.hand:
            if rank in h[0] or rank in h[1]:
                num += 1
        return num

    def check_pair(self):
        count = 0
        for h in self.hand:
            if h[0][0] == h[1][0]:
                count += 1
        return count


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ew = Handrange()
    sys.exit(app.exec_())
