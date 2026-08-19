"""Entry point: runs the simulation and handles Ctrl+C gracefully."""

from exceptions import ConfigError
from starter import StartProgram
from text_printer import Printer
import signal


def main() -> None:
    """Run the welcome flow, load the map, and report the outcome."""
    starter = StartProgram()
    try:
        starter.start_simulation()
        starter.printer.print_by_letter(
            f"Opening '{starter.file}'...",
            0.05,
            1.0
            )
        starter.open_config()
        print(starter.parser.config)
    except ConfigError as e:
        starter.printer.print_by_letter(
            f"{type(e).__name__}: {e}",
            0.01,
            0.5
            )
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            print("\r\033[2K", end="")
            Printer.print_by_letter("Don't kill my program...",
                                    0.4,
                                    0.0)
            exit(1)
        finally:
            signal.signal(signal.SIGINT, old_handler)
