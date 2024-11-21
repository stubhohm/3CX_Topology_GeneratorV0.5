from .Node import Node
from ...Keys import Is_DID, Name, Number

class DIDObj(Node):
    def __init__(self):
        super().__init__()
        self.weight = 6
        self.type = Is_DID
        self.is_did = True

    def define_node(self, node_dict):
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
        text = super().print()
        # There is a lot of type validation here since dids can be merges and that can cause issues
        if type(self.get_number()) == str:
            text += f"\nNumber: {self.get_number()}\n"    
        if self.forward_destinations and type(self.forward_destinations) == dict:
            for key in self.forward_destinations.keys():
                internal_ext = ": None"
                ext_name = ''
                destination = self.forward_destinations.get(key)
                internal = None
                if type(destination) == dict:
                    internal = destination.get("Internal")
                if type(internal) == list and len(internal) > 0:
                    internal_ext = internal[0]
                    for child in self.get_children():
                        if child.get_number() == internal_ext:
                            ext_name = child.get_name()
                            if ext_name == internal_ext:
                                internal_ext = ''    
                            else:
                                internal_ext = "(" + internal_ext + ")"
                            ext_name = ": " + ext_name    
                            break
                    internal_ext = " " + internal_ext
                entry = f"\n{key}{ext_name}{internal_ext}"
                text += entry
        if self.conditions and type(self.conditions) == dict:
            text += "\n\nConditions"
            for key in self.conditions.keys():
                if condition := self.conditions.get(key):
                    condition = ": " + condition
                else:
                    condition = ''
                entry = f"\n\t{key}{condition}"
                text += entry
        return text