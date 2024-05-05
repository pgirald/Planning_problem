from enum import Enum
import networkx as nx
from numpy import full, stack
from Job import Job


class _ST(Enum):
    unset = 0
    active = 1
    unactive = 2
    discarded = 4


class _JobsCSP:
    _graph: nx.Graph
    _nodes: list[int]
    _nodesCount: int
    _next: int = 0

    def __init__(self, graph: nx.Graph):
        self._nodes = list(graph.nodes)
        for i in range(len(self._nodes)):
            graph.nodes[self._nodes[i]]["idx"] = i
        self._graph = graph
        self._nodesCount = len(self._nodes)

    def moveToNext(self) -> None:
        while (
            self._next < self._nodesCount and self._stateOf(self.nextNode) != _ST.unset
        ):
            self._next += 1

    @property
    def isEmpty(self) -> bool:
        return self._nodesCount == 0

    @property
    def nodesCount(self) -> int:
        return self._nodesCount

    @property
    def nextNode(self) -> int | None:
        if self._next >= self.nodesCount:
            return None
        return self._nodes[self._next]

    def jobOf(self, node: int) -> Job:
        return self._graph.nodes[node]["job"]

    def neighborsOf(self, node: int) -> list[int]:
        return self._graph.neighbors(node)

    @property
    def unsetNodes(self) -> list[int]:
        return [
            node
            for node, data in self._graph.nodes(data=True)
            if data["st"] == _ST.unset
        ]

    @property
    def unactiveNodes(self) -> list[int]:
        return [
            node
            for node, data in self._graph.nodes(data=True)
            if data["st"] == _ST.unactive
        ]

    def _indexOf(self, node: int) -> int:
        return self._graph.nodes[node]["idx"]

    def _stateOf(self, node: int) -> _ST:
        return self._graph.nodes[node]["st"]

    def _setStateOf(self, node: int, state: _ST) -> None:
        def setStateOf(node: int, to: _ST):
            self._graph.nodes[node]["st"] = to

        previous = self._stateOf(node)
        if state == _ST.discarded:
            return
        if previous == state:
            return

        setStateOf(node, to=state)

        if previous == _ST.active:
            neighbors = list(self._graph.neighbors(node))
            for neighbor in neighbors:
                setStateOf(neighbor, to=_ST.unset)
            if self._indexOf(neighbors[0]) < self._next:
                self._next = self._indexOf(neighbors[0])

        if state == _ST.unset:
            if self._indexOf(node) < self._next:
                self._next = self._indexOf(node)
            return

        if state == _ST.active:
            neighbors = list(self._graph.neighbors(node))
            for neighbor in neighbors:
                setStateOf(neighbor, to=_ST.discarded)

        self.moveToNext()

    def activate(self, node: int) -> None:
        self._ensureNodeIsValid(node)
        self._setStateOf(node, _ST.active)

    def deactivate(self, node: int) -> None:
        self._ensureNodeIsValid(node)
        self._setStateOf(node, _ST.unactive)

    def unset(self, node: int) -> None:
        self._ensureNodeIsValid(node)
        self._setStateOf(node, _ST.unset)

    def _ensureNodeIsValid(self, node: int) -> None:
        if node not in self._nodes:
            raise ValueError("The specified node does not exist")


def _modelCSP(jobs: list[Job]) -> nx.Graph:
    """
    Returns a model of a constraint satisfaction problem based
    on how multiple jobs overlap
    """
    rawProblem = nx.Graph()
    for i in range(len(jobs)):
        rawProblem.add_node(i, job=jobs[i], st=_ST.unset)
    for i in range(len(jobs) - 1):
        for j in range(i + 1, len(jobs)):
            if jobs[i].overlapsWith(jobs[j]):
                rawProblem.add_edge(i, j)
    return rawProblem


JOBS = "jobs"
INCOME = "income"


# def _solve(csp: _JobsCSP) -> dict:
#     solution = {JOBS: [], INCOME: 0}
#     if csp.isEmpty:
#         return solution
#     if csp.nodesCount == 1:
#         job = csp.jobOf(csp.nextNode)
#         return {JOBS: [job], INCOME: job.income}
#     totalIncome = 0
#     ip = 0
#     current = csp.nextNode
#     jobsTaken: list[Job] = []
#     stack: list[tuple[int, int]] = []

#     while True:
#         match ip:
#             case 0:
#                 if current == None:
#                     if totalIncome > solution[INCOME]:
#                         solution[JOBS] = jobsTaken.copy()
#                         solution[INCOME] = totalIncome
#                     (current, ip) = stack.pop()
#                     break
#                 for node in csp.unactiveNodes:
#                     if len(set(csp.neighborsOf(node)) & set(csp.unsetNodes)) == 0:
#                         (current, ip) = stack.pop()
#                         break
#                 csp.activate(current)
#                 stack.append((current, 1))
#                 jobsTaken.append(csp.jobOf(current))
#                 totalIncome += csp.jobOf(current).income
#                 current = csp.nextNode
#             case 1:
#                 jobsTaken.remove(current)
#                 totalIncome -= csp.jobOf(current).income
#                 csp.deactivate(current)
#                 stack.append((current, 2))
#                 current = csp.nextNode
#                 ip = 0
#             case 2:
#                 csp.unset(current)
#                 (current, ip) = stack.pop()
#         if len(stack) == 0:
#             break
#     return solution


def _solve(csp: nx.Graph, vars: list[int], jobs: list[Job] = [], income: int = 0):
    if len(vars) == 0:
        return (jobs, income)

    solution1 = _solve(
        csp,
        removeNeighbors(csp, vars),
        jobs + [jobOf(csp, vars[0])],
        income + jobOf(csp, vars[0]).income,
    )

    solution2 = _solve(csp, removeAt(0, _from=vars), jobs, income)

    if solution1[1] >= solution2[1]:
        return solution1

    return solution2


def jobOf(csp: nx.Graph, node: int) -> Job:
    return csp.nodes[node]["job"]


def removeNeighbors(csp: nx.Graph, vars: list):
    newVars = [var for var in vars if var not in csp.neighbors(vars[0])]
    newVars.remove(vars[0])
    return newVars


def removeAt(idx: int, _from: list):
    newVars = _from.copy()
    newVars.remove(_from[idx])
    return newVars


def removeAll(elements: list, _from: list):
    for element in elements:
        _from.remove(element)


# def solveAll(jobs: list[Job]) -> dict:
#     fullCSP = _modelCSP(jobs)
#     solution = {JOBS: [], INCOME: 0}
#     connectedComponents: list = nx.connected_components(fullCSP)
#     for connectedNodes in connectedComponents:
#         partialSolution = _solve(_JobsCSP(fullCSP.subgraph(connectedNodes)))
#         solution[JOBS].extend(partialSolution[JOBS])
#         solution[INCOME] += partialSolution[INCOME]
#     return solution


def solveAll(jobs: list[Job]) -> dict:
    fullCSP = _modelCSP(jobs)
    solution = {JOBS: [], INCOME: 0}
    connectedComponents: list = nx.connected_components(fullCSP)
    for connectedNodes in connectedComponents:
        csp = fullCSP.subgraph(connectedNodes)
        partialSolution = _solve(csp, list(csp.nodes))
        solution[JOBS].extend(partialSolution[0])
        solution[INCOME] += partialSolution[1]
    return solution
