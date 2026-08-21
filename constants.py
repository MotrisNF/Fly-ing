from typing import Literal

ZoneType = Literal[
    "normal", "blocked", "restricted", "priority", "start", "end"
]

_HUB_METADATA_KEYS = {"zone", "color", "max_drones"}
_CONNECTION_METADATA_KEYS = {"max_link_capacity"}
