from logger import app_logger
from parser import Parser
from writer import Writer


class App:
    def __init__(self):
        app_logger.info("App initialized successfully.")

    @staticmethod
    def run(args: dict[str, bool]) -> None:

        if args["clear"]:
            Writer.clear()
            return None

        data = Parser().data

        if args["csv"]:
            Writer.save_csv(data)
        if args["xlsx"]:
            Writer.save_xlsx(data)
        if args["xml"]:
            Writer.save_xml(data)
        if args["json"]:
            Writer.save_json(data)
