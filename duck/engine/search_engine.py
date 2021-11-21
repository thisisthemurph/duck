import requests
from bs4 import BeautifulSoup
from typing import Generator

from duck.engine.search_result import SearchResult
from duck.history.history import History


class DuckDuckGo:
    """A representation of the DuckDuckGo search engine"""

    def __init__(self):
        """
        Parameters:
            base_url (str): the base URL used by the search enging to initiate searches
        """
        self.base_url = "https://html.duckduckgo.com/html?q="
        self.session = self.__build_session()

    def __build_url(self, query: str) -> str:
        """Combines the base_url and the search query."""
        query = "%20".join(query)
        return f"{self.base_url}{query}"

    def __build_session(self) -> requests.Session:
        """Creates and returned a new requests.Session."""
        session = requests.Session()
        session.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
            }
        )

        return session

    def __parse(self, html: str, limit: int) -> Generator[SearchResult, None, None]:
        """Parses the HTML, returning a generator of SearchResult objects."""
        soup = BeautifulSoup(html, "html.parser")
        results_ele = soup.find("div", "results")

        yielded_results = 0
        for result in results_ele.find_all("div", "result"):
            if yielded_results == limit:
                break

            if "result--ad" in result.get("class", []):
                continue

            url = result.find("a", "result__url")["href"]
            title = result.find("a", "result__a").text
            snippet = result.find("a", "result__snippet").text

            yielded_results += 1
            yield SearchResult(url, title, snippet)

    def search(self, query: str, limit: int = 5):
        """Perform a search using DuckDockGo"""
        search_history = History()
        search_history.add(" ".join(query))

        url = self.__build_url(query)
        result = self.session.get(url)
        return self.__parse(result.text, limit=limit)
