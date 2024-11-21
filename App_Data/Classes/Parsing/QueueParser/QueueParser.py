from ..ParentParser.Parser import Parser, re
from ....Keys import Name, Number
from ....Keys import Queue

class QueueParser(Parser):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def get_members(self, data:str):
        """Takes a single queue or group and finds the members within that list."""
        member_block = self.get_item_tag(data, "Members")
        if not member_block:
            return []
        return self.regex_DN(member_block)

    def get_status(self, data:str):
        """Takes a block of text and returns all instances of queue status after regex"""
        member_block = self.get_item_tag(data, "Members")
        if not member_block:
            return []
        queue_statuses = re.findall(r'QueueStatus="([A-Za-z]+)"', member_block)
        return queue_statuses

    def get_members_with_status(self, data:str):
        """ Gets a list of members, but if the have statuses returns a dict instead of a list"""
        members = self.get_members(data)
        status = self.get_status(data)
        if len(members) == len(status):
            members_dict = {}
            for i, member in enumerate(members):
                member_dict = {
                    Number : member,
                    "Status" : status[i]
                    }
                members_dict[member] = member_dict
            return members_dict
        else:
            return members

    def get_queue_managers(self, data:str):
        """ Takes a single queue and fines the managers within that list."""
        manager_block = self.get_item_tag(data, "QueueManagers")
        if not manager_block:
            return []
        return self.regex_DN(manager_block)

    def get_destination(self, data:str):
        """Takes a call item block and gets that call items desitations."""
        destination_block = self.get_item_tag(data, "Destination")
        if not destination_block:
            return []
        to_tag = self.get_item_tag(destination_block, "To")
        if to_tag == "External":
            external_tag = self.get_item_tag(destination_block, "External")
            if external_tag:
                return [external_tag]
        return self.regex_DN(destination_block)

    def get_polling_strategy(self, data:str):
        polling_strategy = self.get_item_tag(data, "PollingStrategy")
        polling_strat = "".join([" " + c if c.isupper() else c for c in polling_strategy])
        print(polling_strat)
        return polling_strat

    def get_ring_time(self, data:str):
        ring_time = self.get_item_tag(data, "MasterTimeout")
        return ring_time

    def get_full_queues(self, data:str):
        """
        Gets and parses all ring group info into a dictionary to define class objects
        """
        queue_blocks = self.get_tag_instances_as_list(data, Queue)
        queue_dicts = {}
        for q_block in queue_blocks:
            number = self.get_item_number(q_block)
            name = self.get_item_name(q_block)
            destination = self.get_destination(q_block)
            members = self.get_members_with_status(q_block)
            managers = self.get_queue_managers(q_block)
            polling_strategy = self.get_polling_strategy(q_block)
            ring_time = self.get_ring_time(q_block)
            q_dict = {
                Name : name,
                Number : number,
                "Destination" :destination,
                "Members" : members,
                "Managers" : managers,
                "Strategy" : polling_strategy,
                "Ring Time" : ring_time
            }
            queue_dicts[number] = q_dict
        self.print_json(queue_dicts, Queue)
        return queue_dicts
       
    def get_queue_dict(self, data:str):
        if not data:
            return None
        
        queue_dict = self.get_full_queues(data)

        return queue_dict