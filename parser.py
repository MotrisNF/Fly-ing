from typing import TextIO

from exceptions import FileError


class Parser:
    def __init__(self) -> None:
        self.temp_list: list[list[list[str]]] = []

    def read_file(self, file: TextIO) -> None:
        splited: list[list[str]] = []
        for line in file:
            line.strip()
            if line.strip() and not line.startswith("#"):
                splited.append(line.split())
                self.temp_list.append(splited)
        if len(self.temp_list) == 0:
            raise FileError("The file dont have any key")
