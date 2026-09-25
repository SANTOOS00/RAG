from fire import Fire
from ..src.rag import RAG

class root:
    def chelder_1(self, val: int) -> None:
        print("childer 1 | val == ", val)

    def chelder_2(self, val: int) -> None:
        print("childer 2| val == ", val)


def main() -> None:
if __name__ == "__main__":
    try:
        Fire(RAG)
    except  as e:
        printe