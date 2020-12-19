import networkx as nx
import matplotlib.pyplot as plt
import os
import json
import sys
from networkx.readwrite import json_graph


def read_json_file(path):
    with open(path) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython egonetwork.py data-file\n")
    sys.exit(1)

os.makedirs(os.path.join('data', 'egonetwork'), exist_ok=True)

TW = read_json_file(sys.argv[1])

sky_node = list(TW.nodes)[1]  # SKY TG24
ego_network = nx.ego_graph(TW, sky_node, 2, True, True)

labels = {}
for node in TW.nodes():
    if node == "SkyTG24":
        # set the node name as the key and the label as its value
        labels[node] = node

# ego network graph
plt.figure(figsize=(20,20))
ax = plt.gca()
ax.set_title('Ego network graph')
pos = nx.spring_layout(ego_network)
nx.draw(ego_network, pos, node_color='b', node_size=100, with_labels=False)
nx.draw_networkx_nodes(ego_network, pos, nodelist=[sky_node], node_size=200, node_color='r')

# label of SkyTG24 node
nx.draw_networkx_labels(ego_network, pos, labels, font_size=20, font_color="r", font_family="sans-serif", verticalalignment="bottom")

plt.savefig(os.path.join('data', 'egonetwork', 'egonetwork.png'), dpi=300, bbox_inches='tight')
json.dump(json_graph.node_link_data(TW), open(os.path.join('data', 'egonetwork', 'egonetwork.json'), 'w+'))
