import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt

# 창 화면 설정
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)     # 상단 타이틀 바와 테두리를 완전히 제거 (윈도우 크기 버그 차단)
        
        # 화면 크기 설정 및 생성 위치 조정
        screen = QApplication.primaryScreen().availableGeometry()  # 작업 표시줄을 제외한 실제 사용 가능한 화면 영역(크기 및 좌표) 가져오기
        self.setFixedSize(screen.width(), screen.height())         # 창 크기 고정
        self.move(screen.x(), screen.y())                          # 시작 좌표 모니터 기준으로 생성

        # 화면 투명도 설정
        self.setWindowOpacity(0.3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Windows = MainWindow()
    Windows.show()
    app.exec()