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
        for key, hub in self.config.hubs.items():
            for connection in self.config.connections:
                if connection.pos1 == key:
                    hub.connection.append(connection)
                elif connection.pos2 == key:
                    hub.connection.append(connection)
        print(self.config.hubs)

    def validate_path_to_finish(self) -> None:
        if self.config is None:
            raise PathError("The config is not loaded.")
        actual_hub = self.config.hubs.get(self.config.gates.entry.name)
        print(actual_hub)
