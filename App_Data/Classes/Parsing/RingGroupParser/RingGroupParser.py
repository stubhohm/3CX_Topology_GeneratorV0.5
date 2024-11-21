from ..ParentParser.Parser import Parser
from ....Keys import Name, Number
from ....Keys import RingGroup

class RingGroupParser(Parser):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def get_members(self, data:str):
        """Takes a single queue or group and finds the members within that list."""
        member_block = self.get_item_tag(data, "Members")
        if not member_block:
            return []
        return self.regex_DN(member_block)

    def get_destination_block(self, data:str):
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

    def get_destinations(self, line_data:str):
        destination = self.get_destination_block(line_data)
        if type(destination) == list:
            if len(destination) == 0:
                return {}
            destination = destination[0]
        main_dest = self.get_item_tag(line_data, "OfficeHoursRoute")
        ooo_dest = self.get_item_tag(line_data, "OutOfOfficeHoursRoute")
        hol_dest = self.get_item_tag(line_data, "HolidaysRoute")         
        destinations = {"Office Hours Destination" : main_dest, 
                        "Out of Office Hours Destination": ooo_dest,
                        "Holiday Destination": hol_dest}
        for key in destinations.keys():
            if not destinations.get(key):
                destinations[key] = destination
                continue
            if "ProceedWithNoExceptions" in destinations.get(key):
                destinations[key] = destination
            dest = destinations.get(key)
            destinations[key] = ''.join(c for c in str(dest) if c.isdigit())
        return destinations

    def get_full_ringgroups(self, data:str):
        """
        Gets and parses all ring group info into a dictionary to define class objects
        """
        ringgroup_blocks = self.get_tag_instances_as_list(data, RingGroup)
        ringgroup_dicts = {}
        for rg_block in ringgroup_blocks:
            number = self.get_item_number(rg_block)
            name = self.get_item_name(rg_block)
            #destination = self.get_destination(rg_block)
            destination = self.get_destinations(rg_block)
            ring_strategy = self.get_item_tag(rg_block, "RingStrategy")
            members = self.get_members(rg_block)
            rg_dict = {
                Name : name,
                Number : number,
                "RingStrategy" : ring_strategy,
                "Destination" : destination,
                "Members" : members
            }
            ringgroup_dicts[number] = rg_dict
        self.print_json(ringgroup_dicts, RingGroup)
        return ringgroup_dicts

    def get_ringgroup_dict(self, data:str):
        if not data:
            return None
        
        ring_dict = self.get_full_ringgroups(data)

        return ring_dict