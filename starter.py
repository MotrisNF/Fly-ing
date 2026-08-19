import time

from text_printer import Printer

from exceptions import FileError


class StartProgram:
    def __init__(self) -> None:
        self.printer = Printer()
        self.file: str = ""

    def start_simulation(self) -> None:
        self.printer.print_by_letter(
                                    "Welcome to the dron simulation...",
                                    0.02,
                                    2.0
                                    )
        self.printer.print_by_letter(
                                    "Introduce the name of the map: ",
                                    0.02,
                                    0.0
                                    )
        self.file = input().strip()
        if self.file == "":
            raise FileError("A name for the map file is mandatory.")

        time.sleep(1)
        try:
            with open(self.file):
                ...
        except FileNotFoundError as e:
            raise FileError(f"The '{self.file}' file do not exist.") from e
        except OSError as e:
            raise FileError(f"The '{self.file}' file can't be opened") from e

        self.printer.erase_line(3)
