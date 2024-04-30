import datetime


class DateUtil:

    # 和暦情報
    ERA_DICT = {
        '令和': 2019,
        '平成': 1989,
        '昭和': 1926,
    }

    # 和暦からdatetimeへ変換(「令和6年4月5日」 → 「2024/4/5」)
    @classmethod
    def transform_to_western_year(self, wareki: str, year: int, month: int, day: int) -> datetime.datetime:
        western_year = DateUtil.ERA_DICT[wareki]
        return datetime.datetime(western_year + year - 1, month, day)
