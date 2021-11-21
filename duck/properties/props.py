import os
import json
import tempfile
from pathlib import Path
from typing import Union

from duck.helpers.color import Color

DEFAULT_PROPS = {"outputStyling": True, "primaryColor": "red", "secondaryColor": "white"}


class Properties:
    """Represents the users properties."""

    def __init__(self) -> None:
        self.__file_path = None
        self.__data: dict = DEFAULT_PROPS

        self.__get_props_path()
        self.__create_if_not_exists()
        self.__read()

    def __get_props_path(self):
        tmp_dir = Path(tempfile.gettempdir()) / "duck-cmd-props-tmp"

        if not tmp_dir.exists():
            os.makedirs(tmp_dir)

        self.__file_path = tmp_dir / "properties.json"

    def __create_if_not_exists(self) -> None:
        if not self.__file_path.exists():
            self.__write()

    def __read(self) -> None:
        with open(self.__file_path, "r", encoding="utf8") as props_file:
            self.__data: dict = json.load(props_file)

    def __write(self) -> None:
        with open(self.__file_path, "w", encoding="utf8") as props_file:
            json.dump(self.__data, props_file)

    @property
    def style_output(self) -> bool:
        """A boolean representing if styling should be applied."""
        return self.__data.get("outputStyling", DEFAULT_PROPS["outputStyling"])

    @property
    def primary_color(self) -> Color:
        """The primary color used for formatting titles."""
        return Color[self.__data.get("primaryColor", DEFAULT_PROPS["primaryColor"])]

    @property
    def secondary_color(self) -> Color:
        """The secondary color used for formatting URLs"""
        return Color[self.__data.get("secondaryColor", DEFAULT_PROPS["secondaryColor"])]

    def update(self, key: str, value: Union[str, int, None]) -> None:
        """
        Updates the properties by the given key.

        Parameters:
            key (str): the property to be updated
            value (str | int | None): the new value
        """
        self.__data[key] = value
        self.__write()

    def toggle_output_styling(self):
        """Toggles style_output and returns the new value."""
        self.update("outputStyling", not self.style_output)
        return self.style_output

    def update_primary_color(self, color: Color):
        """Changes the primary color property."""
        self.update("primaryColor", color.name)

    def update_secondary_color(self, color: Color):
        """Changes the secondary color property."""
        self.update("secondaryColor", color.name)

    def reset(self):
        """Reset the peroperties to the defaults."""
        self.__data = DEFAULT_PROPS
        self.__write()
