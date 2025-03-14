from ..Nodes.Nodes import Node, IVRObj, RingGroupObj, QueueObj, DIDObj, UserObj
from ...Keys import Name, Number, Forwards_To, Is_DID, Type, Link_Holiday
from ...Keys import Root, Island, User, Merge_DIDs, IVR, Queue, RingGroup



class TreeBuilder():
    def __init__(self, config_dict:dict):
        self.nodes:dict[str, Node] = {}
        self.unlinked_parents:dict[str, Node] = {}
        self.root:Node = Node()
        self.root.set_name(Root)
        self.root.type = Root
        self.island:Node = Node()
        self.island.set_name(Island)
        self.island.type = Island
        self.merge_dids = config_dict.get(Merge_DIDs)
        self.show_users = config_dict.get(User)
        self.link_holiday = config_dict.get(Link_Holiday)

    def get_node_by_name(self, node_name:str):
        if node_name in self.nodes.keys():
            return self.nodes.get(node_name)
        else:
            return None

    def get_node_names(self):
        node_names = []
        for node in self.nodes.keys():
            node_names.append(node)
        return node_names

    def complete_addition(self):
        """Links all Nodes to either Root or Island and adds terminating children, Usually user numbers."""        
        for node_name in list(self.nodes.keys()):
            # If Node is unparented add it to islands children
            if not self.nodes.get(node_name).parented:
                self.island.add_child(self.nodes[node_name])

            new_nodes = self.nodes.get(node_name).get_children_names()
            # Last round robin check for linkages
            for node in new_nodes:
                if not node:
                    continue
                if node in self.get_node_names():
                    continue
                node_dict = {Name: node,
                            Number: node,
                            Type: User}
                
                self.add_object(self.define_new_node(node_dict))

            if self.root.is_parent(node_name):
                continue
            if self.island.is_parent(node_name):
                continue
            self.island.add_child(self.nodes.get(node_name))

        self.nodes[self.root.get_name()] = self.root
        self.nodes[self.island.get_name()] = self.island

    def merge_similar_dids(self):
        unique_DID_children = []
        root_node = self.get_node_by_name(Root)
        new_root = Node()
        new_root.set_name(Root)
        new_root.type = Root
        for child in root_node.get_children():

            if self.nodes.get(child.get_name()):
                del self.nodes[child.get_name()]
            DID_children = child.get_children()
            
            user = False
            for child in DID_children:
                if child.type == User and not self.show_users:
                    user = True
            if user:continue

            if DID_children not in unique_DID_children:
                unique_DID_children.append(DID_children)

        for DID_children in unique_DID_children:
            merged_did = DIDObj()
            names = [child.get_name() for child in DID_children]
            destinations = {}
            for i, name in enumerate(names):
                child = DID_children[i]
                destinations[f"Merged Destination {i + 1}"] = { "To" : child.type,
                                                        "Internal" : [child.get_number()]}
                
            name = f"Merged DIDs for: {", ".join(names)}"
            number = len(unique_DID_children)
            merged_did_dict = {Name : name,
                               Number: number,
                               "Forward Destinations": destinations,
                               "Conditions" : {"Conditions may vary for merged DIDs." : None,
                                               "DIDs typically handle holiday routing if not allocated elsewhere.": None}
            }
            merged_did.define_node(merged_did_dict)
            for children in DID_children:
                merged_did.add_child(children)
                self.nodes[merged_did.get_name()] = merged_did
                new_root.add_child(merged_did)
            
        self.nodes[Root] = new_root

    def check_if_child_of_existing_node(self, new_node:Node):
        # See if node is a child of an existing node
        name = new_node.get_name()
        node_number = new_node.get_number()
        for node in self.nodes.values():
            if not node:
                continue
            if name in node.get_unmapped_children() or node_number in node.get_unmapped_children():
                node.add_child(new_node)

    def check_if_parent_of_existing_node(self, new_node:Node):
        # See if node is a parent of an existing node
        for forward_to in list(new_node.get_unmapped_children()):
            if not forward_to:
                continue
            for node in self.nodes.values():
                if forward_to == node.get_name() or forward_to == node.get_number():
                    new_node.add_child(node)

    def clean_up_node_lists(self, new_node:Node):
        # If the new node was never parented, add it to the unlinked parents
        if not new_node.parented:
            self.unlinked_parents[new_node.get_name()] = new_node

        # Removed Freshly Linked Parents
        for node in list(self.unlinked_parents.values()):
            if not node:
                continue
            if node.parented:
                del self.unlinked_parents[node.get_name()]

    def define_new_node(self, node_dict:dict):
        """Takes a node dict and returns an instanced node."""
        new_node = Node()
        new_node.set_name(node_dict.get(Name))
        new_node.set_number(node_dict.get(Number))
        new_node.set_forward_to_extensions(node_dict.get(Forwards_To, []))
        new_node.type = node_dict.get(Type)
        return new_node

    def add_object(self, new_node:Node):
        """Addes a new node to the tree given a node dictionary."""
        name = new_node.get_name()
        self.nodes[name] = new_node
        if new_node.type == Is_DID:
            self.root.add_child(new_node)

        self.check_if_child_of_existing_node(new_node)
        self.check_if_parent_of_existing_node(new_node)

        self.nodes[new_node.get_name()] = new_node

        self.clean_up_node_lists(new_node)

    def add_node_object(self, node_obj, node_dict:dict[str, dict]):
        for value in node_dict.values():
            node = node_obj()
            if not isinstance(node, Node):
                continue
            if self.nodes.get(value.get(Name)):
                if type(node) == UserObj:
                    node.define_name(value)
                    value[Name] = node.get_name()
                if not node.type:
                    print(node.get_name())
                    print(node.get_number())
                name = str(value.get(Name)) + node.type
                value[Name] = name
            node.define_node(value)
            self.add_object(node)

    def set_weights(self):
        self.nodes.get(Root).weight = 10
        self.nodes.get(Island).weight = 10

    def full_parsing(self, group_dicts:dict):
        for key in group_dicts.keys():
            node_object = None
            if key == Is_DID:
                node_object = DIDObj
                for value in group_dicts.get(Is_DID).values():
                    self.add_node_object(node_object, value)
                continue
            elif key == IVR:
                node_object = IVRObj
            elif key == Queue:
                node_object = QueueObj
            elif key == RingGroup:
                node_object = RingGroupObj
            elif key == User:
                node_object = UserObj
            if node_object:
                node_dictionarys = group_dicts.get(key)
                self.add_node_object(node_object, node_dictionarys)
        self.complete_addition()
        if self.merge_dids:
            self.merge_similar_dids()
        return self
        
    def print(self):
        """debugging"""
        tree_text = "\nroot"
        text = self.root.print()
        tree_text += text
        tree_text += "\nIslands"
        text = self.island.print()
        tree_text += text
        return tree_text

