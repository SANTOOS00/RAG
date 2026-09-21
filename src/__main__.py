import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple
from tqdm import tqdm
import fire
from pydantic import BaseModel


class ChunkMetadata(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int
    text: str


def chunk_python_code(content: str, max_chunk_size: int) -> List[Tuple[int, int, str]]:
    """Découpe du code Python par blocs/fonctions tout en respectant max_chunk_size."""
    chunks = []
    lines = content.splitlines(keepends=True)
    current_chunk = ""
    start_idx = 0
    current_idx = 0

    for line in lines:
        if len(current_chunk) + len(line) > max_chunk_size and current_chunk:
            end_idx = start_idx + len(current_chunk)
            chunks.append((start_idx, end_idx, current_chunk))
            start_idx = end_idx
            current_chunk = ""
        current_chunk += line

    if current_chunk:
        end_idx = start_idx + len(current_chunk)
        chunks.append((start_idx, end_idx, current_chunk))

    return chunks


def chunk_markdown_text(content: str, max_chunk_size: int) -> List[Tuple[int, int, str]]:
    """Découpe du texte Markdown par sections ou paragraphes."""
    chunks = []
    paragraphs = content.split("\n\n")
    start_idx = 0
    current_chunk = ""
    chunk_start = 0

    for p in paragraphs:
        p_with_sep = p + "\n\n"
        if len(current_chunk) + len(p_with_sep) > max_chunk_size and current_chunk:
            chunk_end = chunk_start + len(current_chunk)
            chunks.append((chunk_start, chunk_end, current_chunk))
            chunk_start = chunk_end
            current_chunk = ""
        current_chunk += p_with_sep

    if current_chunk:
        chunk_end = chunk_start + len(current_chunk)
        chunks.append((chunk_start, chunk_end, current_chunk))

    return chunks


class Indexer:
    """Composant responsable de l'indexation du corpus."""

    def __init__(self, raw_dir: str = "data/raw", processed_dir: str = "data/processed"):
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def build_index(self, max_chunk_size: int = 2000) -> None:
        """Parcourt le dossier raw, découpe les fichiers et sauvegarde l'index."""
        all_files = list(self.raw_dir.rglob("*"))
        valid_files = [f for f in all_files if f.is_file() and f.suffix in [".py", ".md", ".txt"]]

        chunks_data: List[Dict[str, Any]] = []

        print(f"Chargement et découpage des fichiers depuis {self.raw_dir}...")
        for file_path in tqdm(valid_files, desc="Chunking"):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                rel_path = str(file_path)

                if file_path.suffix == ".py":
                    spans = chunk_python_code(content, max_chunk_size)
                else:
                    spans = chunk_markdown_text(content, max_chunk_size)

                for start, end, text in spans:
                    # Garantir strict respect de la taille maximale
                    if len(text) <= max_chunk_size:
                        chunk_meta = ChunkMetadata(
                            file_path=rel_path,
                            first_character_index=start,
                            last_character_index=end,
                            text=text
                        )
                        chunks_data.append(chunk_meta.model_dump())

            except Exception as e:
                continue

        # Sauvegarde de l'index des chunks
        output_chunks_file = self.processed_dir / "index_chunks.json"
        with open(output_chunks_file, "w", encoding="utf-8") as f:
            json.dump(chunks_data, f, indent=2)

        print(f"Ingestion terminée ! {len(chunks_data)} chunks indexés sous {self.processed_dir}/")


def index(max_chunk_size: int = 2000, raw_dir: str = "data/raw", processed_dir: str = "data/processed") -> None:
    """Commande CLI pour indexer le codebase."""
    indexer = Indexer(raw_dir=raw_dir, processed_dir=processed_dir)
    print(indexer)
    indexer.build_index(max_chunk_size=max_chunk_size)


if __name__ == "__main__":
    fire.Fire(index)