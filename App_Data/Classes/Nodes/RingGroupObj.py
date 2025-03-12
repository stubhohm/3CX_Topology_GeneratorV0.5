from .Node import Node
from .UserObj import UserObj
from ...Keys import RingGroup, Name, Number


class RingGroupObj(Node):
    def __init__(self):
        super().__init__()
        self.type = RingGroup

    def define_node(self, node_dict:dict):
        self.type = RingGroup
        self.weight = 3
        self.set_name(node_dict.get(Name))
        self.set_number(node_dict.get(Number))
        self.destination = node_dict.get("Destination")
        self.ring_strategy = node_dict.get("RingStrategy")
        self.members = node_dict.get("Members")
        self.other_dest = node_dict.get("other")
        forwards_to = list(self.members)
        if type(self.destination) == dict:
            for value in self.destination.values():
                forwards_to.append(value)
        super().define_node(node_dict)
        forwards_to.append(self.after_hours_extension)
        self.set_forward_to_extensions(forwards_to)
        
        
    def print(self):
        text = super().print()
        children = self.get_children()
        name = ''
        for child in self.get_children():
            if self.destination == child.get_number():
                name = child.get_name()
                name = f" - {name}"

        text += f"\nTimeout Locations:\n"
        
        for key in self.destination.keys():
            dest_ext = self.destination.get(key)
            child_name = ""
            for child in self.get_children():
                if child.get_number() == dest_ext:
                    if child_name == dest_ext:
                        break
                    child_name = child.get_name()
                    dest_ext = " (" + dest_ext + ")"
                    break
            text += f"{key}: {child_name}{dest_ext}\n"

        member_entries = []
        for number in self.members:
            name = ""
            status = ""
            for child in children:
                if number == child.get_number():
                    name = child.get_name()
                    if type(child) == UserObj:
                        status =  child.status
                        status = f"\n\tStatus: {status}"
                        number = f"\n\tExt: {number}"
                    break
            entry = f"\n{name}{number}{status}"
            member_entries.append(entry)
        sorted_entries = sorted(member_entries)
        text += f"\nRing Strategy: {self.ring_strategy}"
        text += "\n\n-Members-"
        for member in sorted_entries:
            text += member
        text += "\n\n"
        return text