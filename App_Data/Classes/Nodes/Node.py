from ...Keys import User, IVR, Queue, RingGroup, Name, Number, Is_DID
from ...Modules import math
from ..Data_Structures.Vectors.Vector2 import Vector2

class Node():
    def __init__(self):
        self._name = "Unnamed Node"
        self._number = None
        self._children:list[Node] = []
        self._forward_to_extensions:list[str] = []
        self.parented:bool = False
        self.is_did = False
        self.type = None
        self.highlight = False
        self.position = Vector2()
        self.oval_id = None
        self.text_id = None
        self.lock = False

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

    def get_point_on_oval(self, x_origin, y_origin, width, height, angle):
        x = x_origin + (width / 2) * math.cos(angle)
        y = y_origin + (height / 2) * math.sin(angle)
        return x, y

    def initial_position(self, designated_pos:tuple[int, int], screen_size:tuple[int, int], is_radial:bool, depth = 0, visited_nodes = None, rotation = 0):
        if visited_nodes is None:
            visited_nodes = []
        x, y = designated_pos
        if self.get_name() in visited_nodes:
            return
        self.position.set_value(x , y)
        children = self.get_children()
        children_count = len(children)
        height, width = screen_size
        depth += 1
        visited_nodes.append(self.get_name())
        for i, child in enumerate(children):
            if not isinstance(child, Node):
                continue
            degrees = int((i / children_count) * 360)
            degrees -= rotation
            child_x, child_y = self.get_point_on_oval(x, y, (width / (depth + 3)), ( height/ (depth + 3)), degrees)
            child.initial_position((child_x, child_y), screen_size, is_radial, depth, visited_nodes, rotation)

    def print(self):
        print("\n\n")
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        print(f"\nDetails for {self.get_name()}\n")

        print(f"Type: {self.type}")
        if not self.is_did:
            print(f"Extension: {self.get_number()}")
    
    def define_node(self, node_dict:dict):
        pass


class User_obj(Node):

    def define_node(self, node_dict):
        self.type = User
        self.first = node_dict.get("First")
        self.last = node_dict.get("Last")
        if self.first and self.last:
            name = self.first + " " + self.last
        else: name = self.first
        self.set_name(name)
        self.set_number(node_dict.get(Number))
        self.status = node_dict.get("Current Status")
        self.vm_pin = node_dict.get("VM PIN")

    def print(self):
        super().print()
        print(self.status)
        print("---------------------------------------------")
        print("\n\n\n\n\n")


class IVR_obj(Node):
    def __init__(self):
        super().__init__()

    def define_node(self, node_dict):
        self.type = IVR
        self.set_name(node_dict.get(Name))
        self.set_number(node_dict.get(Number))
        self.timeout_type:str = node_dict.get("Timeout Type")
        self.timeout_destination:str = node_dict.get("Timeout DN")
        self.forwards:dict[str, dict] = node_dict.get("Forwards")
        ring_locations = []
        if type(self.forwards) == dict:
            for key in self.forwards.keys():
                if type(key) != str:
                    continue
                if key.isdigit():
                    ring_locations.append(key)
        if type(self.timeout_destination) == str:
            ring_locations.append(self.timeout_destination)
        self.set_forward_to_extensions(ring_locations)


    def print(self):
        super().print()
        fwd_dict = {}
        for forward in self.forwards.values():
            fwd_type = forward.get("Forward Type")
            num = forward.get("Dial Number")
            ext = forward.get("Extension")
            for child in self.get_children():
                if child.get_number() == ext:
                    name = child.get_name()
                    ext = f"{name} ({ext})"
            value = f"{num}: {fwd_type} - {ext}"
            if type(num) == str and num.isdigit():
                order = int(num)
            fwd_dict[order] = value
        for i in range(len(fwd_dict)):
            print(fwd_dict[i + 1])

        name = ''
        for child in self.get_children():
            if self.timeout_destination == child.get_number():
                name = child.get_name()
                name = f" - {name}"
        if self.timeout_destination:
            timeout = f" ({self.timeout_destination})"
        else: timeout = ""
        print(f"\nTimeout:{self.timeout_type}{name}{timeout}")
        print("---------------------------------------------")
        print("\n\n\n\n\n")


