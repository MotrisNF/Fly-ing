import os
import sys
import termios
import time


class Printer:
    @staticmethod
    def print_by_letter(
                        text: str,
                        speed: float,
                        time_to_sleep: float
                        ) -> None:
        fd = sys.stdin.fileno()
        is_tty = os.isatty(fd)
        old_settings = None
        if is_tty:
            old_settings = termios.tcgetattr(fd)
            no_echo_settings = termios.tcgetattr(fd)
            no_echo_settings[3] = no_echo_settings[3] & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, no_echo_settings)
        try:
            temp_text: str = ""
            print("\033[?25l", end="")
            for leter in text:
                temp_text = temp_text + leter
                print(temp_text, end="\r")
                time.sleep(speed)
            print(temp_text, end="")
            print("\033[?25h", end="")
            time.sleep(time_to_sleep)
            print()
        finally:
            if is_tty:
                termios.tcflush(fd, termios.TCIFLUSH)
                termios.tcsetattr(fd, termios.TCSANOW, old_settings)

    @staticmethod
    def erase_line(times: int = 0) -> None:
        for _ in range(0, times):
            print(end="\033[2K\033[A\r")
            Printer.print_by_letter(
                "                                                     ",
                0.025,
                0
            )
            print("\033[2K\r\033[A", end="")
