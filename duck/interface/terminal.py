from typing import List, Union
from termcolor import colored, cprint

from duck.helpers.color import Color
from duck.properties.props import Properties
from duck.engine.search_result import SearchResult


class TerminalInterface:
    def __init__(self, props: Properties) -> None:
        self.props: Properties = props
        self.results: List[SearchResult] = None

    def print(
        self,
        text: Union[str, None] = None,
        color: Union[Color, None] = None,
        bold: bool = False,
        underline: bool = False,
    ):
        """A stylized print."""
        attrs: List[str] = []

        if bold:
            attrs.append("bold")
        if underline:
            attrs.append("underline")

        if not text:
            print()
        elif self.props.style_output:
            color_name = None if not color else color.name
            cprint(colored(text, color=color_name, attrs=attrs))
        else:
            print(text)

    def update(self, results: List[SearchResult]) -> None:
        self.results = results
        self.__display()

    def __display(self):
        idx = 0
        for idx, result in enumerate(self.results, start=1):
            self.print(
                f"{idx}. {result.title}", self.props.primary_color, bold=True, underline=True
            )
            self.print(result.url, self.props.secondary_color, bold=True)
            self.print(result.snippet)
            self.print()

        self.print(f"Fin: {idx} results returned.")
