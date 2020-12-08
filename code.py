import copy
import pylab
import community as groups
import networkx as graphx
import sys
import matplotlib.pyplot as graph

pylab.show()


# to remove edges from the graph
def edgesDelete(Chart):
    values = graphx.edge_betweenness_centrality(Chart)
    delete = []
    high_edge_value = values[max(values, key=values.get)]
    for i, j in values.items():
        if j == high_edge_value:
            delete.append(i)

    Chart.remove_edges_from(delete)
    subgroups = list(Chart.subgraph(groups) for groups in graphx.connected_components(Chart))

    x = {}
    register = 0
    for subgroup in subgroups:
        register += 1
        for actor in subgroup:
            x[actor] = register

    if Chart.number_of_edges() == 0:
        return [list(Chart.subgraph(groups) for groups in graphx.connected_components(Chart)), 0,
                Chart]

    graph_mdl = groups.modularity(x, Chart)
    return [list(Chart.subgraph(groups) for groups in graphx.connected_components(Chart)), graph_mdl, Chart]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("check parameters and try again")
        exit(-1)

    Chart = graphx.read_edgelist(sys.argv[1])
    final_groups = []
    duplicate_chart = copy.deepcopy(Chart)
    i = {}
    for actor in Chart:
        i[actor] = 0

    first_mdl = groups.modularity(i, Chart)
    final_groups.append([i, first_mdl, Chart])

    while Chart.number_of_edges() > 0:
        inbetween_charts = edgesDelete(Chart)
        final_groups.append(inbetween_charts)
        Chart = inbetween_charts[-1]

    for grp in final_groups:
        # print ("modularity",grp[1])
        if grp[1] > first_mdl:
            xyz = grp[0]
            final_grps = []
            modularity = grp[1]

            for chart in grp[0]:
                final_grps.append(sorted([int(node) for node in chart]))

    for groups in final_grps:
        print(groups)

    k = {}
    register = 0

    for chart in xyz:
        for actor in chart:
            k[actor] = register
        register += 1

    layout = graphx.spring_layout(duplicate_chart)
    clrs = ["black", "pink", "indigo", "orange", "yellow", "green", "red", "grey", "cyan", "brown"]
    for i in range(len(xyz)):
        chart = xyz[i]
        nodelist = [actor for actor in chart]
        graphx.draw_networkx_nodes(duplicate_chart, layout, nodelist=nodelist, node_color=clrs[i % 10], node_size=200, alpha=0.8)

    graphx.draw_networkx_edges(duplicate_chart, layout)
    graphx.draw_networkx_labels(duplicate_chart, layout, font_size=10)
    graph.axis('off')
    graph.savefig(sys.argv[2])

