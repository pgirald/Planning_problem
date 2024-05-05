from typing import Callable
from networkx import Graph


class Job:
    name: str
    income: float
    start: float
    end: float

    def __init__(self, income: float, start: float, end: float, name: str = ""):
        self.name = name
        self.income = income
        self.start = start
        self.end = end
        Job.overlapsWith = overlapsWith

    def __str__(self):
        return (
            self.name
            + " : "
            + str(self.income)
            + "    "
            + str(self.start)
            + "-"
            + str(self.end)
        )


def overlapsWith(self: Job, job: Job) -> bool:
    return (self.start >= job.start and self.start <= job.end) or (
        (self.end >= job.start and self.end <= job.end)
    )


def graph2job(graph: Graph) -> Job:
    pass
