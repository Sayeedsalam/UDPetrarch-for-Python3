# from google.cloud import translate_v3beta1 as translate
# client = translate.TranslationServiceClient()
#
# project_id = "myprojectr"
# text = 'Text you wish to translate'
# location = 'global'
#
# parent = client.location_path(project_id, location)
#
# response = client.translate_text(
#     parent=parent,
#     contents=[text],
#     mime_type='text/plain',  # mime types: text/plain, text/html
#     source_language_code='en-US',
#     target_language_code='sr-Latn')
#
# for translation in response.translations:
#     print('Translated Text: {}'.format(translation))

import networkx as nx
from  networkx.algorithms.coloring import greedy_coloring

graph = nx.Graph()

def build_graph_from_file(file="graph.txt"):
    file = open(file, "r")

    lines = file.readlines()

    num_vertices = int(lines[0])

    for i in range(0, num_vertices):
        graph.add_node(i)

    for i in range(1, len(lines)):
        v1, v2 = lines[i].split()

        graph.add_edge(int(v1), int(v2))
    print "Original Graph Edges count: ", str(len(graph.edges()))

    #extending the original graph
    augmented_graph = nx.Graph()
    for edge in graph.edges():
        augmented_graph.add_edge(edge[0], edge[1])

    for node in graph.nodes():
        neighbours = graph.neighbors(node)
        for neighbour in neighbours:
            n_neighbours = graph.neighbors(neighbour)
            for n_neighbour in n_neighbours:
                if not graph.has_edge(node, n_neighbour):
                    augmented_graph.add_edge(node, n_neighbour)

    print "Augmented Graph Edges count: ", str(len(augmented_graph.edges()))
    return augmented_graph



g = build_graph_from_file() #buiding an augmented graph

node_colors = greedy_coloring.greedy_color(g) #running first order coloring algorithm

print "Number of Colors required: ", str(len(set(node_colors.values())))

print node_colors
