from pathlib import Path
from unittest import TestCase

from utils.script_handler import ScriptHandler


class TestScript(TestCase):

    def test_exist(self):
        with self.assertRaises(FileNotFoundError):
            ScriptHandler.read(Path('biba.js'))
        with self.assertRaises(FileNotFoundError):
            ScriptHandler.read(Path('get_date.js'))
        with self.assertRaises(FileNotFoundError):
            ScriptHandler.read(Path('scripts/get_date.js'))

    def test_correct(self):
        with self.assertRaises(ValueError):
            ScriptHandler.read(Path('boba'))
        with self.assertRaises(ValueError):
            ScriptHandler.read(Path('скрипты'))
        with self.assertRaises(ValueError):
            ScriptHandler.read(Path(''))

    def test_read_correct(self):
        self.assertEqual(
            "console.log('hello world')",
            ScriptHandler.read(Path('hello.js'))
        )

    def test_type(self):
        with self.assertRaises(TypeError):
            ScriptHandler.read(Path(12312))
        with self.assertRaises(TypeError):
            ScriptHandler.read(Path(['edit.js']))
        with self.assertRaises(TypeError):
            ScriptHandler.read(Path({'1': '12'}))
