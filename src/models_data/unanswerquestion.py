from pydantic import BaseModel, Field
from typing import uui


class UnanswerdQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda:
                              str(uuid4()))
    question: str
