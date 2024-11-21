from ..ParentParser.Parser import Parser, re
from ....Keys import Forwards_To, Name, Number, Result, Is_DID, Type, Client
from ....Keys import IVR, Queue, RingGroup, User, Make_Jsons, Scrub_Auth_IDs

class DIDParser(Parser):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def get_did_conditions(self, line_data:str):
        """ Gets a DIDs conditions"""
        condition_block = self.get_item_tag(line_data, "Conditions")
        matches = re.findall(r'="([^"]+)"', condition_block)
        dictionary = {}
        if len(matches) == 3:
            dictionary = {"Call Type" : matches[0],
                          "Condition" : matches[1],
                          "Hours" : matches[2]}
        return dictionary

    def get_did_destinations(self, line_data:str):
        """ Gets the DIDs destinations during various times of business"""
        forward_destinations = self.get_item_tag(line_data, "ForwardDestinations")
        dest = self.get_item_tag(forward_destinations, "OfficeHoursDestination")
        office_hours = {"To" : self.get_item_tag(dest, "To"),
                        "Internal" : self.regex_DN(dest),
                        "External" : self.get_item_tag(dest, "External"),
                        }
        dest = self.get_item_tag(forward_destinations, "OutOfOfficeHoursDestination")        
        out_of_office = {"To" : self.get_item_tag(dest, "To"),
                        "Internal" : self.regex_DN(dest),
                        "External" : self.get_item_tag(dest, "External"),
                        }        
        dest = self.get_item_tag(forward_destinations, "HolidaysDestination") 
        holiday = {"To" : self.get_item_tag(dest, "To"),
                        "Internal" : self.regex_DN(dest),
                        "External" : self.get_item_tag(dest, "External"),
                        }
        destinations = {"Office Hours" : office_hours,
                        "After Hours" : out_of_office,
                        "Holiday" : holiday
        }
        return destinations

    def get_full_dids(self, data:str):
        external_line_blocks = self.get_tag_instances_as_list(data, "ExternalLine")
        external_lines_dict = {}
        for external_line_block in external_line_blocks:
            DIDs = self.get_item_tag(external_line_block, "DIDNumbers")
            if DIDs:
                DIDs = DIDs.split(",")
            else:
                continue
            external_number = self.get_item_tag(external_line_block, "ExternalNumber")
            external_line_rules = self.get_tag_instances_as_list(external_line_block, "ExternalLineRule")
            count_unnamed = 1
            in_bound_rules = {}
            for external_line in external_line_rules:
                name = self.get_item_tag(external_line, "RuleName")
                number = self.get_item_tag(external_line, "Data")
                if number in DIDs: 
                    DIDs.remove(number)
                if not number: number = external_number
                if not name: 
                    name = f"Unnammed DID {count_unnamed}"
                    count_unnamed += 1
                conditions = self.get_did_conditions(external_line)
                destinations = self.get_did_destinations(external_line)
                did_dict = {
                    Name : name,
                    Number : number,
                    "Forward Destinations" : destinations,
                    "Conditions" : conditions
                }
                in_bound_rules[number] = did_dict
            main_destinations = in_bound_rules[external_number].get("Forward Destinations")
            main_conditions = in_bound_rules[external_number].get("Conditions")
            for undefined_did in list(DIDs):
                name = f"Unnammed DID {count_unnamed}"
                count_unnamed += 1
                did_dict = {
                    Name : name,
                    Number : undefined_did,
                    "Forward Destinations" : main_destinations,
                    "Conditions" : main_conditions
                }
                in_bound_rules[undefined_did] = did_dict
            external_lines_dict[external_number] = in_bound_rules
        self.print_json(external_lines_dict, Is_DID)
        return external_lines_dict
      
    def get_DID_dict(self, data:str):
        if not data:
            return None

        did_dict = self.get_full_dids(data)

        return did_dict