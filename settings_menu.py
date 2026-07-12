from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class SettingMenu(QMenu):
    system_stop = Signal()         # 종료 버튼 눌렀을 때 신호 넘기기
    system_food = Signal()
    system_toy = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.action1 = QAction("food", self)
        self.action2 = QAction("toy", self)
        self.action3 = QAction("exit", self)
        self.action1.triggered.connect(self.system_food.emit)
        self.action2.triggered.connect(self.system_toy.emit)
        self.action3.triggered.connect(self.system_stop.emit)
        self.addAction(self.action1)
        self.addAction(self.action2)
        self.addAction(self.action3)
        self.setStyleSheet("""
            QMenu::item {
                font-size: 15px;
                padding: 10px 70px;
                color: black;
            }
            QMenu {
                background-color: white;
            }
            QMenu::item:selected {
                background-color: #D9D9D9;
            }
        """)