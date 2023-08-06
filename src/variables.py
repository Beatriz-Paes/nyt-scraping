import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
from RPA.Robocorp.WorkItems import WorkItems

load_dotenv("../.env")

SECTIONS = os.environ.get("SECTIONS")
MONTH_PERIOD = os.environ.get("MONTH_PERIOD")
PHRASE = os.environ.get("PHRASE")
NOTICE_TYPE = os.environ.get("NOTICE_TYPE")
ENV = os.environ.get("ENV")


@dataclass
class Cfg:
    sections: List[str]
    month_period: int
    phrase: str
    notice_type: List[str]


def work_item_variables():
    work_itens = WorkItems()
    work_itens.get_input_work_item()

    variables = Cfg(
        sections=[s.strip() for s in work_itens.get_work_item_variable("SECTIONS").split(",")],
        month_period=work_itens.get_work_item_variable("MONTH_PERIOD"),
        phrase=work_itens.get_work_item_variable("PHRASE"),
        notice_type=[nt.strip() for nt in work_itens.get_work_item_variable("NOTICE_TYPE").split(",")],
    )
    return variables


def get_variables():
    if ENV == 'LOCAL':
        return Cfg(
            sections=[s.strip() for s in SECTIONS.split(",")],
            month_period=int(MONTH_PERIOD),
            phrase=PHRASE,
            notice_type=[nt.strip() for nt in NOTICE_TYPE.split(",")],
        )
    return work_item_variables()
