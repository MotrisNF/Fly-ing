import time


class Printer:
    @staticmethod
    def print_by_letter(
                        text: str,
                        speed: float,
                        time_to_sleep: float
                        ) -> None:
        temp_text: str = ""
        for leter in text:
            temp_text = temp_text + leter
            print(temp_text, end="\r")
            time.sleep(speed)
        print(temp_text)
        time.sleep(time_to_sleep)

    @staticmethod
    def erase_line(times: int = 0) -> None:
        for _ in range(0, times + 1):
            print(end="\033[2K\033[A\r")
            Printer.print_by_letter(
                "                                                     ",
                0.025,
                0
            )
            print("\033[2K\r\033[A", end="")
