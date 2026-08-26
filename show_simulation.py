from initiate_simulation import Initiator
from exceptions import PathError
from constants import (
    COLORS, ZONE_COLORS, DESKTOP_OFFSET, MARGIN_X, MARGIN_Y, MAX_GRID,
    SIDEBAR_RATIO, TURN_DURATION_FRAMES, TURN_PAUSE_FRAMES,
    START_DELAY_FRAMES, FRAME_RATE, NODE_SPRITE_SCALE, DRONE_SPRITE_SCALE,
    MOON_SIZE_DIVISOR, CONNECTION_LINE_WIDTH, CONNECTION_LINE_INNER_WIDTH,
    BADGE_BORDER_WIDTH, CAPACITY_BADGE_RADIUS_FLOOR, CAPACITY_BADGE_FONT_FLOOR,
    CAPACITY_BADGE_GRID_DIVISOR, CAPACITY_BADGE_SIZE_CAP_DIVISOR,
    CAPACITY_BADGE_RADIUS_SIZE_CAP_MIN, CAPACITY_BADGE_FONT_SIZE_CAP_MIN,
    DRONE_BADGE_RADIUS_FLOOR, DRONE_BADGE_FONT_FLOOR, DRONE_BADGE_GRID_DIVISOR,
    DRONE_BADGE_SIZE_CAP_DIVISOR, DRONE_BADGE_RADIUS_SIZE_CAP_MIN,
    DRONE_BADGE_FONT_SIZE_CAP_MIN, TURN_LABEL_FONT_FLOOR,
    TURN_LABEL_SIDEBAR_DIVISOR, TURN_LABEL_MARGIN_TOP,
    TURN_LABEL_MARGIN_SIDE
)

from collections import deque

import math
import pygame


