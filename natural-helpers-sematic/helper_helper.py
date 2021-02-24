def get_neighbors_in(helpers, at_graph):
    return_vals = set()
    for n in helpers.nodes():
        return_vals |= set(at_graph.neighbors(n))
    return_vals -= set(helpers.nodes())
    return return_vals
