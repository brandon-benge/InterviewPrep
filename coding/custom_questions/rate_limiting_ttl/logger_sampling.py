class Logger:
    def __init__(self, level: str = "INFO"):
        ...

    def log(self, level: str, message_key: str, message: str, timestamp_sec: int) -> bool:
        ...


