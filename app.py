from logger import app_logger
from parser import Parser
from writer import Writer


class App:
    def __init__(self):
        app_logger.info("App initialized successfully.")

    @staticmethod
    def parse(args: dict[str, bool], product_name: str) -> list[str] | None:
        writer = Writer(product_name)
        if args.get("clear", None):
            writer.clear()
            return

        data = Parser(product_name).data

        filenames = []

        if args.get("csv", None):
            filenames.append(writer.save_csv(data))
        if args.get("xlsx", None):
            filenames.append(writer.save_xlsx(data))
        if args.get("xml", None):
            filenames.append(writer.save_xml(data))
        if args.get("json", None):
            filenames.append(writer.save_json(data))

        return filenames
