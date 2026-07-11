from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
import config

# 창 화면 설정
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)     # 상단 타이틀 바와 테두리를 완전히 제거 (윈도우 크기 버그 차단)
        
        # 화면 크기 설정 및 생성 위치 조정
        screen = QApplication.primaryScreen().availableGeometry()              # 작업 표시줄을 제외한 실제 사용 가능한 화면 영역(크기 및 좌표) 가져오기
        if screen.width() <= 1920:
            window_size = config.NATIVE_SIZE * config.LAPTOP_SCALE
        else:
            window_size = config.NATIVE_SIZE * config.DESKTOP_SCALE

        self.setFixedSize(window_size, window_size)                   # 창 크기 고정
        window_x = screen.x() + (screen.width()-window_size) // 2     # 창 생성 너비
        window_y = screen.y() + screen.height()-window_size           # 창 생성 높이   
        self.move(window_x, window_y) # 시작 좌표 모니터 기준으로 생성

        # 화면 투명도 설정
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)