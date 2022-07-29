from urllib import parse
from collections.abc import Mapping


class URL:
    def __init__(self, *, domain: str, path: str, query: dict[str, str] = None):
        if not isinstance(query, Mapping) or query is None:
            query = {}
        if not (domain.startswith('https://') or (domain.startswith('http://'))):
            raise TypeError('A domain must contain a protocol.')
        query = {key.lower(): value.lower() for key, value in query.items()}
        self.__domain = parse.urlparse(domain)
        self.__query = query
        self.__path = path

    def __str__(self):
        return (self
                .__domain
                ._replace(path=self.__path, query=parse.urlencode(self.__query))
                .geturl()
                .lower()
                )

    @property
    def domain(self) -> str:
        return self.__domain.geturl()

    @domain.setter
    def domain(self, new_domain: str) -> None:
        self.__domain = parse.urlparse(new_domain)

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, new_path: str) -> None:
        self.__path = new_path

    @property
    def query(self) -> dict[str, str]:
        return self.__query

    @query.setter
    def query(self, new_query: dict[str, str]) -> None:
        self.__query = new_query
