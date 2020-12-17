import os
import json

os.makedirs(os.path.join('data', 'count'), exist_ok=True)

length = len(os.path.join('data', 'nodes', 'nodes.json'))

final = "Nodes are: " + str(length)
print(final)

output_graph = json.dump(json.dumps(final), open(os.path.join('data', 'count', 'count.json'), 'w+'))
