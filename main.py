from app import App
from argparser import ArgParser

if __name__ == '__main__':
    app = App()
    arguments_parser = ArgParser()
    app.run(arguments_parser.formats_to_save)
