import argparse
from typing import Sequence, Any, Union

from duck import app
from duck.helpers.color import Color


class LimitAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Union[str, None] = ...,
    ) -> None:
        if values < 1 or values > 25:
            parser.error("The limit must be a value between 1 and 25.")

        setattr(namespace, self.dest, values)


def parse_args() -> argparse.Namespace:
    """
    Creates the argparse namespace for the terminal inputs.

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        prog="duck",
        description="A utility for completing DuckDuckGo web searches using the commandline.",
    )

    #
    # The primary functionality
    #

    parser.add_argument("search", nargs="*", help="the search term")
    parser.add_argument(
        "-l",
        "--limit",
        action=LimitAction,
        type=int,
        help="max number of results to be displayed",
    )

    #
    # Updating the user settings
    #

    permitted_colors = [c.name for c in Color]
    parser.add_argument(
        "--toggle-styling", help="toggle stylised outputs on or off", action="store_true"
    )
    parser.add_argument(
        "--set-primary-color",
        help="sets the color used for the result headlines",
        choices=permitted_colors,
    )
    parser.add_argument(
        "--set-secondary-color",
        help="sets the color used for the result URLs",
        choices=permitted_colors,
    )
    parser.add_argument(
        "--reset-props", help="sets the user properties back the the defaults", action="store_true"
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    app.run(args)
