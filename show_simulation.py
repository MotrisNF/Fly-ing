from map_config import MapConfig
from initiate_simulation import Initiator
from constants import COLORS, ZONE_COLORS

import pygame


class Pyshow():
    def __init__(self, config: MapConfig) -> None:
        self._config = config
        self._dimentions: tuple[int, int] = (4096 - 250, 2160 - 250)
        self._running: bool = True
        self._clock = pygame.time.Clock()
        self._ticks: float = 30.0

    def start(self, initiator: Initiator) -> None:
        self._initiator = initiator
        self._config = initiator.config
        pygame.init()

        screen = pygame.display.set_mode(self._dimentions)
        back_ground = pygame.Surface(self._dimentions)
        back_ground.fill(COLORS["GREEN"])

        cols = self._config.width + 1
        rows = self._config.height + 1
        self._grid: int = min(
            self._dimentions[0] // cols,
            self._dimentions[1] // rows
        )
        offset_x = (self._dimentions[0] - self._grid * cols) // 2
        offset_y = (self._dimentions[1] - self._grid * rows) // 2

        # for x in range(cols + 1):
        #     pos_x = offset_x + self._grid * x
        #     pygame.draw.line(
        #             back_ground,
        #             COLORS["BLACK"],
        #             (pos_x, offset_y),
        #             (pos_x, offset_y + self._grid * rows),
        #             3
        #         )
        # for y in range(rows + 1):
        #     pos_y = offset_y + self._grid * y
        #     pygame.draw.line(
        #             back_ground,
        #             COLORS["BLACK"],
        #             (offset_x, pos_y),
        #             (offset_x + self._grid * cols, pos_y),
        #             3
        #         )

        radius = int(self._grid * 0.35)
        font = pygame.font.SysFont(None, max(14, self._grid // 6))
        centers: dict[str, tuple[int, int]] = {}
        for name, hub in self._config.hubs.items():
            col = hub.x - self._config.min_x
            row = hub.y - self._config.min_y
            center = (
                offset_x + self._grid * col + self._grid // 2,
                offset_y + self._grid * row + self._grid // 2,
            )
            centers[name] = center
            color = ZONE_COLORS[hub.zone]
            if hub.color:
                try:
                    color = pygame.Color(hub.color)
                except ValueError:
                    pass
            pygame.draw.circle(back_ground, color, center, radius)
            pygame.draw.circle(back_ground, COLORS["BLACK"], center, radius, 3)

            label = font.render(name, True, COLORS["BLACK"])
            label_rect = label.get_rect(
                midbottom=(center[0], center[1] - radius - 14)
            )
            back_ground.blit(label, label_rect)

        for connection in self._config.connections:
            pygame.draw.line(
                back_ground,
                COLORS["GRAY"],
                centers[connection.pos1],
                centers[connection.pos2],
                2
            )

        while self._running:
            self._clock.tick(self._ticks)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            screen.blit(back_ground, (0, 0))
            pygame.display.flip()
        pygame.quit()
