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

    @classmethod
    def clear(cls):
        for file in os.listdir(cls.__result_folder):
            file_path = os.path.join(cls.__result_folder, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        writer_logger.info("Successfully clear a folder results.")

    @staticmethod
    def __get_filename(extension: Literal['json', 'xml', 'csv', 'xlsx'],
                       data: dict[str, dict[str, str | datetime]]) -> Path:
        return Path(
            f"search[{'_'.join(SEARCH.lower().split())}]_"
            f"len[{len(data)}]_"
            f"date[{datetime.now().strftime(FILENAME_TIME_FORMAT)}].{extension}"
        )

    @classmethod
    def __get_data_frame(cls, data: dict[str, dict[str, str | datetime]]) -> pd.DataFrame:
        return pd.DataFrame(data.values())

    @classmethod
    def save_json(cls, data: dict[str, dict[str, str | datetime]]):
        file_name = cls.__get_filename(extension='json', data=data)
        df = cls.__get_data_frame(data)
        df.to_json(cls.__result_folder / file_name, force_ascii=FORCE_ASCII)
        writer_logger.info("Successfully saved data as json format.")

    @classmethod
    def save_xml(cls, data: dict[str, dict[str, str | datetime]]):
        file_name = cls.__get_filename(extension='xml', data=data)
        df = cls.__get_data_frame(data)
        df.to_xml(cls.__result_folder / file_name, encoding=FILE_ENCODING)
        writer_logger.info("Successfully saved data as xml format.")

    @classmethod
    def save_csv(cls, data: dict[str, dict[str, str | datetime]]) -> None:
        file_name = cls.__get_filename(extension='csv', data=data)
        df = cls.__get_data_frame(data)
        df.to_csv(cls.__result_folder / file_name, CSV_DELIMITER, encoding=FILE_ENCODING)
        writer_logger.info("Successfully saved data as csv format.")

    @classmethod
    def save_xlsx(cls, data: dict[str, dict[str, str | datetime]]):
        file_name = cls.__get_filename(extension='xlsx', data=data)
        df = cls.__get_data_frame(data)
        df.to_excel(cls.__result_folder / file_name, encoding=FILE_ENCODING)
        writer_logger.info("Successfully saved data as xlsx format.")
