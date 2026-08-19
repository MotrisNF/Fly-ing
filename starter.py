"""Bootstraps the simulation: greets the user and loads the map file."""

from text_printer import Printer
from exceptions import FileError
from parser import Parser


class StartProgram:
    """Coordinates the welcome prompt and map file loading."""

    def __init__(self) -> None:
        self.printer = Printer()
        self.parser = Parser()
        self.file: str = ""

    def start_simulation(self) -> None:
        """Greet the user, ask for a map filename, and check it opens.

        Raises:
            FileError: If no filename is entered, or the file cannot
                be opened.
        """
        self.printer.print_by_letter(
                                    "Welcome to the dron simulation...",
                                    0.02,
                                    1.0
                                    )
        self.printer.print_by_letter(
                                    "Introduce the name of the map: ",
                                    0.02,
                                    0.0
                                    )
        self.file = input().strip()
        if self.file == "":
            raise FileError("A name for the map file is mandatory.")

        try:
            with open(self.file, 'r'):
                ...

        except FileNotFoundError as e:
            raise FileError(f"The '{self.file}' file do not exist.") from e
        except OSError as e:
            raise FileError(f"The '{self.file}' file can't be opened") from e

        self.printer.erase_line(3)

    def open_config(self) -> None:
        """Read and parse the previously validated map file.

        Raises:
            FileError: If the map file's contents are malformed.
        """
        with open(self.file) as file:
            self.parser.read_file(file)
