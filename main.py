"""Entry point: runs the simulation and handles Ctrl+C gracefully."""

from exceptions import ConfigError
from starter import StartProgram
from text_printer import Printer
from initiate_simulation import Initiator

import signal


def main() -> None:
    """Run the welcome flow, load the map, and report the outcome."""
    starter = StartProgram()
    try:
        starter.start_simulation()
        starter.printer.print_by_letter(
            f"Opening '{starter.file}'...",
            0.05,
            1.0,
            "\033[92m"
            )
        starter.open_config()
        initialicer = Initiator(starter.parser.config)
        initialicer.printer.print_by_letter(
            "Everything it's ok until here",
            0.05,
            0.0
        )
        initialicer.fill_hub_connections()
    except ConfigError as e:
        starter.printer.print_by_letter(
            f"{type(e).__name__}: {e}",
            0.01,
            0.5,
            "\033[91m"
            )
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            print("\r\033[2K", end="")
            Printer.print_by_letter("Don't kill my f****** program...",
                                    0.4,
                                    0.0,
                                    "\033[91m"
                                    )
            exit(0)
        finally:
            signal.signal(signal.SIGINT, old_handler)
