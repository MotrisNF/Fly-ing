"""Shared literal types and metadata keys used across the project."""

from typing import Literal

ZoneType = Literal[
    "normal", "blocked", "restricted", "priority", "start", "end"
]
"""Movement-cost category of a hub; ``start``/``end`` mark the gates."""

DroneStatus = Literal[
    "waiting", "in_transit", "delivered"
]
"""Lifecycle state of a drone within a simulation turn."""

_HUB_METADATA_KEYS = {"zone", "color", "max_drones"}
"""Metadata keys accepted inside a ``hub:`` line's ``[...]`` block."""

_CONNECTION_METADATA_KEYS = {"max_link_capacity"}
"""Metadata keys accepted inside a ``connection:`` line's ``[...]`` block."""

TESTING = True

COLORS = {
    "GREEN": (124, 252, 0),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (220, 20, 60),
    "ORANGE": (255, 140, 0),
    "GOLD": (255, 215, 0),
    "CYAN": (0, 200, 200),
    "MAGENTA": (200, 0, 200),
    "GRAY": (128, 128, 128),
    "DARK_BLUE": (0, 0, 100),
}

ZONE_COLORS: dict[ZoneType, tuple[int, int, int]] = {
    "normal": COLORS["WHITE"],
    "blocked": COLORS["RED"],
    "restricted": COLORS["ORANGE"],
    "priority": COLORS["GOLD"],
    "start": COLORS["CYAN"],
    "end": COLORS["MAGENTA"],
}

DESKTOP_OFFSET = 100
MARGIN_X = 60
MARGIN_Y = 200
MAX_GRID = 140
SIDEBAR_RATIO = 1 / 3
TURN_DURATION_FRAMES = 45
TURN_PAUSE_FRAMES = 8
START_DELAY_FRAMES = 60
