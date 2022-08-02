from parser import Parser
from writer import Writer


class App:
    def __init__(self):
        self.__writer = Writer()

    def run(self, args: dict[str, bool]) -> None:

        if args["clear"]:
            self.__writer.clear()
            return None

        data = Parser().data

        if args["csv"]:
            self.__writer.save_csv(data)
        if args["xlsx"]:
            self.__writer.save_xlsx(data)
        if args["xml"]:
            self.__writer.save_xml(data)
        if args["json"]:
            self.__writer.save_json(data)
