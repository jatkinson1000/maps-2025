"""
Day 8: Urban - Get OSM data.

Using OSMnx - OpenStreetMap with NetworkX
"""

import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

ox.settings.bidirectional_network_types += "bike"
ox.settings.bidirectional_network_types += "drive"

# Get bidirected digraph (loops and directed edges)
G_bike = ox.graph.graph_from_place("Cambridge, UK", network_type="bike")
G_car = ox.graph.graph_from_place("Cambridge, UK", network_type="drive")

for i, network in enumerate([G_bike, G_car]):
    # # Convert to undirected MultiGraph (loops and parallel edges)
    # M = ox.convert.to_undirected(network)
    # fig, ax = ox.plot.plot_graph(M)

    # # ???
    # D = ox.convert.to_digraph(G)

    # # Convert to node and edge GeoPandas GeoDataFrame
    # gdf_nodes, gdf_edges = ox.convert.graph_to_gdfs(network)
    # print(gdf_nodes.head())
    # print(gdf_edges.head())

    # # Convert dataframes to NetworkX graph
    # G2 = ox.convert.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)

    # Get some basic stats
    network_proj = ox.projection.project_graph(network)
    nodes_proj = ox.convert.graph_to_gdfs(network_proj, edges=False)
    graph_area_m = nodes_proj.union_all().convex_hull.area
    print(f"Area in km^2: {graph_area_m / 1e6}")

    # ox.stats.basic_stats(nodes_proj, area=graph_area_m, clean_int_tol=15)

    # convert to line graph so edges become nodes and vice versa and
    # calculate centrality - how close a node is to all other nodes
    edge_centrality = nx.closeness_centrality(nx.line_graph(network))
    nx.set_edge_attributes(network, edge_centrality, "edge_centrality")

    # color edges in original graph with closeness centralities from line graph
    ec = ox.plot.get_edge_colors_by_attr(network, "edge_centrality", cmap="inferno")
    network_type = "bike" if i == 0 else "car"
    fig, ax = ox.plot.plot_graph(
        network,
        edge_color=ec,
        edge_linewidth=2,
        node_size=0,
        show=False,
        close=False,
        # save=True,
        # filepath=f"Cambridge_{network_type}.png",
    )
    ax.set_title(f"Cambridge UK {network_type} network centrality")
    plt.savefig(f"Cambridge_{network_type}.png", dpi=300)
    plt.close()
