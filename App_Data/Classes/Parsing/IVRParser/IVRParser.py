from ..ParentParser.Parser import Parser, re
from ....Keys import Name, Number
from ....Keys import IVR

class IVRParser(Parser):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def get_ivr_number(self, data:str):
        """Removes the forward block to get the IVRs Extension."""
        number = self.get_tag_instances_as_list(data, Number)
        return number[-1]

    def get_office_destination(self, data:str):
        """Takes an IVR and finds the forward destinations of that IVR."""
        fwd_destinations = self.get_item_tag(data, "ForwardDestinations")
        pattern = r'DN="(\d+)"'
        if not fwd_destinations:
            return []
        destinations = re.findall(pattern, fwd_destinations)
        return destinations      

    def get_full_IVR_forwards(self, data:str):
        """Takes an IVR and finds the forward destinations of that IVR."""
        forwards_block = self.get_item_tag(data, "Forwards")
        if not forwards_block:
            return {}
        forwards = self.get_tag_instances_as_list(forwards_block, "IVRForward")
        if not forwards:
            return {}
        forward_dict = {}
        for forward in forwards:
            ext = self.get_item_tag(forward,"ForwardDN")
            dial_num = self.get_item_number(forward)
            type = self.get_item_tag(forward, "ForwardType")
            forward_dict[dial_num] = {
                "Extension" : ext,
                "Dial Number" : dial_num,
                "Forward Type" : type}
        return forward_dict

    def get_full_IRVs(self, data:str):
        """
        Gets and parses all IVR info into a dictionary to define class object.
        """
        ivr_blocks = self.get_tag_instances_as_list(data, IVR)
        ivr_dicts = {}
        for ivr_data in ivr_blocks:
            number = self.get_ivr_number(ivr_data)
            name = self.get_item_name(ivr_data)
            timeout_type = self.get_item_tag(ivr_data, "TimeoutForwardType")
            timeout_dn = self.get_item_tag(ivr_data, "TimeoutForwardDN")
            forwards = self.get_full_IVR_forwards(ivr_data)
            after_hours = self.get_outside_hours_destination(ivr_data)
            ivr_item = { Name: name,
                        Number : number,
                        "Timeout Type" : timeout_type,
                        "Timeout DN" : timeout_dn,
                        "Forwards" : forwards,
                        "After Hours" : after_hours
                        }
            ivr_dicts[number] = ivr_item
        
        self.print_json(ivr_dicts, IVR)
        return ivr_dicts
          
    def get_IVR_dict(self, data:str):
        if not data:
            return {}
        
        ivrs_dict = self.get_full_IRVs(data)

        return ivrs_dict