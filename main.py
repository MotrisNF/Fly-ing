# import pydantic
from exceptions import ConfigError

from starter import StartProgram


if __name__ == "__main__":
    starter = StartProgram()
    try:
        starter.start_simulation()
    except ConfigError as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)
