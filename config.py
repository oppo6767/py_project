from pathlib import Path
import sys

# 경로  만약 exe로 실행할 경우 sys._MEIPASS를 아닐 경우 Path(__file__).resolve().parent
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = Path(sys._MEIPASS)
else:   
    BASE_DIR = Path(__file__).resolve().parent  # png가 저장된 프로젝트 폴더 위치 찾기
ASSET_DIR = BASE_DIR / "assets"                 # png가 저장된 하위 폴더 지정

# 스프라이트 시트 명세
SHEETS = {
    "start": {"file": "Start.png", "cols": 10, "rows": 6, "frames": 49},
    "stop": {"file": "stop.png", "cols": 6, "rows": 3, "frames": 16},
    "right": {"file": "right.png", "cols": 8, "rows": 1, "frames": 8},
    "left": {"file": "left.png", "cols": 8, "rows": 1, "frames": 8},
    "idle": {"file": "idle.png", "cols": 10, "rows": 1, "frames": 10},
    "relax_1": {"file": "relax_1.png", "cols": 8, "rows": 4, "frames": 30},
    "relax_1_loop": {"file": "relax_1_loop.png", "cols": 4, "rows": 4, "frames": 15},
    "relax_1_end": {"file": "relax_1_end.png", "cols": 6, "rows": 4, "frames": 24},
    "relax_2": {"file": "relax_2.png", "cols": 5, "rows": 4, "frames": 19},
    "relax_2_loop": {"file": "relax_2_loop.png", "cols": 8, "rows": 1, "frames": 8},
    "relax_2_end": {"file": "relax_2_end.png", "cols": 6, "rows": 4, "frames": 21}
}

# 픽셀아트 / 스케일
NATIVE_SIZE = 64                       # Aseprite 원본 (64×64)
LAPTOP_SCALE = 2                       # 노트북 화면 확대 배율
DESKTOP_SCALE = 4                      # 데스크탑 화면 확대 배율

# 애니메이션
DEFAULT_FRAME_INTERVAL_MS = 100         # PNG 실험용 고정 간격
MOTION_INTERVAL_RANGE_MS = (4000, 9000) # 모션 결정 대기 
WALK_DURATION_RANGE_MS = (2000, 5000)   # 걷기 지속 시간 (새로)

# 이동 / 위치
MOVE_SPEED = 2                         # tick당 이동 px
MOVE_TICK_MS = 16                      # 틱 시간
TASKBAR_MARGIN = 0                     # 작업표시줄 위 여백 px