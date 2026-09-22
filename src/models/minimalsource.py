from pydantic import BaseModel, Field
from uuid import uuid4

class MinimalSource(BaseModel):
    """
    pass
    """
    file_path: str
    first_character: int
    last_character_index: int


class UnanswerdQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda:
                              str(uuid4()))
    question: str


class AnsweredQuestion(UnanswerdQuestion):
    sources: list[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: list[AnsweredQuestion | UnanswerdQuestion]


if __name__ == "__main__":
    UnanswerdQuestion(
      question_id="0d29b0e8-686c-41b7-9a48-50f8e4bc63de",
      question="What's the default value of \
        trust_remote_code in vLLM's LLM class constructor?"
    )