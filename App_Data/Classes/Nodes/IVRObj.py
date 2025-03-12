from .Node import Node
from ...Keys import IVR, Name, Number

class IVRObj(Node):
    def __init__(self):
        super().__init__()
        self.type = IVR

    def define_node(self, node_dict):
        self.type = IVR
        self.weight = 6
        self.set_name(node_dict.get(Name))
        self.set_number(node_dict.get(Number))
        self.timeout_type:str = node_dict.get("Timeout Type")
        self.timeout_destination:str = node_dict.get("Timeout DN")
        self.forwards:dict[str, dict] = node_dict.get("Forwards")
        ring_locations = []
        if type(self.forwards) == dict:
            for value in self.forwards.values():
                if type(value) != dict:
                    continue
                if ext := value.get("Extension"):
                    ring_locations.append(ext)
        if type(self.timeout_destination) == str:
            ring_locations.append(self.timeout_destination)
        super().define_node(node_dict)
        ring_locations.append(self.after_hours_extension)     
        self.set_forward_to_extensions(ring_locations)


    def print(self):
        text = super().print()

        name = ''
        for child in self.get_children():
            if self.timeout_destination == child.get_number():
                name = child.get_name()
                name = f" - {name}"
        if self.timeout_destination:
            timeout = f" ({self.timeout_destination})"
        else: timeout = ""
        text += f"\nTimeout: {self.timeout_type}{name}{timeout}\n"

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
        
        for key in sorted(fwd_dict.keys(), key=int):
            text += f"\n{fwd_dict[key]}"
        return text