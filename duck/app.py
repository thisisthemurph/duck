import argparse

from duck.helpers.color import Color
from duck.properties.props import Properties
from duck.engine.search_engine import DuckDuckGo
from duck.interface.terminal import TerminalInterface


def run(args: argparse.Namespace) -> None:
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

    elif args.search:
        engine = DuckDuckGo()
        results = engine.search(args.search, limit=args.limit or None)
        interface.update(results)
