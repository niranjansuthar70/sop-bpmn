# src/models.py
import uuid

class Node:
    def __init__(self, name, node_type="task"):
        self.id = f"node_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.type = node_type  # "start", "end", "task", "gateway"

class Edge:
    def __init__(self, source_id, target_id, label=None):
        self.id = f"flow_{uuid.uuid4().hex[:8]}"
        self.source = source_id
        self.target = target_id
        self.label = label  # e.g., "Yes" or "No"

class ProcessGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)
        return node

    def add_edge(self, source, target, label=None):
        edge = Edge(source.id, target.id, label)
        self.edges.append(edge)