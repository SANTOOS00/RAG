from pydantic import BaseModel
from models_data import AnsweredQuestion,\
    UnanswerdQuestion

class RagDataset(BaseModel):
    rag_questions: list[AnsweredQuestion | UnanswerdQuestion]
