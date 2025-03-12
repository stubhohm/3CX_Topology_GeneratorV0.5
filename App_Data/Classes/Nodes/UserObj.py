from .Node import Node
from ...Keys import User, Number

class UserObj(Node):
    def __init__(self):
        super().__init__()
        self.type = User
        self.weight = 1

    def define_name(self, node_dict:dict):
        self.first = node_dict.get("First")
        if type(self.first) == str:
            self.first = self.first.capitalize()
        self.last = node_dict.get("Last")
        if type(self.last) == str:
            self.last = self.last.capitalize()
        if self.first and self.last:
            name = self.first + " " + self.last
        else: name = self.first
        self.set_name(name)

    def define_node(self, node_dict):
        self.weight = 1
        self.type = User
        self.define_name(node_dict)
        self.set_number(node_dict.get(Number))
        self.status = node_dict.get("Current Status")
        self.vm_pin = node_dict.get("VM PIN")
        super().define_node(node_dict)

    def print(self):
        text = super().print()
        text += f"\nUser Status: {self.status}"
        text += "\n\n"
        return text