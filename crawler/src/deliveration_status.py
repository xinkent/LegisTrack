from enum import Enum


class DeliverationStatus(Enum):
    DELIVERATION_IN_REPRESENTATIVE = "衆議院で審議中"
    DELIVERATION_IN_COUNCILOR = "参議院で審議中"
    ESTABLISHED = "成立"

    @classmethod
    def value_of(cls, target_value):
        for e in DeliverationStatus:
            if e.value == target_value:
                return e
        raise ValueError("{}は審議ステータス内に想定されていません。".format(target_value))
