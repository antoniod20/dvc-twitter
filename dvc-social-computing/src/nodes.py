import json
import os
from networkx.readwrite import json_graph


def read_json_file():
    with open(os.path.join('data', 'output', 'graph.json')) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


os.makedirs(os.path.join('data', 'nodes'), exist_ok=True)

TW = read_json_file()

output_graph = json.dump(json.dumps(list(TW.nodes())), open(os.path.join('data', 'nodes', 'nodes.json'), 'w+'))
