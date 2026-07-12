from pet_state import Condition
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
import config
import random

class PetController():
    # 초기 설정
    def __init__(self, pet):
        self.pet = pet
        self._stop_requested = False
        self._end_requested = False

        # 배회 시 설정
        self._move_timer = QTimer(self.pet)
        self._move_timer.timeout.connect(self._move_tick)  

    # 캐릭터 자동 배회 시
    def _move_tick(self):
        # 좌/우 모션인 경우
        if self.pet.current_condition == Condition.MOVE_LEFT:
            self.pet.move(self.pet.x() - config.MOVE_SPEED, self.pet.y())
        else:
            self.pet.move(self.pet.x() + config.MOVE_SPEED, self.pet.y())

        # 화면 좌/우 이동 계산
        screenSize = QApplication.primaryScreen().availableGeometry().width()
        if self.pet.x() + self.pet.width() < 0:
            self.pet.move(screenSize, self.pet.y())
        elif self.pet.x() > screenSize:
            self.pet.move(-self.pet.width(), self.pet.y())

        # 화면 안에 걷기 종료가 뜰 경우
        if self._stop_requested and (self.pet.x() >=0 and self.pet.x() + self.pet.width() <= screenSize):
            self._move_timer.stop()
            self._stop_requested = False
            self.pet.set_condition(Condition.IDLE)

    # 배회 모션 종료 시
    def _stop_walking(self):  
        if self.pet.current_condition in (Condition.MOVE_LEFT, Condition.MOVE_RIGHT):
            self._stop_requested = True

    # 캐릭터 자동 배회
    def _choose_next(self):
        motion = random.choices(       # -s - 가중치(옵션) 때문에
            [Condition.IDLE, Condition.MOVE_LEFT, Condition.MOVE_RIGHT, Condition.RELAX_1, Condition.RELAX_2], 
            weights=[17, 13, 13, 0.5, 0.5]
        )[0]                           # [0] - 랜덤으로 뽑는데 리스트 안의 값을 가져오기 위해서  
        self.pet.set_condition(motion) # IDLD의 다음 모션 보내기

        # 모션이 좌/우 배회 모션이면 종료 시간 설정
        if motion in (Condition.MOVE_LEFT, Condition.MOVE_RIGHT):
            low, high = config.WALK_DURATION_RANGE_MS
            duration = random.randint(low, high)
            self._move_timer.start(config.MOVE_TICK_MS)
            QTimer.singleShot(duration, self._stop_walking)  # 한 번만 타이머 설정

    # 애니메이션 종료 시 다음 상태로 전환
    def _on_animation_finished(self, name): 
        if name == Condition.START.sheet_key:             # 키가 start이면 IDLE 실행
            self.pet.set_condition(Condition.IDLE)
        elif name == Condition.RELAX_1.sheet_key:         # 키가 relax1이면 loop 실행
            self.pet.set_condition(Condition.RELAX_1_LOOP)
        elif name == Condition.RELAX_1_END.sheet_key:     # 키가 relax1 end이면 IDLE 실행
            self.pet.set_condition(Condition.IDLE)
        elif name == Condition.RELAX_2.sheet_key:         # 키가 relax2이면 loop 실행
            self.pet.set_condition(Condition.RELAX_2_LOOP)
        elif name == Condition.RELAX_2_END.sheet_key:     # 키가 relax1 end이면 IDLE 실행
            self.pet.set_condition(Condition.IDLE)
        elif name == Condition.IDLE.sheet_key:            # 키가 IDLE이면 다음 동작 선택
            self._choose_next()

    # loop 한 바퀴 완료 시 → 종료 예약돼 있으면 그때 end로 전환
    def _on_loop_completed(self, name):
        if self._end_requested and name == Condition.RELAX_1_LOOP.sheet_key:
            self.pet.set_condition(Condition.RELAX_1_END)
        elif self._end_requested and name == Condition.RELAX_2_LOOP.sheet_key:
            self.pet.set_condition(Condition.RELAX_2_END)
        
        self._end_requested = False