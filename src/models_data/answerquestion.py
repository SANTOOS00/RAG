from models_data import UnanswerdQuestion, MinimalSource


class AnsweredQuestion(UnanswerdQuestion):
    sources: list[MinimalSource]
    answer: str
