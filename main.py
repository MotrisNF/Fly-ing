# import pydantic
from exceptions import ConfigError

from starter import StartProgram


class Parser:
    def __init__(self, file: str) -> None:
        self.file = file


if __name__ == "__main__":
    starter = StartProgram()
    try:
        starter.start_simulation()
    except ConfigError as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)
    parser = Parser(starter.file)
    starter.printer.print_by_letter(f"Opening '{parser.file}'", 0.05, 1.0)
