from pathlib import Path


class ScriptHandler:
    @staticmethod
    def read(script_path: Path) -> str:
        # todo 1. Разобраться с объектом Path
        # todo 2. Перенести весь текст скриптов в файлы и подключить их через этот класс
        # todo 3. Написать пару тестов для ScriptHandler:
        #  1. несуществующий файл
        #  2. существующий файл должен нормально открываться и возвращать текст
        #  io https://docs.python.org/3/library/io.html
        #  3. Файл должен иметь расширение .js (Path!!!)
        with open(script_path, "r") as script:
            return script.read()
