from urllib import parse
from collections.abc import Mapping


class URL:
    def __init__(self, domain: str, path: str, query: dict[str, str]):
        if not isinstance(query, Mapping) or query is None:
            query = {}

        self.__domain = parse.urlparse(domain)
        self.__query = parse.urlencode(query)
        self.__path = path

    def __str__(self):
        return (self
                .__domain
                ._replace(path=self.__path, query=self.__query)
                .geturl()
                .lower()
                )

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, new_domain: str):
        self.__domain = parse.urlparse(new_domain)
