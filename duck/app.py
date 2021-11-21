import argparse
from duck import history

from duck.helpers.color import Color
from duck.history.history import History
from duck.properties.props import Properties
from duck.engine.search_engine import DuckDuckGo
from duck.interface.terminal import TerminalInterface


def run(args: argparse.Namespace) -> None:
    search_history = History()
    props = Properties()
    interface = TerminalInterface(props)

    if args.toggle_styling:
        is_on = props.toggle_output_styling()
        interface.print(f"Output styling has been switched {'on' if is_on else 'off'}")

    elif args.set_primary_color:
        color = Color[args.set_primary_color]
        props.update_primary_color(color)
        interface.print(f"Primary color changed to {color.name}", color=color)

    elif args.set_secondary_color:
        color = Color[args.set_secondary_color]
        props.update_secondary_color(color)
        interface.print(f"Secondary color changed to {color.name}", color=color)

    elif args.reset_props:
        props.reset()
        interface.print("Your properties have been set back to the defaults.")

    elif args.history:
        history = search_history.get_history()

        idx = 0
        for idx, item in enumerate(history, start=1):
            interface.print(f"{idx}. {item}")

        if idx:
            interface.print(f"\n{idx} history items shown.")
        else:
            interface.print("There are no history items to show.")

    elif args.clear_history:
        search_history.clear()
        interface.print("Your search history has been cleared.")

    elif args.search:
        engine = DuckDuckGo()
        results = engine.search(args.search, limit=args.limit or None)
        interface.update(results)
