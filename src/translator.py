class Translator:

    original_query = str
    translated_query = str

    def __init__(self, query: str) -> None:
        self.original_query = query
        self.translated_query = ""

    def translate_query(self, query: str):
        pass        