from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import config

# 창 화면 설정
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)     # 상단 타이틀 바와 테두리를 완전히 제거 (윈도우 크기 버그 차단)
        
        # 화면 크기 설정 및 생성 위치 조정
        screen = QApplication.primaryScreen().availableGeometry()              # 작업 표시줄을 제외한 실제 사용 가능한 화면 영역(크기 및 좌표) 가져오기
        self.setFixedSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)           # 창 크기 고정
        windpw_x = screen.x() + (screen.width()-config.WINDOW_WIDTH) // 2      # 창 생성 너비
        windpw_y = screen.y() + screen.height()-config.WINDOW_HEIGHT + 23      # 창 생성 높이 (23은 애니메이션 높이를 고려함)    
        self.move(windpw_x, windpw_y) # 시작 좌표 모니터 기준으로 생성

        # 화면 투명도 설정
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)