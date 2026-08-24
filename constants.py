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
FRAME_RATE = 30.0

# How big the node/drone sprites are drawn, as a fraction of the grid
# cell size.
NODE_SPRITE_SCALE = 0.7
DRONE_SPRITE_SCALE = 0.55

# The moon's diameter is the shorter map dimension divided by this.
MOON_SIZE_DIVISOR = 4

# Connection lines: a thicker black line first, then a thinner white
# line on top, giving the outlined look.
CONNECTION_LINE_WIDTH = 6
CONNECTION_LINE_INNER_WIDTH = 2

# Shared outline thickness for every white-circle badge (connection
# capacity, node capacity, drone count).
BADGE_BORDER_WIDTH = 2

# Connection/node capacity badges: radius and font size are
# grid-proportional, floored so they stay legible, and capped so they
# never outgrow the node they sit on.
CAPACITY_BADGE_RADIUS_FLOOR = 6
CAPACITY_BADGE_FONT_FLOOR = 9
CAPACITY_BADGE_GRID_DIVISOR = 8
CAPACITY_BADGE_SIZE_CAP_DIVISOR = 3
CAPACITY_BADGE_RADIUS_SIZE_CAP_MIN = 2
CAPACITY_BADGE_FONT_SIZE_CAP_MIN = 6

# Same idea for the drone count badge, sized off the (smaller) drone
# sprite instead of the node sprite.
DRONE_BADGE_RADIUS_FLOOR = 6
DRONE_BADGE_FONT_FLOOR = 9
DRONE_BADGE_GRID_DIVISOR = 10
DRONE_BADGE_SIZE_CAP_DIVISOR = 3
DRONE_BADGE_RADIUS_SIZE_CAP_MIN = 2
DRONE_BADGE_FONT_SIZE_CAP_MIN = 6

# Turn counter label, top-left of the sidebar.
TURN_LABEL_FONT_FLOOR = 24
TURN_LABEL_SIDEBAR_DIVISOR = 12
TURN_LABEL_MARGIN = 20

# Real per-turn cost (in turns) of moving into a normal/priority vs.
# a restricted hub; see VII.3 in the subject.
NORMAL_ZONE_TURN_COST = 1
RESTRICTED_ZONE_TURN_COST = 2

# Route planning (Router, in routing.py).
MAX_CANDIDATE_PATHS = 8
PATH_COST_CEILING_RATIO = 3.0
PRIORITY_BIAS = 1e-3
COMPLEXITY_THRESHOLD = 20.0
REFINE_TRIAL_BUDGET = 400
