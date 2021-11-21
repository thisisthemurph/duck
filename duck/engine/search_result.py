from duck.helpers.stripper import strip_tags


class SearchResult:
    def __init__(self, url: str, title: str, snippet: str):
        self.url = url
        self.title = title
        self.__snippet = snippet

    def __repr__(self) -> str:
        return f"{self.title}\n{self.snippet}\n  >>  {self.url}"

    @property
    def snippet(self) -> str:
        return strip_tags(self.__snippet)
