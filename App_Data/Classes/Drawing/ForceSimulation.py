from ..Nodes.Node import Node
from ..Constructor.TreeBuilder import TreeBuilder
from ...Modules import math, tk

class ForceSimulation():
    def __init__(self, tree: TreeBuilder):
        self.repusion = 10000
        self.attaction = 10
        self.tree = tree
        self.node_positions:dict = {}
        self.interations = 10

    def iterate(self, edges:list[list[str]], window:tk.Tk):
        for _ in range(self.interations):
            self.apply_force(edges)
            window.update()

    def apply_repulsion(self, delta_pos:dict):
        for node1 in self.tree.nodes.values():
            for node2 in self.tree.nodes.values():
                if node1 == node2:
                    continue
                if node1 not in self.node_positions or node2 not in self.node_positions:
                    continue
                dx = self.node_positions[node1.get_name()][0] - self.node_positions[node2.get_name()][0]
                dy = self.node_positions[node1.get_name()][1] - self.node_positions[node2.get_name()][1]
                distance_sqrd = dx**2 + dy**2 
                force = self.repusion / distance_sqrd
                distance = math.sqrt(distance_sqrd) or 0.1
                delta_pos[node1.get_name()][0] += (dx / distance) * force
                delta_pos[node1.get_name()][1] += (dy / distance) * force 
        return delta_pos

    def apply_attraction(self, delta_pos:dict, edges:list[list[str]]):
        for node1_name, node2_name in edges:
            node1 = self.tree.nodes.get(node1_name)
            node2 = self.tree.nodes.get(node2_name)
            if not node1 or not node2:
                continue
            if not self.node_positions.get(node1) or not self.node_positions.get(node2):
                continue
            print(node1, node2)
            dx = self.node_positions[node1.get_name()][0] - self.node_positions[node2.get_name()][0]
            dy = self.node_positions[node1.get_name()][1] - self.node_positions[node2.get_name()][1]
            distance_sqrd = dx**2 + dy**2 
            force = self.attaction / distance_sqrd
            distance = math.sqrt(distance_sqrd) or 0.1
            delta_pos[node1_name][0] += (dx / distance) * force
            delta_pos[node1_name][1] += (dy / distance) * force
            delta_pos[node2_name][0] -= (dx / distance) * force
            delta_pos[node2_name][1] -= (dy / distance) * force
        return delta_pos

    def apply_force(self, edges:list[list[str]]):
        delta_pos = {name: [0,0] for name in self.tree.nodes.keys()}
        
        delta_pos = self.apply_repulsion(delta_pos)

        delta_pos = self.apply_attraction(delta_pos, edges)

        for node_name in self.tree.nodes.keys():
            if node_name not in self.node_positions.keys():
                continue
            dx, dy = delta_pos[node_name][0], delta_pos[node_name][1]
            if "1000" in node_name:
                print("+++" + node_name.upper() + "+++")
                print(dx, dy)
                print(self.node_positions[node_name][0], self.node_positions[node_name][1])
            self.node_positions[node_name][0] += dx
            self.node_positions[node_name][1] += dy
            if "1000" in node_name:
                print(self.node_positions[node_name][0], self.node_positions[node_name][1])
                print("\n")


