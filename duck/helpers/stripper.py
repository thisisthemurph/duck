from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data: str):
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html: str) -> str:
    """
    Stript HTML tags from the given string.

    Parameters:
        html (str): a string containing HTML and text

    Returns:
        a string without the HTML tags
    """
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()
