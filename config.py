from pathlib import Path

# 경로
BASE_DIR = Path(__file__).resolve().parent # png가 저장된 프로젝트 폴더 위치 찾기
ASSET_DIR = BASE_DIR / "assets"            # png가 저장된 하위 폴더 지정

# 스프라이트 시트 명세
SHEETS = {
    "start": {"file": "Start.png", "cols": 9, "rows": 6, "frames": 49},
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
SCALE = 4                              # 화면 확대 배율
DISPLAY_SIZE = NATIVE_SIZE * SCALE     # 256. SCALE만 바꾸면 창까지 연동

# 캐릭터 생성 창 크기
WINDOW_WIDTH = DISPLAY_SIZE
WINDOW_HEIGHT = DISPLAY_SIZE

# 애니메이션
DEFAULT_FRAME_INTERVAL_MS = 100         # PNG 실험용 고정 간격
MOTION_INTERVAL_RANGE_MS = (3000, 7000) # 모션 결정 대기 
WALK_DURATION_RANGE_MS = (2000, 5000)   # 걷기 지속 시간 (새로)

# 이동 / 위치
MOVE_SPEED = 2                         # tick당 이동 px
MOVE_TICK_MS = 16                      # 틱 시간
TASKBAR_MARGIN = 0                     # 작업표시줄 위 여백 px