import unittest
from parameterized import parameterized
from networkx import Graph, connected_components
import Graph_extension
from Job_CSP import _modelCSP, solveAll
from Job import Job

g1 = Graph()
g1.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
g1.add_edges_from([(1, 3), (4, 5), (2, 2), (7, 6), (6, 4)])

g2 = Graph()
g2.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
g2.add_edges_from([(1, 3), (4, 5), (2, 2), (7, 6), (6, 4)])

g3 = Graph()
g3.add_nodes_from([1, 2, 3, 4])
g3.add_edges_from([(1, 3), (4, 5), (2, 2), (6, 4)])

g4 = Graph()
g4.add_nodes_from([1, 2, 3, 4])
g4.add_edges_from([(1, 3), (4, 5), (2, 2), (4, 6)])

g5 = Graph()
g5.add_nodes_from([1, 2, 3, 4])
g5.add_edges_from([(1, 3), (4, 5), (2, 2), (2, 5)])

g6 = Graph()
g6.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
g6.add_edges_from(
    [
        (1, 2),
        (2, 3),
        (3, 5),
        (1, 3),
        (3, 4),
        (4, 5),
        (1, 7),
        (4, 7),
        (8, 9),
        (9, 10),
        (8, 10),
        (8, 11),
        (11, 10),
        (12, 13),
        (13, 14),
        (12, 14),
        (15, 14),
        (14, 16),
        (15, 16),
    ]
)


class GraphTesting(unittest.TestCase):
    @parameterized.expand(
        [(g3, g4, True), (g1, g2, True), (g1, g3, False), (g3, g5, False)]
    )
    def test_graph_equal(self, a: Graph, b: Graph, expected: bool):
        self.assertEqual(a == b, expected)

    @parameterized.expand(
        [
            (g1,),
            (g2,),
            (g3,),
            (g4,),
            (g5,),
            (g6,),
        ]
    )
    def test_neighbors_order(self, graph: Graph):
        subGraphs: list[Graph] = [
            graph.subgraph(comps) for comps in connected_components(graph)
        ]
        for subGraph in subGraphs:
            for node in subGraph.nodes:
                n1 = list(subGraph.neighbors(node))
                n2 = list(graph.neighbors(node))
                for i in range(len(n1)):
                    self.assertEqual(n1[i], n2[i])


jobs1: list[Job] = [
    Job(name="Programmer", income=50, start=1, end=3),
    Job(name="Architect", income=60, start=3, end=6),
    Job(name="Tester", income=70, start=6, end=8),
    Job(name="Owner", income=40, start=4, end=7),
]

solution1 = [0, 2]

csp1 = Graph()
csp1.add_nodes_from(range(len(jobs1)))
csp1.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 3)])


jobs2: list[Job] = [
    Job(name="Job1", income=60, start=1, end=3),
    Job(name="Job2", income=20, start=4, end=6),
    Job(name="Job3", income=50, start=9, end=10),
    Job(name="Job4", income=70, start=2, end=3),
    Job(name="Job5", income=10, start=1, end=2),
    Job(name="Job6", income=10, start=5, end=8),
]

solution2 = [1, 2, 3]

jobs3: list[Job] = [
    Job(name="Job1", income=155, start=0, end=2),
    Job(name="Job2", income=142, start=1, end=2),
    Job(name="Job3", income=82, start=2, end=3),
    Job(name="Job4", income=113, start=4, end=5),
    Job(name="Job5", income=62, start=3, end=4),
    Job(name="Job6", income=44, start=5, end=5.5),
    Job(name="Job7", income=142, start=6, end=8),
    Job(name="Job8", income=58, start=6, end=7),
    Job(name="Job9", income=188, start=7, end=8),
    Job(name="Job10", income=54, start=8, end=9),
    Job(name="Job11", income=174, start=10, end=12),
    Job(name="Job12", income=75, start=11, end=12),
    Job(name="Job13", income=42, start=12, end=14),
    Job(name="Job14", income=192, start=13, end=14),
    Job(name="Job15", income=96, start=14, end=15),
]

solution3 = [0, 3, 8, 10, 13]

csp2 = Graph()
csp2.add_nodes_from(range(len(jobs1)))
csp2.add_edges_from(
    [
        (0, 3),
        (0, 4),
        (1, 5),
        (3, 4),
    ]
)

csp3 = Graph()
csp3.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
csp3.add_edges_from(
    [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 4),
        (3, 4),
        (3, 5),
        (6, 7),
        (6, 8),
        (6, 9),
        (7, 8),
        (8, 9),
        (10, 11),
        (10, 12),
        (11, 12),
        (12, 13),
        (12, 14),
        (13, 12),
    ]
)


class CsProblemGenTesting(unittest.TestCase):
    @parameterized.expand([(jobs1, csp1), (jobs2, csp2), (jobs3, csp3)])
    def test_CSP_Gen(self, jobs: list[Job], csp: Graph):
        self.assertTrue(_modelCSP(jobs) == csp)

    @parameterized.expand([(jobs1,), (jobs2,), (jobs3,)])
    def test_neighbors_asc_order(self, jobs: list[Job]):
        graph: Graph = _modelCSP(jobs)
        for node in graph.nodes:
            neighbors = list(graph.neighbors(node))
            for i in range(1, len(neighbors)):
                self.assertGreater(neighbors[i], neighbors[i - 1])

    @parameterized.expand([(jobs1, solution1), (jobs2, solution2), (jobs3, solution3)])
    def test_problem_solver(self, jobs: list[Job], expected: list[int]):
        solution1 = solveAll(jobs)["jobs"]
        solution2 = [jobs[i] for i in expected]
        self.assertTrue(set(solution1) == set(solution2))

    @parameterized.expand([(jobs1,), (jobs2,), (jobs3,)])
    def test_total_income_correct(self, jobs: list[Job]):
        expectedIncome = 0
        solution = solveAll(jobs)
        for job in solution["jobs"]:
            expectedIncome += job.income
        self.assertEqual(expectedIncome, solution["income"])


if __name__ == "__main__":
    unittest.main()
