from PySide6.QtCore import Signal, QTimer, QObject
from PySide6.QtGui import QPixmap
from config import DEFAULT_FRAME_INTERVAL_MS
from dataclasses import dataclass

# 애니메이션 데이터 구조 정의
@dataclass
class Animation:
    frames: list[QPixmap]
    durations: list[int]    # 각 프레임마다 ms
    loop: bool              # 애니메이션이 반복되는지 여부를 나타내는 속성, 기본값은 Truefr

class AnimationManager(QObject):
    frame_changed = Signal(QPixmap)   # 애니메이션 프레임이 변경될 때 발생하는 시그널
    finished = Signal(str)            # 애니메이션이 끝났을 때 발생하는 시그널
    loop_completed = Signal(str)      # loop에서 해당 모션이 끝까지 돌았을 때 발생하는 시그널

    # 초기화
    def __init__(self, parent=None):
        super().__init__(parent)
        self._loaded_animations = {}                   # 로드된 스프라이트 시트 저장소
        self._playing_animation = None                 # 현재 재생 중인 애니메이션
        self._index = 0                                # 현재 프레임 인덱스
        self._current_name = None                      # 현재 재생 중인 애니메이션 이름

        self._timer = QTimer(self)                    # 타이머 설정
        self._timer.timeout.connect(self._on_timeout) # 타이머가 만료될 때 호출되는 메서드 연결

    # 애니메이션을 로드하여 저장소에 추가
    def load_animation(self, name, frames, durations=None, loop=True):
        if durations is None:
            durations = [DEFAULT_FRAME_INTERVAL_MS] * len(frames)
        self._loaded_animations[name] = Animation(frames=frames, durations=durations, loop=loop)

    # 애니메이션 재생
    def play(self, name):
        if name not in self._loaded_animations:
            raise ValueError(f"Animation '{name}' not loaded.") # 조건에 맞지 않으면 오류 메시지 출력
        self._playing_animation = self._loaded_animations[name]
        self._index = 0
        self._current_name = name
        self.frame_changed.emit(self._playing_animation.frames[self._index])
        self._timer.start(self._playing_animation.durations[self._index])
    
    # 애니메이션 종료
    def stop(self):
        self._timer.stop()
        self._playing_animation = None
        self._index = 0
        self._current_name = None

    # 애니메이션 일시정지
    def pause(self):
        self._timer.stop()
    
    # 애니메이션 재개
    def resume(self):
        if self._playing_animation and not self._timer.isActive():
            self._timer.start(self._playing_animation.durations[self._index])

    # 타이머 만료 시 호출되는 메서드
    def _on_timeout(self):
        if not self._playing_animation:                          # 현재 재생 중인 애니메이션 없으면 종료
            return
        
        self._index += 1
        # 인덱스가 프레임 수를 초과한 경우
        if self._index >= len(self._playing_animation.frames):
            if self._playing_animation.loop:                      # 루프 여부 확인
                self._index = 0
                self.loop_completed.emit(self._current_name)
            else:                                                 # 루프가 아니면 애니메이션 종료
                name = self._current_name
                self.stop()
                self.finished.emit(name)
                return
        # 프레임 변경 시그널 발생 및 타이머 재시작
        self.frame_changed.emit(self._playing_animation.frames[self._index])
        self._timer.start(self._playing_animation.durations[self._index])

    # 현재 재생 중인 애니메이션 이름 반환
    @property
    def current_name(self):
        return self._current_name