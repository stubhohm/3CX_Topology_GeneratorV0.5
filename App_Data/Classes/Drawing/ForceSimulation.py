from ..Nodes.Node import Node, Vector2
from ..Constructor.TreeBuilder import TreeBuilder
from ...Modules import math, tk, start_time, total_time
from ...Keys import Height, Width, User, Is_DID, Unlinked_DIDs

class ForceSimulation():
    def __init__(self):
        self.k = 100 #coulombs constant
        self.charge = 5 # particle charge
        self.interations = 10
        self.smoothing_factor = .6
        self.show_end_users = False
        self.show_unlinked_dids = False

    def get_distance_sqrd(self, node1:Node, node2:Node):
        dist_squared = node1.position.difference(node2.position).quick_magnitude()
        return dist_squared

    def apply_repulsion(self, node1:Node, node2:Node, forces:dict[str, Vector2]):
        distance_sqrd = self.get_distance_sqrd(node1, node2)
        if distance_sqrd > 75000:
            return forces
        else:
            if distance_sqrd < 20: distance_sqrd = 20
            force_scale = self.k * (node1.weight * self.charge) * (node2.weight * self.charge) / distance_sqrd
        difference_vector = node1.position.difference(node2.position)
        unit_vector = difference_vector.scale(1/math.sqrt(distance_sqrd))
        force_1_new = unit_vector.scale(force_scale * 5)
        force_2_new = unit_vector.scale(force_scale * -5)       
        if force_1 := forces.get(node1.get_name()):
            forces[node1.get_name()] = force_1.add(force_1_new)
        else: forces[node1.get_name()] = force_1_new
        if force_2 := forces.get(node2.get_name()):
            forces[node2.get_name()] = force_2.add(force_2_new)
        else: forces[node2.get_name()] = force_2_new
        return forces


    def apply_attraction(self, node1:Node, node2:Node, forces:dict[str, Vector2]):
        distance_sqrd = self.get_distance_sqrd(node1, node2)
        if distance_sqrd < 10000:
            return forces
        force_scale = math.sqrt(distance_sqrd) / (self.k / 2)
        difference_vector = node1.position.difference(node2.position)
        unit_vector = difference_vector.scale(1/math.sqrt(distance_sqrd))
        force_1_new = unit_vector.scale(force_scale * -10)
        force_2_new = unit_vector.scale(force_scale * 10)       
        if force_1 := forces.get(node1.get_name()):
            forces[node1.get_name()] = force_1.add(force_1_new)
        else: forces[node1.get_name()] = force_1_new
        if force_2 := forces.get(node2.get_name()):
            forces[node2.get_name()] = force_2.add(force_2_new)
        else: forces[node2.get_name()] = force_2_new
        return forces

    def simulate(self, edges:list[tuple[str]], nodes:dict[str, Node], gravity:bool):
        forces:dict[str, Vector2] = {}
        for i, node1 in enumerate(nodes.values()):
            for j, node2 in enumerate(nodes.values()):
                if i >= j:
                    # Does not act on self and does not check each item twice
                    continue
                
                forces = self.apply_repulsion(node1, node2, forces)
        for edge in edges:
            node1 = nodes.get(edge[0])
            node2 = nodes.get(edge[1])
            if not node1 or not node2:
                continue
            if node1.hide_edges or node2.hide_edges:
                continue
            forces = self.apply_attraction(node1, node2, forces)
        stable = True
        for node in nodes.values():
            if node.lock:
                continue
            force = forces.get(node.get_name())
            if type(force) != Vector2:
                continue
            force = force.scale(1/node.weight * self.smoothing_factor)
            if force.quick_magnitude() < .5:
                continue
            else: stable = False
            newx, newy = node.position.add(force).get_value()
            if gravity:
                newy += 1
            padding = 30
            if Width - padding < newx: newx = Width - padding
            if newx - padding < 0: newx = 0 + padding
            if Height - padding < newy: newy = Height - padding
            if newy - padding < 0: newy = 0 + padding
            node.position.set_value(newx, newy)
        return stable



