from urllib import parse
from collections.abc import Mapping


class URL:
    def __init__(self, domain: str, path: str, query: dict):
        if not isinstance(query, Mapping) or query is None:
            query = {}

        self.__domain = parse.urlparse(domain)
        self.__query = parse.urlencode(query)
        self.__path = path

    def get_url(self) -> str:
        return (self
                .__domain
                ._replace(path=self.__path, query=self.__query)
                .geturl()
                .lower()
                )
