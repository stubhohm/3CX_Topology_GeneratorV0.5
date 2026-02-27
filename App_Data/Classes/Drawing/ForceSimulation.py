from ..Nodes.Node import Node, Vector2
from ..Constructor.TreeBuilder import TreeBuilder
from ...Modules import math, tk, start_time, total_time
from ...Keys import Height, Width

class ForceSimulation():
    def __init__(self):
        # Physical Constants
        self.k = 15.0            # Ideal spring length/strength constant
        self.repulsion_strength = 800.0
        self.attraction_strength = 0.10
        self.damping = 0.85      # Velocity decay (0.0 to 1.0)
        self.max_force = 50.0    # Prevents "explosive" movements
        
        # State
        self.velocities: dict[str, Vector2] = {}

    def get_displacement(self, node1: Node, node2: Node):
        """Returns the vector from node2 to node1 and the distance."""
        dx = node1.position.getX() - node2.position.getX()
        dy = node1.position.getY() - node2.position.getY()
        dist_sq = dx*dx + dy*dy
        dist = math.sqrt(dist_sq) if dist_sq > 0 else 0.1
        return dx, dy, dist

    def simulate(self, edges: list[tuple[str]], nodes: dict[str, Node], gravity: bool):
        # 1. Initialize forces for this frame
        node_list = list(nodes.values())
        forces = {name: [0.0, 0.0] for name in nodes.keys()}

        # 2. Repulsion (All-to-all)
        # Optimized to avoid square roots inside the main loop where possible
        for i, node1 in enumerate(node_list):
            name1 = node1.get_name()
            for j in range(i + 1, len(node_list)):
                node2 = node_list[j]
                name2 = node2.get_name()
                
                dx, dy, dist = self.get_displacement(node1, node2)
                
                # Coulomb-like repulsion: Force = Strength / distance^2
                # Limit min distance to avoid division by zero/infinite force
                if dist < 10: dist = 10 
                
                mag = (self.repulsion_strength * node1.weight * node2.weight) / (dist * dist)
                
                fx = (dx / dist) * mag
                fy = (dy / dist) * mag
                
                forces[name1][0] += fx
                forces[name1][1] += fy
                forces[name2][0] -= fx
                forces[name2][1] -= fy

        # 3. Attraction (Edges only)
        for u, v in edges:
            node1, node2 = nodes.get(u), nodes.get(v)
            if not node1 or not node2 or node1.hide_edges or node2.hide_edges:
                continue
                
            dx, dy, dist = self.get_displacement(node1, node2)
            
            # Hooke's Law: Force = Strength * distance
            mag = dist * self.attraction_strength
            
            fx = (dx / dist) * mag
            fy = (dy / dist) * mag
            
            forces[u][0] -= fx
            forces[u][1] -= fy
            forces[v][0] += fx
            forces[v][1] += fy

        # 4. Apply Forces and Move Nodes
        stable = True
        padding = 30
        
        for name, node in nodes.items():
            if node.lock:
                continue

            # Get force and apply mass (weight)
            fx, fy = forces[name]
            accel_x = fx / node.weight
            accel_y = fy / node.weight

            # Get or init velocity
            vel = self.velocities.get(name, [0.0, 0.0])
            
            # Update velocity with damping
            vel[0] = (vel[0] + accel_x) * self.damping
            vel[1] = (vel[1] + accel_y) * self.damping

            # Cap max speed to prevent jitter
            speed_sq = vel[0]**2 + vel[1]**2
            if speed_sq > self.max_force**2:
                scale = self.max_force / math.sqrt(speed_sq)
                vel[0] *= scale
                vel[1] *= scale

            # Check if moving significantly
            if speed_sq > 0.2:
                stable = False

            # Update position
            new_x = node.position.getX() + vel[0]
            new_y = node.position.getY() + vel[1]
            
            if gravity:
                new_y += 1.5

            # Boundary Constraints
            new_x = max(padding, min(Width - padding, new_x))
            new_y = max(padding, min(Height - padding, new_y))

            node.position.set_value(new_x, new_y)
            self.velocities[name] = vel

        return stable