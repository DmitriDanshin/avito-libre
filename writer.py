from datetime import datetime
from pathlib import Path

import pandas as pd


class Writer:
    def __init__(self):
        self.__result_folder = Path("results")

    # todo extension должен иметь тип Literal, состоящий из необходимых расширений
    # from typing import Literal
    # todo формат времени в константу
    # разделитель csv delimiter, encoding, force_ascii в константы

    # todo добавить в название файла поисковой запрос
    # поисковой запрос в нижний регистр, разделять слова нижним подчёркиванием
    # search[daewoo_matiz]_len[187]_date[2022-07-31-19h49m26s]
    def clear(self):
        pass

    def __get_filename(self, extension) -> Path:
        pass

    def save_json(self, data: dict[str, dict[str, str | datetime]]):
        file_name = Path(
            f"len[{len(data)}]_"
            f"date[{datetime.now().strftime('%Y-%m-%d-%Hh%Mm%Ss')}].json"
        )
        df = pd.DataFrame(data.values())
        df.to_json(self.__result_folder / file_name, force_ascii=False)

    def save_xml(self, data: dict[str, dict[str, str | datetime]]):
        file_name = Path(
            f"len[{len(data)}]_"
            f"date[{datetime.now().strftime('%Y-%m-%d-%Hh%Mm%Ss')}].xml"
        )
        df = pd.DataFrame(data.values())
        df.to_xml(self.__result_folder / file_name, encoding="utf-8")

    def save_csv(self, data: dict[str, dict[str, str | datetime]]) -> None:
        file_name = Path(
            f"len[{len(data)}]_"
            f"date[{datetime.now().strftime('%Y-%m-%d-%Hh%Mm%Ss')}].csv"
        )
        df = pd.DataFrame(data.values())
        df.to_csv(self.__result_folder / file_name, ",", encoding="utf-8")

    def save_xlsx(self, data: dict[str, dict[str, str | datetime]]):
        file_name = Path(
            f"len[{len(data)}]_"
            f"date[{datetime.now().strftime('%Y-%m-%d-%Hh%Mm%Ss')}].xlsx"
        )
        df = pd.DataFrame(data.values())
        df.to_excel(self.__result_folder / file_name, encoding="utf-8")