class Pyshow():
    """Renders the map and animates the simulated drone fleet."""

    def __init__(self, initiator: Initiator) -> None:
        """Store the finished simulation to render.

        Args:
            initiator: A simulation that has already been run.

        Raises:
            PathError: If the config isn't loaded.
        """
        if initiator.config is None:
            raise PathError("The config is not loaded.")
        self._initiator = initiator
        self._c = initiator.config
        self._dimentions: tuple[int, int] = (0, 0)
        self._running: bool = True
        self._clock = pygame.time.Clock()
        self._ticks: float = FRAME_RATE
        self._grid: int = 0
        self._spacing_x: float = 0.0
        self._spacing_y: float = 0.0
        self._offset_x: int = 0
        self._offset_y: int = 0
        self._centers: dict[str, tuple[int, int]] = {}
        self._frame_count: int = 0

    def _to_screen(self, x: int, y: int) -> tuple[int, int]:
        """Convert a hub's map coordinates to a screen pixel position."""
        col = x - self._c.min_x
        row = y - self._c.min_y
        return (
            self._offset_x + int(col * self._spacing_x),
            self._offset_y + int(row * self._spacing_y),
        )

    def _interpolate(
        self, waypoints: list[tuple[int, int, int]]
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        """Find a drone's current screen position and facing direction.

        Locates which pair of waypoints brackets the current frame
        and linearly interpolates between them, so a move animates
        smoothly across the turns it takes to complete.

        Args:
            waypoints: A drone's ``(turn, x, y)`` rest positions, in
                order.

        Returns:
            The interpolated screen position, and the direction of
            travel for that segment.
        """
        for i in range(len(waypoints) - 1):
            turn0, x0, y0 = waypoints[i]
            turn1, x1, y1 = waypoints[i + 1]
            turns_spanned = turn1 - turn0
            frame0 = (turn0 + 1) * TURN_DURATION_FRAMES
            frame1 = (turn1 + 1) * TURN_DURATION_FRAMES
            move_frames = turns_spanned * (
                TURN_DURATION_FRAMES - TURN_PAUSE_FRAMES
            )
            if self._frame_count <= frame1 or i == len(waypoints) - 2:
                t = (self._frame_count - frame0) / move_frames
                t = max(0.0, min(1.0, t))
                position = (
                    int(x0 + (x1 - x0) * t),
                    int(y0 + (y1 - y0) * t),
                )
                direction = (x1 - x0, y1 - y0)
                if direction == (0, 0):
                    direction = self._last_direction(waypoints, i)
                return position, direction
        last = (waypoints[-1][1], waypoints[-1][2])
        return last, (0, -1)

    def _last_direction(
        self, waypoints: list[tuple[int, int, int]], i: int
    ) -> tuple[int, int]:
        """Find the last real movement direction up to waypoint ``i``.

        Used while a drone is stationary (arrived or waiting) so its
        sprite keeps facing the way it was last moving, instead of
        resetting to a default orientation.
        """
        for k in range(i, -1, -1):
            x0, y0 = waypoints[k][1], waypoints[k][2]
            x1, y1 = waypoints[k + 1][1], waypoints[k + 1][2]
            if (x1 - x0, y1 - y0) != (0, 0):
                return (x1 - x0, y1 - y0)
        return (0, -1)

    def _distances_from_entry(self) -> dict[str, int]:
        """Hop-distance from the entry hub to every other hub.

        Used to tell, for a given connection, which endpoint is
        "downstream" -- the one a drone would be advancing towards
        when moving away from the entry -- so its zone (not the
        upstream one) decides the connection badge's color.
        """
        adjacency: dict[str, list[str]] = {name: [] for name in self._c.hubs}
        for connection in self._c.connections:
            adjacency[connection.pos1].append(connection.pos2)
            adjacency[connection.pos2].append(connection.pos1)

        start_name = self._c.gates.entry.name
        distances = {start_name: 0}
        queue = deque([start_name])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        return distances

    def start(self) -> None:
        """Open the window, draw the static map, and animate the fleet."""
        pygame.init()

        desktop = pygame.display.Info()
        self._dimentions = (
            desktop.current_w - DESKTOP_OFFSET,
            desktop.current_h - DESKTOP_OFFSET
            )

        screen = pygame.display.set_mode(self._dimentions)
        back_ground = pygame.Surface(self._dimentions)
        back_ground.fill(COLORS["DARK_BLUE"])

        sidebar_width = int(self._dimentions[0] * SIDEBAR_RATIO)
        map_width = self._dimentions[0] - sidebar_width
        map_height = self._dimentions[1]

        star_tile = pygame.image.load("assets/star_tile.png").convert()
        tile_w, tile_h = star_tile.get_size()
        for tile_x in range(0, map_width, tile_w):
            for tile_y in range(0, map_height, tile_h):
                back_ground.blit(star_tile, (tile_x, tile_y))

        moon_sprite = pygame.image.load("assets/moon.png").convert_alpha()
        moon_size = min(map_width, map_height) // MOON_SIZE_DIVISOR
        moon_scaled = pygame.transform.scale(
            moon_sprite, (moon_size, moon_size)
        )
        moon_rect = moon_scaled.get_rect(
            center=(map_width // 2, map_height // 2)
        )
        back_ground.blit(moon_scaled, moon_rect)

        sidebar_rect = pygame.Rect(map_width, 0, sidebar_width, map_height)
        pygame.draw.rect(back_ground, COLORS["BLACK"], sidebar_rect)
        pygame.draw.rect(back_ground, COLORS["BROWN"], sidebar_rect, width=24)

        usable_width = map_width - MARGIN_X * 2
        usable_height = map_height - MARGIN_Y * 2

        cols = self._c.width + 1
        rows = self._c.height + 1

        grid_candidates: list[float] = [MAX_GRID]
        if cols > 1:
            self._spacing_x = usable_width / (cols - 1)
            self._offset_x = MARGIN_X
            grid_candidates.append(self._spacing_x)
        else:
            self._spacing_x = 0.0
            self._offset_x = MARGIN_X + usable_width // 2

        if rows > 1:
            self._spacing_y = usable_height / (rows - 1)
            self._offset_y = MARGIN_Y
            grid_candidates.append(self._spacing_y)
        else:
            self._spacing_y = 0.0
            self._offset_y = MARGIN_Y + usable_height // 2

        self._grid = int(min(grid_candidates))

        node_sprite = pygame.image.load("assets/node.png").convert_alpha()
        size = int(self._grid * NODE_SPRITE_SCALE)
        scaled_node_sprite = pygame.transform.scale(node_sprite, (size, size))

        for name, hub in self._c.hubs.items():
            self._centers[name] = self._to_screen(hub.x, hub.y)

        capacity_radius = min(
            max(
                CAPACITY_BADGE_RADIUS_FLOOR,
                self._grid // CAPACITY_BADGE_GRID_DIVISOR
            ),
            max(
                CAPACITY_BADGE_RADIUS_SIZE_CAP_MIN,
                size // CAPACITY_BADGE_SIZE_CAP_DIVISOR
            )
        )
        capacity_font_px = min(
            max(
                CAPACITY_BADGE_FONT_FLOOR,
                self._grid // CAPACITY_BADGE_GRID_DIVISOR
            ),
            max(
                CAPACITY_BADGE_FONT_SIZE_CAP_MIN,
                size // CAPACITY_BADGE_SIZE_CAP_DIVISOR
            )
        )
        capacity_font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf",
            capacity_font_px)
        entry_distances = self._distances_from_entry()
        restricted_badges: list[tuple[tuple[int, int], int, tuple]] = []
        other_badges: list[tuple[tuple[int, int], int, tuple]] = []
        for connection in self._c.connections:
            pos1 = self._centers[connection.pos1]
            pos2 = self._centers[connection.pos2]
            pygame.draw.line(
                back_ground, COLORS["BLACK"], pos1, pos2,
                CONNECTION_LINE_WIDTH
            )
            pygame.draw.line(
                back_ground, COLORS["WHITE"], pos1, pos2,
                CONNECTION_LINE_INNER_WIDTH
            )

            midpoint = (
                (pos1[0] + pos2[0]) // 2,
                (pos1[1] + pos2[1]) // 2,
            )

            downstream_name = connection.pos2
            if (
                entry_distances.get(connection.pos1, 0)
                > entry_distances.get(connection.pos2, 0)
            ):
                downstream_name = connection.pos1
            downstream_zone = self._c.hubs[downstream_name].zone

            if downstream_zone == "restricted":
                badge_fill = ZONE_COLORS["restricted"]
                restricted_badges.append(
                    (midpoint, connection.capacity, badge_fill)
                )
            else:
                badge_fill = (
                    ZONE_COLORS["priority"] if downstream_zone == "priority"
                    else COLORS["WHITE"]
                )
                other_badges.append(
                    (midpoint, connection.capacity, badge_fill)
                )

        for midpoint, capacity, badge_fill in restricted_badges + other_badges:
            pygame.draw.circle(
                back_ground, badge_fill, midpoint, capacity_radius
            )
            pygame.draw.circle(
                back_ground, COLORS["BLACK"], midpoint, capacity_radius,
                BADGE_BORDER_WIDTH
            )

            capacity_label = capacity_font.render(
                str(capacity), False, COLORS["BLACK"]
            )
            capacity_rect = capacity_label.get_rect(center=midpoint)
            back_ground.blit(capacity_label, capacity_rect)

        for name, hub in self._c.hubs.items():
            center = self._centers[name]
            color = pygame.Color(ZONE_COLORS[hub.zone])
            if hub.color:
                try:
                    color = pygame.Color(hub.color)
                except ValueError:
                    pass

            tinted_node_sprite = scaled_node_sprite.copy()
            tinted_node_sprite.fill(
                color, special_flags=pygame.BLEND_RGBA_MULT
            )
            node_rect = tinted_node_sprite.get_rect(center=center)
            back_ground.blit(tinted_node_sprite, node_rect)

            if hub.zone not in ("start", "end"):
                badge_center = (
                    node_rect.right - capacity_radius,
                    node_rect.bottom - capacity_radius,
                )
                pygame.draw.circle(
                    back_ground, COLORS["WHITE"], badge_center,
                    capacity_radius
                )
                pygame.draw.circle(
                    back_ground, COLORS["BLACK"], badge_center,
                    capacity_radius, BADGE_BORDER_WIDTH
                )
                capacity_label = capacity_font.render(
                    str(hub.max_drones), False, COLORS["BLACK"]
                )
                capacity_rect = capacity_label.get_rect(center=badge_center)
                back_ground.blit(capacity_label, capacity_rect)

        drone_sprite = pygame.image.load("assets/drone.png").convert_alpha()
        drone_size = int(self._grid * DRONE_SPRITE_SCALE)
        scaled_drone_sprite = pygame.transform.scale(
            drone_sprite, (drone_size, drone_size)
        )
        drone_badge_radius = min(
            max(
                DRONE_BADGE_RADIUS_FLOOR,
                self._grid // DRONE_BADGE_GRID_DIVISOR
            ),
            max(
                DRONE_BADGE_RADIUS_SIZE_CAP_MIN,
                drone_size // DRONE_BADGE_SIZE_CAP_DIVISOR
            )
        )
        drone_badge_font_px = min(
            max(
                DRONE_BADGE_FONT_FLOOR,
                self._grid // DRONE_BADGE_GRID_DIVISOR
            ),
            max(
                DRONE_BADGE_FONT_SIZE_CAP_MIN,
                drone_size // DRONE_BADGE_SIZE_CAP_DIVISOR
            )
        )
        drone_badge_font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf",
            drone_badge_font_px)

        entry = self._c.gates.entry
        turn_positions = self._initiator.turn_positions
        total_turns = len(turn_positions)

        entry_x, entry_y = self._to_screen(entry.x, entry.y)
        drone_waypoints: dict[int, list[tuple[int, int, int]]] = {
            drone_id: [(-1, entry_x, entry_y)]
            for drone_id in range(1, self._c.nb_drones + 1)
        }
        for turn_index, positions in enumerate(turn_positions):
            for position in positions:
                if position.in_transit:
                    continue
                sx, sy = self._to_screen(position.x, position.y)
                drone_waypoints[position.drone_id].append(
                    (turn_index, sx, sy)
                )

        turn_font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf",
            max(
                TURN_LABEL_FONT_FLOOR,
                sidebar_width // TURN_LABEL_SIDEBAR_DIVISOR
            )
        )
        loop_frame = 0

        while self._running:
            self._clock.tick(self._ticks)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            loop_frame += 1
            if loop_frame > START_DELAY_FRAMES:
                self._frame_count += 1
            elapsed_turns = self._frame_count // TURN_DURATION_FRAMES

            drone_counts: dict[tuple[int, int], int] = {}
            drone_directions: dict[tuple[int, int], tuple[int, int]] = {}
            for waypoints in drone_waypoints.values():
                drone_pos, direction = self._interpolate(waypoints)
                drone_counts[drone_pos] = drone_counts.get(drone_pos, 0) + 1
                if drone_pos not in drone_directions:
                    drone_directions[drone_pos] = direction

            screen.blit(back_ground, (0, 0))
            for drone_pos, count in drone_counts.items():
                dx, dy = drone_directions[drone_pos]
                if dx == 0 and dy == 0:
                    angle = 0.0
                else:
                    angle = -math.degrees(math.atan2(dx, -dy))
                rotated_sprite = pygame.transform.rotate(
                    scaled_drone_sprite, angle
                )
                drone_rect = rotated_sprite.get_rect(center=drone_pos)
                screen.blit(rotated_sprite, drone_rect)

                pygame.draw.circle(
                    screen, COLORS["WHITE"], drone_pos, drone_badge_radius
                )
                pygame.draw.circle(
                    screen, COLORS["BLACK"], drone_pos,
                    drone_badge_radius, BADGE_BORDER_WIDTH
                )
                drone_label = drone_badge_font.render(
                    str(count), False, COLORS["BLACK"]
                )
                drone_label_rect = drone_label.get_rect(center=drone_pos)
                screen.blit(drone_label, drone_label_rect)

            turn_label = turn_font.render(
                f"Turno {min(elapsed_turns, total_turns)}",
                False, COLORS["WHITE"]
            )
            screen.blit(
                turn_label, (
                    map_width + TURN_LABEL_MARGIN_SIDE,
                    TURN_LABEL_MARGIN_TOP)
            )

            pygame.display.flip()
        pygame.quit()
