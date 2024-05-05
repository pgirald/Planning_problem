from networkx import Graph


def graphsEqual(self: Graph, other: Graph) -> bool:
    """Returns a boolean value indicating if the graphs given
    as parameters are equal based on their structure"""
    if (
        self.number_of_nodes() != other.number_of_nodes()
        or self.number_of_edges() != other.number_of_edges()
    ):
        return False

    if set(self.nodes) != set(other.nodes) or set(self.edges) != set(other.edges):
        return False

    return True


Graph.__eq__ = graphsEqual
