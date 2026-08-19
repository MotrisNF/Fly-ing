# import pydantic

from exceptions import ConfigError
from starter import StartProgram


def main() -> None:
    starter = StartProgram()
    try:
        starter.start_simulation()
    except ConfigError as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)
    starter.printer.print_by_letter(f"Opening '{starter.file}'...", 0.05, 1.0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\r\033[2K", end="")
        exit("Don't kill my program...")
