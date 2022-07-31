import settings
from parser import Parser
from writer import Writer


class App:
    def __init__(self):
        self.__parser = Parser()
        self.__writer = Writer()

    def run(self):
        data = self.__parser.data
        self.__writer.save_csv(data)
        self.__writer.save_xlsx(data)
        self.__writer.save_xml(data)
        self.__writer.save_json(data)

        # todo сделать метод clear, который очищает папку results
        # self.__writer.clear()
        while settings.DEBUG:
            ...