class Queue_obj(Node):
    def __init__(self):
        super().__init__()

    def define_node(self, node_dict):
        self.type = Queue
        self.set_name(node_dict.get(Name))
        self.set_number(node_dict.get(Number))
        self.members:dict[str, dict] = node_dict.get("Members")
        self.managers = node_dict.get("Managers")
        if len(self.managers) > 0:
            self.managers = sorted(self.managers)
        self.destination = node_dict.get("Destination")
        if self.destination:
            self.destination = self.destination[0]
        ring_locations = []
        for key in self.members.keys():
            ring_locations.append(key)
        ring_locations.append(self.destination)
        self.set_forward_to_extensions(ring_locations)


    def print(self):
        super().print()
        member_entries = []
        children = self.get_children()
        name = ''
        for child in self.get_children():
            if self.destination == child.get_number():
                name = child.get_name()
                name = f" - {name}"        
        
        print(f"Timeout{name} ({self.destination})\n")
        
        print("-- Managers --")
        for manager in self.managers:
            name = ""
            for child in children:
                if manager == child.get_number():
                    name = child.get_name()
                    name = f": {name}"
                    break
            print(f"{manager}{name}")

        for members in self.members.values():
            number = members.get("Number")
            name, agent_status = "", ""
            for child in children:
                if number == child.get_number():
                    name = child.get_name()
                    if isinstance(child, User_obj):
                        agent_status = f"\n\tAgent Status: {child.status}"
                    break
            entry = f"{name}\n\tExt: {number}\n\tQueue Status: {members.get("Status")}{agent_status}"
            member_entries.append(entry)
        sorted_entries = sorted(member_entries)
        
        print("\n-Members-")
        for member in sorted_entries:
            print(member)
        print("---------------------------------------------")
        print("\n\n\n\n\n")

class RingGroup_obj(Node):
    def __init__(self):
        super().__init__()


    def define_node(self, node_dict:dict):
        self.type = RingGroup
        self.set_name(node_dict.get(Name))
        self.set_number(node_dict.get(Number))
        self.destination = node_dict.get("Destination")
        self.ring_strategy = node_dict.get("RingStrategy")
        if self.destination:
            self.destination = self.destination[0]
        self.members = node_dict.get("Members")
        forwards_to = list(self.members)
        forwards_to.append(self.destination)
        self.set_forward_to_extensions(forwards_to)
        
        
    def print(self):
        super().print()
        children = self.get_children()
        name = ''
        for child in self.get_children():
            if self.destination == child.get_number():
                name = child.get_name()
                name = f" - {name} -"
        print(f"\n#Timeout#{name} Ext: {self.destination}")
        
        member_entries = []
        for number in self.members:
            name = ""
            status = ""
            for child in children:
                if number == child.get_number():
                    name = child.get_name()
                    if type(child) == User_obj:
                        status =  child.status
                        status = f"\n\tStatus: {status}"
                        number = f"\n\tExt: {number}"
                    break
            entry = f"{name}{number}{status}"
            member_entries.append(entry)
        sorted_entries = sorted(member_entries)
        print(f"Ring Strategy: {self.ring_strategy}")
        print("\n-Members-")
        for member in sorted_entries:
            print(member)
        print("---------------------------------------------")
        print("\n\n\n\n\n")

class DID_obj(Node):
    def __init__(self):
        super().__init__()

    def define_node(self, node_dict):
        self.type = Is_DID
        self.is_did = True
        self.set_name(node_dict.get(Name))
        self.set_number(node_dict.get(Number))
        self.conditions = node_dict.get("Conditions")
        self.forward_destinations:dict = node_dict.get("Forward Destinations")
        rings_to = []
        if type(self.forward_destinations) == dict:
            for destination in self.forward_destinations.values():
                internal_dest = destination.get("Internal")
                if type(internal_dest) != list:
                    continue
                if len(internal_dest) != 0:
                    rings_to.append(internal_dest[0])
        self.set_forward_to_extensions(rings_to)

    def print(self):
        super().print()
        print("---------------------------------------------")

