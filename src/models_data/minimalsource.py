
from pydantic import BaseModel


class MinimalSource(BaseModel):
    file_path: str
    first_character: int
    last_character_index: int
