from parser import Parser


class App:
    def __init__(self):
        self.__parser = Parser()

    def run(self):
        print(self.__parser)
