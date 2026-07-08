from window import MainWindow
from animation_manager import AnimationManager
from pet_state import Condition
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QApplication
import settings_menu
import config
import random
import sys

class PetWidget(MainWindow):
    # 초기 상태 설정 및 애니메이션 매니저 생성
    def __init__(self):
        super().__init__()
        self.animation_manager = AnimationManager(self) # 애니메이션 매니저 생성
        self.current_condition = Condition.START        # 초기 상태 설정
        self.current_pixmap = None                      # 현재 표시할 프레임 저장용
        self._setup_signals()                           # 애니메이션 매니저의 시그널 연결
        self._load_animations()                         # 애니메이션 로드 여부 확인용
        self.set_condition(Condition.START)             # 초기 상태에 맞는 애니메이션 재생
        self._stop_requested = False
        
        # 배회 모션 설정
        self._timer = QTimer(self)                      # 타이머 설정
        self._timer.setSingleShot(True)                 # 타이머 예약
        self._timer.timeout.connect(self._random_move)  # 타이머 종료 시 연결
        self._schedule_next()

        # 배회 시 설정
        self._move_timer = QTimer(self)
        self._move_timer.timeout.connect(self._move_tick)                           

    # 다음 랜덤 타이머 설정
    def _schedule_next(self):
        low, high = config.MOTION_INTERVAL_RANGE_MS
        interval = random.randint(low, high)
        self._timer.start(interval)                     # 타이머 시작
    
    # 배회 모션 종료 시
    def _stop_walking(self):  
        if self.current_condition in (Condition.MOVE_LEFT, Condition.MOVE_RIGHT):
            self._stop_requested = True

    # 애니메이션 매니저와 시그널 연결
    def _setup_signals(self):
        self.animation_manager.frame_changed.connect(self._on_frame_changed) # 프레임 변경 시그널 연결
        self.animation_manager.finished.connect(self._on_animation_finished) # 애니메이션 종료 시그널 연결

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

    # 애니메이션 종료 시 다음 상태로 전환
    def _on_animation_finished(self, name): 
        if name == Condition.START.sheet_key:             # 키가 start이면 IDLE 실행
            self.set_condition(Condition.IDLE)
        elif name == Condition.RELAX_1.sheet_key:         # 키가 relax1이면 loop 실행
            self.set_condition(Condition.RELAX_1_LOOP)
        elif name == Condition.RELAX_1_END.sheet_key:     # 키가 relax1 end이면 IDLE 실행
            self.set_condition(Condition.IDLE)
        elif name == Condition.RELAX_2.sheet_key:         # 키가 relax2이면 loop 실행
            self.set_condition(Condition.RELAX_2_LOOP)
        elif name == Condition.RELAX_2_END.sheet_key:     # 키가 relax1 end이면 IDLE 실행
            self.set_condition(Condition.IDLE)

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
                self.set_condition(Condition.RELAX_1_END)
            elif self.current_condition == Condition.RELAX_2_LOOP:         # 쉬는 모션이 2일 경우
                self.set_condition(Condition.RELAX_2_END)
    
    # 우클릭 시 메뉴 띄우기
    def contextMenuEvent(self, event):
        pass

    # 캐릭터 자동 배회
    def _random_move(self):
        self._schedule_next()
        if self.current_condition != Condition.IDLE:                              # IDLE가 아니면 넘기기 
            return
        
        motion = random.choices(
            [Condition.RELAX_1, Condition.RELAX_2, Condition.MOVE_LEFT, Condition.MOVE_RIGHT], 
            weights=[3, 3, 5, 5]
        )[0]
        self.set_condition(motion) # IDLE일 경우

        # 모션이 좌/우 배회 모션이면 종료 시간 설정
        if motion in (Condition.MOVE_LEFT, Condition.MOVE_RIGHT):
            low, high = config.WALK_DURATION_RANGE_MS
            duration = random.randint(low, high)
            self._move_timer.start(config.MOVE_TICK_MS)
            QTimer.singleShot(duration, self._stop_walking)  # 한 번만 타이머 설정

    # 캐릭터 자동 배회 시
    def _move_tick(self):
        # 좌/우 모션인 경우
        if self.current_condition == Condition.MOVE_LEFT:
            self.move(self.x() - config.MOVE_SPEED, self.y())
        else:
            self.move(self.x() + config.MOVE_SPEED, self.y())

        # 화면 좌/우 이동 계산
        screenSize = QApplication.primaryScreen().availableGeometry().width()
        if self.x() + self.width() < 0:
            self.move(screenSize, self.y())
        elif self.x() > screenSize:
            self.move(-self.width(), self.y())

        # 화면 안에 걷기 종료가 뜰 경우
        if self._stop_requested and (self.x() >=0 and self.x() + self.width() <= screenSize):
            self._move_timer.stop()
            self._stop_requested = False
            self.set_condition(Condition.IDLE)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Windows = PetWidget()
    Windows.show()
    app.exec()


"""
class PetWidget(PetWindow):

  __init__            부모 창 띄우고 살림 차리기
                      (매니저 소유 / 시작 상태 = APPEARING / 프레임 보관칸 비우기)
  ─────────────
  _setup_signals      매니저의 시그널 2개를 내 슬롯에 연결
                      (프레임 바뀜 → 다시 그림 / 끝남 → 다음 상태)
  ─────────────
  _load_animations    config의 SHEETS 뒤져서 매니저에 애니 전부 등록
                      (play가 동작하려면 미리 넣어둬야 함)
  ─────────────
  set_condition       상태 하나 받아서 → config 매핑 조회 → 매니저에 play 시킴
                      (상태 → 모션 연결하는 지휘자)
  ─────────────
  _on_frame_changed   ★새 프레임 받으면 보관 + update() (→ 다시 그리라고 찌르기)
  ─────────────
  _on_animation_finished  안 도는 모션 끝났을 때 다음으로
                          (지금은 APPEARING → IDLE 하나만)
  ─────────────
  paintEvent          보관한 프레임을 실제로 화면에 칠하기
                      (뭉갬 끄기 / 배경 안 칠함 / 비었으면 그냥 넘김)
  ─────────────
  contextMenuEvent    우클릭 → 메뉴 띄우기
                      ("설정" → 독립 창 열기 / "종료" → 끝내기)
"""