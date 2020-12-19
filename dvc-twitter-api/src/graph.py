import sys
import os
import pandas as pd
import json
import networkx as nx
from networkx.readwrite import json_graph

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython graph.py data-file\n")
    sys.exit(1)

os.makedirs(os.path.join('data', 'graph'), exist_ok=True)

input_path = sys.argv[1]
data = pd.read_csv(input_path, sep=',', names=['UserID','FollowerID'],header=0)

TW = nx.from_pandas_edgelist(data,'FollowerID','UserID',create_using=nx.DiGraph)

json.dump(json_graph.node_link_data(TW), open(os.path.join('data', 'graph', 'graph.json'), 'w+'))
