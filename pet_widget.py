from window import MainWindow
from animation_manager import AnimationManager
from pet_controller import PetController
from pet_state import Condition
from settings_menu import SettingMenu
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QPainter
import config

class PetWidget(MainWindow):
    # 초기 상태 설정 및 애니메이션 매니저 생성
    def __init__(self):
        super().__init__()
        self.current_condition = Condition.START        # 초기 상태 설정
        self.current_pixmap = None                      # 현재 표시할 프레임 저장용
        self.animation_manager = AnimationManager(self) # 애니메이션 매니저 생성
        self.controller = PetController(self)
        self.menu = SettingMenu(self)
        self._setup_signals()                           # 애니메이션 매니저의 시그널 연결
        self._load_animations()                         # 애니메이션 로드 여부 확인용
        self.set_condition(Condition.START)             # 초기 상태에 맞는 애니메이션 재생            

    # 애니메이션 매니저와 시그널 연결
    def _setup_signals(self):
        self.animation_manager.frame_changed.connect(self._on_frame_changed)              # 프레임 변경 시그널 연결
        self.animation_manager.finished.connect(self.controller._on_animation_finished)   # 애니메이션 종료 시그널 연결
        self.animation_manager.loop_completed.connect(self.controller._on_loop_completed) # loop 끝까지 돌았다는 시그널 연결
        self.menu.system_stop.connect(self.controller._on_exit_requested)                 # 종료 버튼 클릭 시그널 연결 - 연결하는 곳 고민 필요

    # 애니메이션 로드 여부 확인용
    def _load_animations(self):
        for cond in Condition:
            # 애니메이션 시트가 config.SHEETS에 존재하는지 확인
            if cond.sheet_key not in config.SHEETS:
                raise ValueError(f"Animation sheet '{cond.sheet_key}' not found in config.SHEETS.")
            
            spec = config.SHEETS[cond.sheet_key]
            sheet = QPixmap(config.ASSET_DIR / spec["file"])  # 스프라이트 시트 위치
            w = sheet.width() // spec["cols"]                 # 각 프레임의 너비
            h = sheet.height() // spec["rows"]                # 각 프레임의 높이
            frames = [                                        # 각 프레임의 QPixmap 객체 생성
                sheet.copy(x * w, y * h, w, h)
                for y in range(spec["rows"])
                for x in range(spec["cols"])
            ]
            frames = frames[:spec["frames"]]                  # 실제 프레임의 수만큼 잘라내기
            self.animation_manager.load_animation(cond.sheet_key, frames, loop=cond.loops)

    # 상태를 받아서 애니메이션 재생
    def set_condition(self, condition):
        self.current_condition = condition
        self.animation_manager.play(condition.sheet_key) # 해당 상태에 애니메이션 재생

    # 새 프레임 보관 및 화면 갱신
    def _on_frame_changed(self, pixmap):
        self.current_pixmap = pixmap  # 시그널을 통해 받음 다음 프레임 한 장을 새로 갱신
        self.update()                 # 갱신한 것을 업데이트하기 -> paintEvent()

    # 화면에 현재 프레임 그리기
    def paintEvent(self, event):
        # current_pixmap가 비어있을 경우 메서드 넘기기
        if self.current_pixmap is None:
            return 
        
        painter = QPainter(self)                                     # 그리기 설정
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False) # 부드러운 보정 끄기(픽셀 뭉겜 방지)
        painter.drawPixmap(self.rect(), self.current_pixmap)         # 다음 프레임 자동확장하면서 그리기 

    # 좌클릭 시 이벤트(쉬는 시간 끝내기)
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            if self.current_condition == Condition.RELAX_1_LOOP:           # 쉬는 모션이 1일 경우
                self.controller._end_requested = True
            elif self.current_condition == Condition.RELAX_2_LOOP:         # 쉬는 모션이 2일 경우
                self.controller._end_requested = True
    
    # 우클릭 시 메뉴 띄우기
    def contextMenuEvent(self, event):
        pos = event.globalPos()
        menu_h = self.menu.sizeHint().height()
        self.menu.popup(QPoint(pos.x(), pos.y() - menu_h - 50))