from parser import Parser


class App:
    def __init__(self):
        self.__parser = Parser()

    def run(self):
        data = self.__parser.data
        print(len(data), data)
