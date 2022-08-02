from datetime import datetime
from pathlib import Path
import os
import pandas as pd
from typing import Literal
from settings import (
    FILENAME_TIME_FORMAT, FILE_ENCODING,
    CSV_DELIMITER, FORCE_ASCII, SEARCH
)


class Writer:
    def __init__(self):
        self.__result_folder = Path("results")

    def clear(self):
        for file in os.listdir(self.__result_folder):
            file_path = os.path.join(self.__result_folder, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    @staticmethod
    def __get_filename(extension: Literal['json', 'xml', 'csv', 'xlsx'],
                       data: dict[str, dict[str, str | datetime]]) -> Path:
        return Path(
            f"search[{'_'.join(SEARCH.lower().split())}]_"
            f"len[{len(data)}]_"
            f"date[{datetime.now().strftime(FILENAME_TIME_FORMAT)}].{extension}"
        )

    @staticmethod
    def __get_data_frame(data: dict[str, dict[str, str | datetime]]) -> pd.DataFrame:
        return pd.DataFrame(data.values())

    def save_json(self, data: dict[str, dict[str, str | datetime]]):
        file_name = self.__get_filename(extension='json', data=data)
        df = self.__get_data_frame(data)
        df.to_json(self.__result_folder / file_name, force_ascii=FORCE_ASCII)

    def save_xml(self, data: dict[str, dict[str, str | datetime]]):
        file_name = self.__get_filename(extension='xml', data=data)
        df = self.__get_data_frame(data)
        df.to_xml(self.__result_folder / file_name, encoding=FILE_ENCODING)

    def save_csv(self, data: dict[str, dict[str, str | datetime]]) -> None:
        file_name = self.__get_filename(extension='csv', data=data)
        df = self.__get_data_frame(data)
        df.to_csv(self.__result_folder / file_name, CSV_DELIMITER, encoding=FILE_ENCODING)

    def save_xlsx(self, data: dict[str, dict[str, str | datetime]]):
        file_name = self.__get_filename(extension='xlsx', data=data)
        df = self.__get_data_frame(data)
        df.to_excel(self.__result_folder / file_name, encoding=FILE_ENCODING)
