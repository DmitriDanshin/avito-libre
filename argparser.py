import argparse


class ArgParser:
    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__add_arguments()

    def __add_arguments(self):
        self.__parser.add_argument("--csv", action='store_true')
        self.__parser.add_argument("--xlsx", action='store_true')
        self.__parser.add_argument("--xml", action='store_true')
        self.__parser.add_argument("--json", action='store_true')
        self.__parser.add_argument("--clear", action="store_true")

    @property
    def formats_to_save(self) -> dict[str, bool]:
        return vars(self.__parser.parse_args())
