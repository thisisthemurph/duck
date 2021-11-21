import os
import tempfile
from pathlib import Path
from typing import Iterable, List, Union


class History:
    """Represents the users search history."""

    def __init__(self) -> None:
        self.__file_path: Union[Path, None] = None
        self.__history_items: List[str] = []

        self.__get_path()
        self.__create_if_not_exists()
        self.__read()

    def __get_path(self):
        tmp_dir = Path(tempfile.gettempdir()) / "duck-cmd-props-tmp"

        if not tmp_dir.exists():
            os.makedirs(tmp_dir)

        self.__file_path = tmp_dir / "history.txt"

    def __create_if_not_exists(self):
        if not self.__file_path.exists():
            self.__write()

    def __read(self):
        with open(self.__file_path, "r", encoding="utf8") as hist_file:
            self.__history_items = [item.strip() for item in hist_file.readlines()]

    def __write(self):
        with open(self.__file_path, "w", encoding="utf8") as hist_file:
            hist_file.write("\n".join(self.__history_items))

    def get_history(self) -> Iterable[str]:
        """Returns an iterable of history items."""
        return self.__history_items

    def add(self, history_item):
        """Adds a new history item."""
        self.__history_items.append(history_item)
        self.__write()

    def clear(self):
        """Clears the history."""
        self.__history_items = []
        self.__write()
