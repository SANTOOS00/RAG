from fire import Fire
from ..src.rag import RAG
from custem_error import RagError


def main() -> None:
if __name__ == "__main__":
    try:
        Fire(RAG)
    except ragerror as e:
        RagError.print()