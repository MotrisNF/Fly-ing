"""Entry point: runs the simulation and handles Ctrl+C gracefully."""

from exceptions import ConfigError, PathError
from starter import StartProgram
from text_printer import Printer
from initiate_simulation import Initiator

import signal
import sys


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
        if not initialicer.find_path_to_end():
            raise PathError("There is not a posible way to the end.")
        initialicer.printer.print_by_letter(
            "Found a posible way on the map recived.",
            0.02,
            1,
            "\033[92m"
        )
        initialicer.printer.erase_line(4)
        initialicer.printer.print_by_letter(
            "Starting the drone moves...",
            0.05,
            2,
            "\033[92m"
        )
        initialicer.run_simulation()
        for step in initialicer.turns:
            initialicer.printer.print_by_letter(
                step,
                0.02,
                0.1
            )
        initialicer.printer.print_by_letter(
            "Counying the movements...",
            0.05,
            2
        )
        
    except ConfigError as e:
        starter.printer.print_by_letter(
            f"{type(e).__name__}: {e}",
            0.01,
            0.5,
            "\033[91m"
            )
        sys.exit(1)


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
            sys.exit(0)
        finally:
            signal.signal(signal.SIGINT, old_handler)
    finally:
        printer = Printer()
        printer.print_by_letter(
            "End of the simulation...",
            0.02,
            0.0
        )
