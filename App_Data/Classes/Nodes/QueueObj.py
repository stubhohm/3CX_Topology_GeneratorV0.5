from .Node import Node
from .UserObj import UserObj
from ...Keys import Queue, Name, Number


class QueueObj(Node):
    def __init__(self):
        super().__init__()
        self.type = Queue

    def define_node(self, node_dict):
        self.type = Queue
        self.weight = 3
        self.set_name(node_dict.get(Name))
        self.set_number(node_dict.get(Number))
        self.destination = node_dict.get("Destination")
        self.strategy = node_dict.get("Strategy")
        self.ring_time = node_dict.get("Ring Time")
        self.members:dict[str, dict] = node_dict.get("Members")
        self.managers = node_dict.get("Managers")
        if len(self.managers) > 0:
            self.managers = sorted(self.managers)
        
        if self.destination:
            self.destination = self.destination[0]
        ring_locations = []
        for key in self.members.keys():
            ring_locations.append(key)
        ring_locations.append(self.destination)
        self.set_forward_to_extensions(ring_locations)

    def print(self):
        text = super().print()
        member_entries = []
        children = self.get_children()
        name = 'Destination:'
        for child in self.get_children():
            if self.destination == child.get_number():
                name = child.get_name()
                name = f"Destination: {name}"        
        ring_time = ""
        if self.ring_time:
            ring_time = self.ring_time + " seconds\n"

        text += f"\nTimeout: {ring_time}{name} ({self.destination})\n"
        
        text += "\n-- Managers --"
        for manager in self.managers:
            name = ""
            for child in children:
                if manager == child.get_number():
                    name = child.get_name()
                    name = f": {name}"
                    break
            text += f"\n{manager}{name}"

        for members in self.members.values():
            number = members.get("Number")
            name, agent_status = "", ""
            for child in children:
                if number == child.get_number():
                    name = child.get_name()
                    if isinstance(child, UserObj):
                        agent_status = f"\n\tAgent Status: {child.status}"
                    break
            entry = f"\n{name}\n\tExt: {number}\n\tQueue Status: {members.get("Status")}{agent_status}"
            member_entries.append(entry)
        sorted_entries = sorted(member_entries)
        
        text += f"\n\nPolling Strategy:{self.strategy}"

        text += "\n-Members-"
        for member in sorted_entries:
            text += member
        text += "\n\n"
        return text
