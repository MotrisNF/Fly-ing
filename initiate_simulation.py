from map_config import MapConfig
from text_printer import Printer
from typing import Optional
from exceptions import PathError


class Initiator:
    def __init__(self, config: Optional[MapConfig]) -> None:
        self.config = config
        self.printer: Printer = Printer()
        self.printer.print_by_letter(
            "Initiating the simulation...",
            0.1,
            0.5,
            "\033[92m"
        )

    def fill_hub_connections(self) -> None:
        if self.config is None:
            raise PathError("Sonthing was wrong")
        for key, hub in self.config.hubs.items():
            for connection in self.config.connections:
                if connection.pos1 == key:
                    hub.connection.append(connection)
                elif connection.pos2 == key:
                    hub.connection.append(connection)

    def find_path_to_end(self) -> bool:
        if self.config is None:
            raise PathError("The config is not loaded.")
        self.fill_hub_connections()
        self.printer.print_by_letter(
            "Serching a valid way to the end...",
            0.02,
            2,
            "\033[92m"
        )
        start = self.config.gates.entry.name
        end = self.config.gates.exit.name
        visited: set[str] = set()
        to_visit = [start]
        while to_visit:
            current = to_visit.pop()
            if current == end:
                return True
            if current in visited:
                continue
            visited.add(current)
            hub = self.config.hubs.get(current)
            if hub is None:
                continue
            for connection in hub.connection:
                if connection.pos1 == current:
                    neighbor = connection.pos2
                else:
                    neighbor = connection.pos1
                if neighbor not in visited:
                    to_visit.append(neighbor)
        return False
