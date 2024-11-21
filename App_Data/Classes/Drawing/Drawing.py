from ...Modules import tk, math, os
from ..Constructor.TreeBuilder import TreeBuilder
from ...Classes.Nodes.Node import Node, Vector2
from .ForceSimulation import ForceSimulation
from ...Keys import User, RingGroup, IVR, Is_DID, Queue, Root, Island, Client, Display_Format, Link_Holiday
from ...Keys import Line, HighLight, Display_Format, Lock, Text
from ...Keys import Unlinked_DIDs, Background, default_colors, dark_mode_colors,Dark_Mode
from ...Keys import Height, Width


class Renderer():
    def __init__(self, tree:TreeBuilder, config_dict:dict):
        self.config_dict = config_dict
        self.client_name = config_dict.get(Client)
        self.tree = tree
        self.show_end_users = config_dict.get(User)
        self.show_unlinked_dids = config_dict.get(Unlinked_DIDs)
        self.radial_display = config_dict.get(Display_Format)
        self.link_holiday = config_dict.get(Link_Holiday)
        self.set_color_pallet(config_dict.get(Dark_Mode))
        self.instance_default_variables()

        self.define_edges(tree)

        self.generate_graph()

        self.root = tk.Tk()
        self.root.title(f"3CX Topology: {self.client_name}")
        self.canvas = tk.Canvas(self.root, width=Width, height=Height, bg=self.color_coding.get(Background))
        self.canvas.pack()

        self.set_key_binds()

        self.draw_graph()      

    def set_key_binds(self):
        if os.name == "posix":
            right_click = '<ButtonPress-2>'
            right_release = '<ButtonRelease-2>'
        else:
            right_click = '<ButtonPress-3>'
            right_release = '<ButtonRelease-3>'
        self.canvas.bind('<ButtonPress-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind(right_click, self.right_click_toggle_node_highlight)
        self.canvas.bind('<MouseWheel>', self.gravity_well)
        self.canvas.bind(right_release, self.on_release)
        self.root.bind('<j>', self.gravity_well)
        self.root.bind('<k>', self.gravity_well)
        self.root.bind('<l>', self.node_lock)
        self.root.bind('<h>', self.toggle_hide_edges)
        self.root.bind('<i>', self.print_info)
        self.root.bind('<u>', self.simulate_nodes)
        self.root.bind('<g>', self.simulate_nodes)

    def instance_default_variables(self):
        self.edges = None
        self.selected_node = None
        self.marked_node = None
        self.edge_ids = {}
        self.graph = None
        self.node_radius = 20
        self.pull_strength = 1

    def set_color_pallet(self, is_dark_mode:bool):
        if is_dark_mode:
            self.color_coding = dark_mode_colors
        else:
            self.color_coding = default_colors

    def define_edges(self, tree:TreeBuilder):
        """Takes the input tree and gets define edges for graphing."""
        edges:set = {(1,1)}
        for node in tree.nodes.values():
            if not self.is_valid_to_draw(node):
                continue
            parent_name = node.get_name()
            for child in node.get_children():
                if not self.is_valid_to_draw(child):
                    continue

                entry = (parent_name, child.get_name())

                if entry not in edges:
                    edges.add(entry)
        print(len(edges))
        self.edges = edges
      
    def generate_graph(self):
        """Takes defined edges and generates positions based on those edges."""
        # Create a directed graph (for tree-like structure)
        drawn_nodes = []
        for node in self.tree.nodes.values():
            if self.is_valid_to_draw(node):
                drawn_nodes.append(node)

        nodes_count = len(drawn_nodes)
        sqr_size = int(math.sqrt(nodes_count))
        width_space = Width / sqr_size
        height_space = Height / sqr_size        
        for i, node in enumerate(drawn_nodes):
            column = i % sqr_size
            row = int(i / sqr_size)
            x = (column) * width_space
            y = (row) * height_space
            node.position.set_value(x,y)

        self.tree.nodes[Root].unlock_all_children()
        self.tree.nodes[Island].unlock_all_children()

    def is_valid_to_draw(self, node:Node):
        """Checks is node is valid based on what node types are shown."""
        if not isinstance(node, Node):
            return False
        if node.type == User:
            if not self.show_end_users:
                return False 
        if node.type == Is_DID:
            if not self.show_unlinked_dids:
                if len(node.get_children_names()) < 2:
                    return False
        if not self.link_holiday:
            if node.get_number() == "HOL":
                return False
        return True
    
    def draw_graph(self):
        # Draw edges first
        for edge in self.edges:
            self.draw_edge(edge)
        # Draw nodes and text
        for node in self.tree.nodes.values():
            if not node:
                continue

            self.draw_node(node)

    def adjust_for_radius(self, x0, y0, x1, y1):
        """Adjust the edge positions to stop at the node boundaries, not inside the ovals."""
        # Calculate the direction vector from node1 to node2
        dx = x1 - x0
        dy = y1 - y0
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Calculate the unit direction vector
        if distance == 0:
            distance = 1
        ux = dx / distance
        uy = dy / distance

        # Adjust both start and end positions by the radius of the node
        x0_adj = x0 + self.node_radius * ux
        y0_adj = y0 + self.node_radius * uy
        x1_adj = x1 - self.node_radius * ux
        y1_adj = y1 - self.node_radius * uy

        return x0_adj, y0_adj, x1_adj, y1_adj

    def draw_node(self, node:Node):
        """Draw a node and its label."""
        if not self.is_valid_to_draw(node):
            return
        position = node.position
        x, y = position.getX(), position.getY()
        node_name = node.get_name()
        color = self.color_coding.get(node.type, 'lightblue')
        text_color = self.color_coding.get(Text, "grey")
        outline_color = "black"
        if node.highlight:
            outline_color = self.color_coding.get(HighLight)
        node.oval_id = self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill=color, outline=outline_color)
        node.text_id = self.canvas.create_text(x, y, text=node_name, fill= text_color) 

    def draw_edge(self, edge):
        """Draw an edge between two nodes with an arrow, adjusting for the node radius."""
        node1, node2 = edge
        node1_obj = self.tree.get_node_by_name(node1)
        node2_obj = self.tree.get_node_by_name(node2)
        if not self.is_valid_to_draw(node1_obj):
            return
        if not self.is_valid_to_draw(node2_obj):
            return
        
        x0, y0 = node1_obj.position.getX(), node1_obj.position.getY()
        x1, y1 = node2_obj.position.getX(), node2_obj.position.getY()

        # Adjust the positions so that the line doesn't go inside the nodes
        x0_adj, y0_adj, x1_adj, y1_adj = self.adjust_for_radius(x0, y0, x1, y1)

        # Draw arrowed line for directed edge
        line_color = self.color_coding.get(Line, "grey")
        
        self.edge_ids[edge] = self.canvas.create_line(x0_adj, y0_adj, x1_adj, y1_adj, arrow=tk.LAST, fill= line_color)

    def update_edges(self, node:Node):
        """Update the position of edges connected to a node."""
        if not self.is_valid_to_draw(node):
            return
        for edge in self.edges:
            edge_id = self.edge_ids.get(edge)
            if not edge_id:
                continue
            if node.get_name() in edge:
                node1, node2 = edge
                node1_obj = self.tree.get_node_by_name(node1)
                node2_obj = self.tree.get_node_by_name(node2)
                x0, y0 = node1_obj.position.getX(), node1_obj.position.getY()
                x1, y1 = node2_obj.position.getX(), node2_obj.position.getY()
                x0_adj, y0_adj, x1_adj, y1_adj = self.adjust_for_radius(x0, y0, x1, y1)
                line_color = self.color_coding.get(Line, "grey")
                if node1_obj.highlight and node2_obj.highlight:
                    line_color = self.color_coding.get(HighLight, "grey")
                if node1_obj.hide_edges or node2_obj.hide_edges:
                    self.canvas.itemconfigure(edge_id, state="hidden")
                else:
                    self.canvas.itemconfigure(edge_id, state="normal")
                self.canvas.itemconfig(edge_id, fill = line_color)

                self.canvas.itemconfig(node1_obj.oval_id, outline ="black")
                self.canvas.itemconfig(node2_obj.oval_id, outline ="black")
                if node1_obj.highlight:
                    self.canvas.itemconfig(node1_obj.oval_id, outline = self.color_coding.get(HighLight, "grey"))   
                elif node1_obj.lock:
                    self.canvas.itemconfig(node1_obj.oval_id, outline = self.color_coding.get(Lock, "grey"))
                if node2_obj.highlight:
                    self.canvas.itemconfig(node2_obj.oval_id, outline = self.color_coding.get(HighLight, "grey"))
                elif node2_obj.lock:
                    self.canvas.itemconfig(node2_obj.oval_id, outline = self.color_coding.get(Lock, "grey"))

                self.canvas.coords(edge_id, x0_adj, y0_adj, x1_adj, y1_adj)

    def on_click(self, event):
        """Handle node selection on mouse click."""
        item = self.canvas.find_closest(event.x, event.y)[0]
        for node in self.tree.nodes.values():
            if not node:
                continue
            if item == node.oval_id or item == node.text_id:
                x, y = self.canvas.coords(node.oval_id)[0], self.canvas.coords(node.oval_id)[1]
                distance = int((event.x - x)**2 + (event.y - y)**2)
                if (distance) > ((self.node_radius * 2)**2):
                    continue
                self.selected_node = node
                # Calculate the offset to ensure smooth dragging
                self.node_offset_x = event.x - x
                self.node_offset_y = event.y - y
                break

    def right_click_toggle_node_highlight(self, event):
        """Handle node selection on mouse click."""
        item = self.canvas.find_closest(event.x, event.y)[0]
        for node in self.tree.nodes.values():
            if not node:
                continue
            if item == node.oval_id or item == node.text_id:
                x, y = self.canvas.coords(node.oval_id)[0], self.canvas.coords(node.oval_id)[1]
                distance = int((event.x - x)**2 + (event.y - y)**2)
                if (distance) > ((self.node_radius * 2)**2):
                    continue
                node.highlight_children()
                self.marked_node = node
                for node in self.tree.nodes.values():
                    self.update_edges(node)
                break
            
    def on_drag(self, event):
        """Handle node dragging."""
        if self.selected_node:
            # Update node position
            x, y = event.x - self.node_offset_x, event.y - self.node_offset_y
            self.canvas.coords(self.selected_node.oval_id, x, y, x + (2*self.node_radius), y + (2*self.node_radius))

            # Update text position
            self.canvas.coords(self.selected_node.text_id, x + self.node_radius, y + self.node_radius)

            # Update the graph's node position (for updating edges)
            x, y = ((x + self.node_radius), (y + self.node_radius))
            self.selected_node.position.set_value(x, y)

            # Update connected edges
            self.update_edges(self.selected_node)

    def pull_all(self, event):
        if not self.selected_node:
            return
        for node in self.tree.nodes.values():
            if not self.is_valid_to_draw(node):
                continue
            self.push_or_pull_nodes(node, 1)

    def repel_children_while_pulling(self, parent_node:Node):
        min_distance = 10
        repulsion_strength = 5000
        for i, child_a in enumerate(parent_node.get_children()):
            if not self.is_valid_to_draw(child_a):
                continue
            for j, child_b in enumerate(parent_node.get_children()):
                if not self.is_valid_to_draw(child_b):
                    continue
                if i >= j:
                    continue
                # Calculate the distance between the two nodes
                dx = child_b.position.getX() - child_a.position.getX()
                dy = child_b.position.getY() - child_a.position.getY()
                distance = math.sqrt(dx**2 + dy**2)

                # Avoid division by zero and too strong forces for very close nodes
                if distance < min_distance:
                    distance = min_distance

                # Calculate repulsive force
                force = repulsion_strength / (distance**2)  # Force decreases with distance squared

                # Determine movement along x and y axes
                move_x = force * (dx / distance)
                move_y = force * (dy / distance)

                # Apply movement to both nodes in opposite directions
                child_a_x = child_a.position.getX() - move_x
                child_a_y = child_a.position.getY() - move_y
                child_b_x = child_b.position.getX() + move_x
                child_b_y = child_b.position.getY() + move_y

                # Update positions and pin insdie window to prevent runaways
                if not child_a.lock:
                    if child_a_x < 0: child_a_x = 0
                    if child_a_x > Width: child_a_x = Width
                    if child_a_y < 0: child_a_y = 0
                    if child_a_y > Height: child_a_y = Height
                    child_a.position.set_value(child_a_x, child_a_y)
                if not child_b.lock:
                    if child_b_x < 0: child_b_x = 0
                    if child_b_x > Width: child_b_x = Width
                    if child_b_y < 0: child_b_y = 0
                    if child_b_y > Height: child_b_y = Height
                    child_b.position.set_value(child_b_x, child_b_y)            

        for child in parent_node.get_children():
            x, y = (child.position.getX() - self.node_radius), (child.position.getY() - self.node_radius)
            self.canvas.coords(child.oval_id, x, y, x + (2*self.node_radius), y + (2*self.node_radius))
            self.canvas.coords(child.text_id, x + self.node_radius, y + self.node_radius)
            self.update_edges(child)

    def push_or_pull_nodes(self, parent_node:Node, direction:int):
        pull_factor = 0.05
        parent_x, parent_y = parent_node.position.get_value() 
        for child in parent_node.get_children():
            if child.lock:
                continue
            if not self.is_valid_to_draw(child):
                continue
            child_x, child_y = child.position.get_value()
            dx, dy = child_x - parent_x, child_y - parent_y
            dist_to_child = math.sqrt(dx**2 + dy**2)
            if dist_to_child < self.node_radius * 4 and direction > 0:
                dx = 0
                dy = 0            
            x = child_x - (dx * pull_factor * direction)
            y = child_y - (dy * pull_factor * direction)
            if x < 0: x = 0
            if x > Width: x= Width
            if y < 0: y = 0
            if y > Height: y = Height
            child.position.set_value(x,y)
        self.repel_children_while_pulling(parent_node)
        
    def gravity_well(self, event:tk.Event):
        if event.num == 5 or event.delta > 0 or event.keysym == "k":
            mag_scaler = -1
        elif event.num == 4 or event.delta < 0 or event.keysym == "j":
            mag_scaler = 1
        else:
            return
        if not self.marked_node and not self.selected_node:
            return
        parent_node = (self.marked_node or self.selected_node)
        if not isinstance(parent_node, Node):
            return
        parent_node.highlight_children(highlight_tgt=False)
        for node in self.tree.nodes.values():
            self.update_edges(node)
        self.push_or_pull_nodes(parent_node, mag_scaler)

    def node_lock(self, event):
        if event.keysym != "l":
            return
        if not self.marked_node and not self.selected_node:
            return
        primary_node = (self.marked_node or self.selected_node)
        if not isinstance(primary_node, Node):
            return
        primary_node.lock = not primary_node.lock
        if primary_node.lock:
            self.canvas.itemconfig(primary_node.oval_id, outline = self.color_coding.get(Lock, "grey"))
        else:
            self.canvas.itemconfig(primary_node.oval_id, outline = "black")

    def print_info(self, event):
        if not self.selected_node:
            return
        self.selected_node.info_popup(self.color_coding)

    def toggle_hide_edges(self, event):
        if not self.selected_node:
            return
        self.selected_node.hide_edges = not self.selected_node.hide_edges
        self.update_edges(self.selected_node)

    def on_release(self, event):
        """Reset the selected node after releasing the mouse button."""
        self.selected_node = None
        self.marked_node = None

    def simulate_nodes(self, event):
        force_sim = ForceSimulation()
        drawn_nodes:dict[str, Node] = {}
        for node in self.tree.nodes.values():
            if not self.is_valid_to_draw(node):
                continue
            drawn_nodes[node.get_name()] = node
        gravity =  not self.config_dict.get(Display_Format)
        for i in range(500):
            stable = force_sim.simulate(self.edges, drawn_nodes, gravity)
            for node in self.tree.nodes.values():
                x, y = (node.position.getX() - self.node_radius), (node.position.getY() - self.node_radius)
                self.canvas.coords(node.oval_id, x, y, x + (2*self.node_radius), y + (2*self.node_radius))
                self.canvas.coords(node.text_id, x + self.node_radius, y + self.node_radius)
                self.update_edges(node)
            self.root.update()           
            if i % 100 == 0:
                print("Iterations: ", i)
            if stable:
                return