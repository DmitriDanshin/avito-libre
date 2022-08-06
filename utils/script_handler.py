from pathlib import Path


class ScriptHandler:
    @staticmethod
    def read(script_path: Path) -> str:
        if script_path.suffix != '.js':
            raise ValueError('A file must have .js extension.')

        with open(script_path, "r") as script:
            return script.read()
