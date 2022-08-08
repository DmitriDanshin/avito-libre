import re
from datetime import datetime
from pathlib import Path
import os
import pandas as pd
from typing import Literal

from logger import writer_logger
from settings import (
    FILENAME_TIME_FORMAT, FILE_ENCODING,
    CSV_DELIMITER, FORCE_ASCII, SEARCH
)


class Writer:
    __result_folder: Path = Path("results")

    def __init__(self, product_name: str = SEARCH):
        self.__product_name = product_name

    def clear(self):
        for file in os.listdir(self.__result_folder):
            file_path = os.path.join(self.__result_folder, file)
            file_exists = os.path.isfile(file_path)

            product_name_in_file_name = (
                re
                .compile(rf"\[{self.__product_name}]")
                .search(str(file))
            )

            if file_exists and product_name_in_file_name:
                os.unlink(file_path)

        writer_logger.info("Successfully clear a folder results.")

    def __get_filename(self, extension: Literal['json', 'xml', 'csv', 'xlsx'],
                       data: dict[str, dict[str, str | datetime]]) -> Path:
        return Path(
            f"search[{'_'.join(self.__product_name.lower().split())}]_"
            f"len[{len(data)}]_"
            f"date[{datetime.now().strftime(FILENAME_TIME_FORMAT)}].{extension}"
        )

    @staticmethod
    def __get_data_frame(data: dict[str, dict[str, str | datetime]]) -> pd.DataFrame:
        return pd.DataFrame(data.values())

    def save_json(self, data: dict[str, dict[str, str | datetime]]) -> str:
        file_name = self.__get_filename(extension='json', data=data)
        df = self.__get_data_frame(data)
        df.to_json(self.__result_folder / file_name, force_ascii=FORCE_ASCII)
        writer_logger.info("Successfully saved data as json format.")
        return str(file_name)

    def save_xml(self, data: dict[str, dict[str, str | datetime]]) -> str:
        file_name = self.__get_filename(extension='xml', data=data)
        df = self.__get_data_frame(data)
        df.to_xml(self.__result_folder / file_name, encoding=FILE_ENCODING)
        writer_logger.info("Successfully saved data as xml format.")
        return str(file_name)

    def save_csv(self, data: dict[str, dict[str, str | datetime]]) -> str:
        self.clear()
        file_name = self.__get_filename(extension='csv', data=data)
        df = self.__get_data_frame(data)
        df.to_csv(self.__result_folder / file_name, CSV_DELIMITER, encoding=FILE_ENCODING)
        writer_logger.info("Successfully saved data as csv format.")
        return str(file_name)

    def save_xlsx(self, data: dict[str, dict[str, str | datetime]]) -> str:
        file_name = self.__get_filename(extension='xlsx', data=data)
        df = self.__get_data_frame(data)
        df.to_excel(self.__result_folder / file_name, encoding=FILE_ENCODING)
        writer_logger.info("Successfully saved data as xlsx format.")
        return str(file_name)
