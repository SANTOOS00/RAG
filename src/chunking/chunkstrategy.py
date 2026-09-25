from typing import Protocol


class chunkstrategie(Protocol):
    def chunk(self) -> None: ...


