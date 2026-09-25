class RagError(Exception):
    def __init__(self, **context: str) -> None:
        super().__init__(self.__format_output_error(context))

    def __format_output_error(self, context: dict[str, str]) -> str:
        return f"[Error]: {context['message']}"

    def print(self) -> None:
        print("self")


class RagWarning(UserWarning):
    pass