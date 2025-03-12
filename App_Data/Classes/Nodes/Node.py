from ...Keys import User, IVR, Queue, RingGroup, Name, Number, Is_DID, Height, Width, Background, Line, Text
from ...Modules import math, tk, font
from ..Data_Structures.Vectors.Vector2 import Vector2

class Node():
    def __init__(self):
        self._name = "Unnamed Node"
        self._number = None
        self._children:list[Node] = []
        self._forward_to_extensions:list[str] = []
        self.after_hours_extension:str = "Not Set"
        self.parented:bool = False
        self.is_did = False
        self.type = 'No Type'
        self.highlight = False
        self.position = Vector2()
        self.oval_id = None
        self.text_id = None
        self.lock = False
        self.hide_edges = False
        self.weight = 1

    def define(self, name, number, type):
            self._name = name
            self._number = number
            self.type = type
            
    def set_name(self, new_name:str):
        self._name = new_name

    def get_name(self):
        return self._name
    
    def get_number(self):
        return self._number
    
    def set_number(self, new_number:str):
        self._number = new_number

    def set_forward_to_extensions(self, new_forward_to_extensions:list[str]):
        """"
        Stores a string list of extension names that are children of this node.
        \nThis are removed when the node is added fully.
        """
        self._forward_to_extensions = new_forward_to_extensions

    def get_forward_to_extensions(self):
        return self._forward_to_extensions

    def add_child(self, child_node):
        """
        Adds child to this node, and removes it from unmapped nodes if it is present.
        """
        if not isinstance(child_node, Node):
            return
        else:
            child_node.parented = True
            self._children.append(child_node)
            if child_node.get_name() in self._forward_to_extensions:
                self._forward_to_extensions.remove(child_node.get_name())
            if child_node.get_number() in self._forward_to_extensions:
                self._forward_to_extensions.remove(child_node.get_number())

    def remove_child(self, child_node):
        if not isinstance(child_node, Node):
            return
        else:
            if child_node in self._children:
                self._children.remove(child_node)   

    def find_child_with_name(self, name, visited_nodes = None):
        if visited_nodes is None:
            visited_nodes = []
        node_name = self.get_name()
        # Found Target
        if node_name == name:
            return self
        # Found Loop
        if node_name in visited_nodes:
            return None
        
        # Incriment
        visited_nodes.append(node_name)

        for child in self.get_children():
            if target := child.find_child_with_name(name, visited_nodes):
                if isinstance(target, Node):
                    return target
        return None

    def get_child_node_by_name(self, node_name:str):
        for child in self.get_children():
            if not child:
                continue
            if not isinstance(child ,Node):
                continue
            if node_name == child.get_name():
                return child
            else:
                continue

    def get_children(self):
        return self._children

    def get_mapped_children_numbers(self):
        number_list:list[str] = []
        for child in self.get_children():
            if not child:
                continue
            number_list.append(child.get_number())     
        return number_list

    def get_mapped_children_names(self):
        name_list:list[str] = []
        for child in self.get_children():
            if not child:
                continue
            name_list.append(child.get_name())
        return name_list

    def is_parent(self, node_name):
        """Returns True if the node_name is a child of the input node."""
        if self.get_name() == node_name:
            return True
        if self.find_child_with_name(node_name):
            return True
        return False

    def get_unmapped_children(self):
        name_list:list[str] = []
        mapped_numbers = self.get_mapped_children_numbers()
        for forward_to in self._forward_to_extensions:
            if not forward_to:
                continue
            if forward_to in mapped_numbers:
                continue
            if forward_to not in name_list:
                name_list.append(forward_to)
        return name_list

    def get_children_names(self):
        mapped_list = self.get_mapped_children_names()
        unmapped_list = self.get_unmapped_children()
        name_list = mapped_list
        for entry in unmapped_list:
            name_list.append(entry)
        return name_list

    def map_unmapped_chilren(self):
        unmapped_nodes = self.get_unmapped_children()
        new_nodes:list[Node] = []
        for unmapped_node in unmapped_nodes:
            new_node = Node()
            new_node.define(unmapped_node, unmapped_node, User)
            self.add_child(new_node)
            new_nodes.append(new_node)
        return new_nodes

    def highlight_children(self, visited_nodes = None, highlight_tgt = None):
        if highlight_tgt is None:
            highlight_tgt = None

        if visited_nodes is None:
            visited_nodes = []
        
        # Break Loops
        if self.get_name() in visited_nodes:
            return
        # Incriment
        visited_nodes.append(self.get_name())
        # Ensures that all children are highlighted
        # in the same scheme as the parent.
        if highlight_tgt is None:
            self.highlight = not self.highlight
            highlight_tgt = self.highlight
        self.highlight = highlight_tgt
        for child in self.get_children():
            if not isinstance(child, Node):
                continue
            child.highlight_children(visited_nodes, highlight_tgt)

    def get_point_on_oval(self, x_origin, y_origin, distance, radians):
        x = x_origin + (distance / 2) * math.cos(radians)
        y = y_origin + (distance / 2) * math.sin(radians)
        return x, y

    def unlock_all_children(self):
        if not self.lock:
            return
        else: self.lock = False
        for child in self.get_children():
            if not isinstance(child, Node):
                continue
            child.unlock_all_children()

    def initial_position(self, designated_pos:tuple[int, int], is_radial:bool, depth = 0, rotation = 0, draw_users = False):
        if self.lock:
            return
        else:
            self.lock = True
        x, y = designated_pos
        self.position.set_value(x , y)            
        
        children = self.get_children()
        if len(children) == 0:
            return
        unique_children, unique_names = [], []
        for child in children:
            if not draw_users and child.type == User:
                continue
            if child.get_name() not in unique_names:
                unique_children.append(child)
                unique_names.append(child.get_name())
        if len(unique_children) == 0:
            return
        
        distance = 500
        depth += 1
        distance = 500 / depth
        radian_incriment = 2 * math.pi / len(unique_children)
        
        for i, child in enumerate(unique_children):
            if not draw_users and child.type == User:
                continue
            if not isinstance(child, Node):
                continue    
            degrees = radian_incriment * i
            adjusted_degrees = degrees + rotation
            child_x, child_y = self.get_point_on_oval(x, y, distance, degrees)
            child.initial_position((child_x, child_y), is_radial, depth, adjusted_degrees, draw_users)

    def print(self):
        text = f"\n\n\nType: {self.type}"
        if not self.is_did and not self.type == Is_DID:
            text += f"\nExtension: {self.get_number()}"
        text += "\n"
        for child in self.get_children():
            if self.after_hours_extension == child.get_number():
                name = child.get_name()
                text += f"After Hours Locatoin: {name} ({child.get_number()})\n" 
        return text

    def info_popup(self, color_pallet:dict):
        title = f"\nDetails for {self.get_name()}"
        body = self.print()
        pop_up = tk.Toplevel()
        pop_up.title("Node Details")
        pop_up.geometry(f"450x450")
        
        body_font = font.Font(family="Helvetica", size=10)
        header_font = font.Font(family="Helvetica", size=15)

        frame = tk.Frame(pop_up)
        

        text_widget = tk.Text(frame, wrap="word", bg = color_pallet.get(Background, "white")) # Insert the text content
        text_widget.tag_configure("header", font=header_font, foreground=color_pallet.get(Text, "grey"), justify="center")
        text_widget.tag_configure("body", font=body_font, foreground=color_pallet.get(Text, "grey"))  

        text_widget.insert("1.0", title, "header")
        text_widget.insert("end", body, "body")
        text_widget.config(state="disabled")

        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(expand=True, side="top", fill="both")
        frame.pack(expand=True, fill="both")
        pop_up.bind("<Escape>", lambda e: pop_up.destroy())

    def set_weight(self, weight:int, visited_nodes:list[str]):
        if self.weight:
            return
        if self.get_name() in visited_nodes:
            return
        visited_nodes.append(self.get_name())
        self.weight = weight/2
        for child in self.get_children():
            child.set_weight(self.weight, visited_nodes)

    def define_node(self, node_dict:dict):
        self.after_hours_extension = node_dict.get("After Hours", "Not Set")
        pass

