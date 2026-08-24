from initiate_simulation import Initiator
from exceptions import PathError
from constants import (
    COLORS, ZONE_COLORS, DESKTOP_OFFSET, MARGIN_X, MARGIN_Y, MAX_GRID,
    SIDEBAR_RATIO, TURN_DURATION_FRAMES, TURN_PAUSE_FRAMES,
    START_DELAY_FRAMES
)

import math
import pygame


class Pyshow():
    def __init__(self, initiator: Initiator) -> None:
        if initiator.config is None:
            raise PathError("The config is not loaded.")
        self._initiator = initiator
        self._c = initiator.config
        self._dimentions: tuple[int, int] = (0, 0)
        self._running: bool = True
        self._clock = pygame.time.Clock()
        self._ticks: float = 30.0
        self._grid: int = 0
        self._spacing_x: float = 0.0
        self._spacing_y: float = 0.0
        self._offset_x: int = 0
        self._offset_y: int = 0
        self._centers: dict[str, tuple[int, int]] = {}
        self._frame_count: int = 0

    def _to_screen(self, x: int, y: int) -> tuple[int, int]:
        col = x - self._c.min_x
        row = y - self._c.min_y
        return (
            self._offset_x + int(col * self._spacing_x),
            self._offset_y + int(row * self._spacing_y),
        )

    def _interpolate(
        self, waypoints: list[tuple[int, int, int]]
    ) -> tuple[tuple[int, int], tuple[int, int]]:
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
        for k in range(i, -1, -1):
            x0, y0 = waypoints[k][1], waypoints[k][2]
            x1, y1 = waypoints[k + 1][1], waypoints[k + 1][2]
            if (x1 - x0, y1 - y0) != (0, 0):
                return (x1 - x0, y1 - y0)
        return (0, -1)

    def start(self) -> None:
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
        moon_size = min(map_width, map_height) // 4
        moon_scaled = pygame.transform.scale(
            moon_sprite, (moon_size, moon_size)
        )
        moon_rect = moon_scaled.get_rect(
            center=(map_width // 2, map_height // 2)
        )
        back_ground.blit(moon_scaled, moon_rect)

        sidebar_rect = pygame.Rect(map_width, 0, sidebar_width, map_height)
        pygame.draw.rect(back_ground, COLORS["BLACK"], sidebar_rect)

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
        size = int(self._grid * 0.7)
        scaled_node_sprite = pygame.transform.scale(node_sprite, (size, size))

        for name, hub in self._c.hubs.items():
            self._centers[name] = self._to_screen(hub.x, hub.y)

        capacity_radius = min(
            max(6, self._grid // 8), max(2, size // 3)
        )
        capacity_font_px = min(
            max(9, self._grid // 8), max(6, size // 3)
        )
        capacity_font = pygame.font.SysFont(None, capacity_font_px)
        for connection in self._c.connections:
            pos1 = self._centers[connection.pos1]
            pos2 = self._centers[connection.pos2]
            pygame.draw.line(back_ground, COLORS["BLACK"], pos1, pos2, 6)

            midpoint = (
                (pos1[0] + pos2[0]) // 2,
                (pos1[1] + pos2[1]) // 2,
            )
            pygame.draw.circle(
                back_ground, COLORS["WHITE"], midpoint, capacity_radius
            )
            pygame.draw.circle(
                back_ground, COLORS["BLACK"], midpoint, capacity_radius, 2
            )
            pygame.draw.line(back_ground, COLORS["WHITE"], pos1, pos2, 2)

            capacity_label = capacity_font.render(
                str(connection.capacity), False, COLORS["BLACK"]
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
                    capacity_radius, 2
                )
                capacity_label = capacity_font.render(
                    str(hub.max_drones), False, COLORS["BLACK"]
                )
                capacity_rect = capacity_label.get_rect(center=badge_center)
                back_ground.blit(capacity_label, capacity_rect)

        drone_sprite = pygame.image.load("assets/drone.png").convert_alpha()
        drone_size = int(self._grid * 0.55)
        scaled_drone_sprite = pygame.transform.scale(
            drone_sprite, (drone_size, drone_size)
        )
        drone_badge_radius = min(
            max(6, self._grid // 10), max(2, drone_size // 3)
        )
        drone_badge_font_px = min(
            max(9, self._grid // 10), max(6, drone_size // 3)
        )
        drone_badge_font = pygame.font.SysFont(None, drone_badge_font_px)

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

        turn_font = pygame.font.SysFont(None, max(24, sidebar_width // 12))
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
                    drone_badge_radius, 2
                )
                drone_label = drone_badge_font.render(
                    str(count), False, COLORS["BLACK"]
                )
                drone_label_rect = drone_label.get_rect(center=drone_pos)
                screen.blit(drone_label, drone_label_rect)

            turn_label = turn_font.render(
                f"Turno {min(elapsed_turns, total_turns)}/{total_turns}",
                False, COLORS["WHITE"]
            )
            screen.blit(turn_label, (map_width + 20, 20))

            pygame.display.flip()
        pygame.quit()
