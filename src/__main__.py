
from fire import Fire
from rag import RAG
from custem_error import RagError

if __name__ == "__main__":
    try:
        Fire(RAG)
    except RagError as e:
        e.print()