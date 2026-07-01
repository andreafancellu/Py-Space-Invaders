import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 800
FPS = 60

PLAYER_SPEED = 320
BULLET_SPEED = 520
ALIEN_HORIZONTAL_SPEED = 45
ALIEN_VERTICAL_SPEED = 16
ALIEN_EDGE_PADDING = 20
COLLISION_COOLDOWN_MS = 750

SHUTTLE_HP = 100
SHUTTLE_DAMAGE = 10
BOSS_DAMAGE = 15
BOSS_HIT_DAMAGE = 25

INITIAL_SHUTTLE_POSITION = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100]
INITIAL_BOSS_POSITION = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 600]

LEVELS = [
    {
        "number": 1,
        "name": "Neon Hatchlings",
        "alien_tint": (120, 255, 120),
        "alien_speed_multiplier": 1.0,
        "boss_name": "Alienoooo",
        "boss_texture": "boss.png",
        "boss_hp": 100,
        "boss_speed": 85,
    },
    {
        "number": 2,
        "name": "Solar Marauders",
        "alien_tint": (255, 150, 75),
        "alien_speed_multiplier": 1.35,
        "boss_name": "Captain Flarefang",
        "boss_texture": "boss_level2.png",
        "boss_hp": 140,
        "boss_speed": 125,
    },
    {
        "number": 3,
        "name": "Void Carnival",
        "alien_tint": (210, 95, 255),
        "alien_speed_multiplier": 1.75,
        "boss_name": "Baron Nebula",
        "boss_texture": "boss_level3.png",
        "boss_hp": 190,
        "boss_speed": 165,
    },
]


def asset_path(filename):
    return os.path.join(DATA_DIR, filename)
