from .models import Node
from heapq import heappop, heappushpop


def calculate_path(node_from, node_to):
    visited = {node_from}
    dist = {node_from: 0}
    last = {}
    queue = [node_from]
    while queue:
        current = heappop(queue)
        visited.remove(current)
        node = Node.query.filter_by(id=current).first()
        for i in node.connected:
            if (i not in dist) or (dist[i] > dist[current]+1):
                dist[i] = dist[current] + 1
                last[i] = current
                if i not in visited:
                    visited.add(i)
                    heappushpop(queue, i)
    if node_to not in dist:
        raise ValueError()  # not connected
    path = [node_to]
    while node_to != node_from:
        path.append(last[node_to])
        node_to = last[node_to]
    path.reverse()
    return path
