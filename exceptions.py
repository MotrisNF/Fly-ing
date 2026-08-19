class ConfigError(Exception):
    def __init__(self, msg: str = "Default ConfigError."):
        super().__init__(msg)


class FileError(ConfigError):
    def __init__(self, msg: str = "Default FileError.") -> None:
        super().__init__(msg)
