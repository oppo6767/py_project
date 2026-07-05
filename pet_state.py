from enum import Enum

# 해당 애니메이션 동작이 반복되는지 여부를 나타내는 Enum 클래스
class Condition(Enum):
    START = ("start", False)
    IDLE = ("idle", True)
    MOVE_LEFT = ("left", True)
    MOVE_RIGHT = ("right", True)
    RELAX_1 = ("relax_1", False)
    RELAX_1_LOOP = ("relax_1_loop", True)
    RELAX_1_END = ("relax_1_end", False)
    RELAX_2 = ("relax_2", False)
    RELAX_2_LOOP = ("relax_2_loop", True)
    RELAX_2_END = ("relax_2_end", False)
    STOP = ("stop", False)

    # 애니메이션 시트 키와 반복 여부를 초기화하는 생성자
    def __init__(self, sheet_key: str, loops: bool):
        self.sheet_key = sheet_key
        self.loops = loops