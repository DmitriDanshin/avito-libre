import re
from datetime import datetime


class DateHandler:
    months_locales = {
        'января': 'January',
        'февраля': 'February',
        'марта': 'March',
        'апреля': 'April',
        'мая': 'May',
        'июня': 'June',
        'июля': 'July',
        'августа': 'August',
        'сентября': 'September',
        'октября': 'October',
        'ноября': 'November',
        'декабря': 'December'
    }

    @classmethod
    def reformat_date(cls, date_string: str) -> datetime:
        date_string = re.compile(r'[А-Яа-я]+').sub(
            lambda match: cls.months_locales[match.group()]
            if match.group() in cls.months_locales else '',
            date_string
        )
        date = datetime.strptime(date_string, "%d %B %H:%M")

        return date.replace(year=datetime.now().year)
