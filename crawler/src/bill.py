import dataclasses
import datetime

from deliveration_status import DeliverationStatus


@dataclasses.dataclass(frozen=True)
class Bill:
    diet_no: str
    bill_type: str
    submit_diet_no: int
    submit_bill_no: int
    bill_subject: str
    status: DeliverationStatus
    submit_person: str
    submit_parties: str
    representatives_accept_date: datetime.datetime
    representatives_finish_date: datetime.datetime
    representatives_deliveration_result: str
    councilors_accept_date: datetime.datetime
    councilors_finish_date: datetime.datetime
    councilors_deliveration_result: str
    promulgation_date: datetime.datetime
    body_link: str

    @classmethod
    def from_dict(cls, d: dict):
        return Bill(
            d.get('diet_no'),
            d.get('bill_type'),
            d.get('submit_diet_no'),
            d.get('submit_bill_no'),
            d.get('bill_subject'),
            d.get('status'),
            d.get('submit_person'),
            d.get('submit_parties'),
            d.get('representatives_accept_date'),
            d.get('representatives_finish_date'),
            d.get('representatives_deliveration_result'),
            d.get('councilors_accept_date'),
            d.get('councilors_finish_date'),
            d.get('councilors_deliveration_result'),
            d.get('promulgation_date'),
            d.get('body_link'),
        )
