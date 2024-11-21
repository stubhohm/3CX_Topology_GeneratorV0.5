from ...Modules import os, re, glob, json
from ...Keys import Forwards_To, Name, Number, Result, Is_DID, Type
from ...Keys import IVR, Queue, RingGroup, User, Make_Jsons

class Parser():
    def __init__(self, config_dict:dict):
        self.input_path:str = os.path.join("App_Data", "Input", "*.xml")
        self.testing_path:str = os.path.join("App_Data", "Input", "ExampleInput.json")
        self.make_json = config_dict.get(Make_Jsons)

    def open_file(self, path:str):
        """ Opens XML file from the Input directory."""
        xml_files = glob.glob(path)
        if xml_files:
            xml_file = xml_files[0]
        else:
            print(f"File not Found: {path}")
            return None
        try:
            with open(xml_file, "rb") as file:
                text = file.read()
                string_text = text.decode("utf-8")
            return string_text
        except FileNotFoundError:
            print(f"Not able to find file with given path: {path}")
            return None

    def print_json(self, dictionary:dict, file_name):
        if not self.make_json:
            return
        output_path = os.path.join("App_Data", "Output", f"{file_name}.json")
        with open(output_path, "w") as file:
            json.dump(dictionary, file, indent=4)

    def regex_DN(self, data:str):
        """performs a regex search and returns all numbers in the pattern as an array."""
        pattern = r'DN="(\d+)"'
        items = re.findall(pattern, data)
        return items

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
        return self.regex_DN(destination_block)

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
            return []
        forwards = self.get_tag_instances_as_list(forwards_block, "IVRForward")
        if not forwards:
            return {}
        forward_dict = {}
        for forward in forwards:
            ext = self.get_item_tag(forward,"ForwardDN")
            dial_num = self.get_item_number(forward)
            type = self.get_item_tag(forward, "ForwardType")
            forward_dict[ext] = {
                "Extension" : ext,
                "Dial Number" : dial_num,
                "Forward Type" : type}
        return forward_dict

    def get_IVR_forwards(self, data:str):
        """Takes an IVR and finds the forward destinations of that IVR."""
        forwards_block = self.get_item_tag(data, "Forwards")
        if not forwards_block:
            return []
        forwards = self.get_tag_instances_as_list(forwards_block, "IVRForward")
        if not forwards:
            return {}
        forwards_list = []
        for forward in forwards:
            ext = self.get_item_tag(forward,"ForwardDN")
            forwards_list.append(ext)
        return forwards_list

    def get_item_tag(self, data:str, tag:str):
        """Returns the string bound inside the first instance of a tag in a data string."""
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start_pos = data.find(start_tag)
        
        if start_pos == -1:
            return None
        
        start_pos += len(start_tag)

        end_pos = data.find(end_tag, start_pos)

        if end_pos == -1:
            return None
        return data[start_pos:end_pos].strip()

    def get_item_name(self, data:str):
        """Takes a data string and returns the first item inside the Name tag field."""
        return self.get_item_tag(data, "Name")
    
    def get_item_number(self, data:str):
        """Takes a data string and returns the first item inside the Number tag field."""
        return self.get_item_tag(data, "Number")

    def get_tag_instances_as_list(self, data:str, tag:str):
        """ Returns a list of all items with a given tag appear in a data string."""
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start_pos = 0
        results:list[str] = []

        while True:
            start_pos = data.find(start_tag, start_pos)
            if start_pos == -1:
                break

            start_pos += len(start_tag)
            end_pos = data.find(end_tag, start_pos)
            if end_pos == -1:
                break
            results.append(data[start_pos:end_pos].strip())

            start_pos = end_pos + len(end_tag)
        return results

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
    
    def get_dids(self, data:str):
        tag = "ExternalLineRule"
        results = self.get_tag_instances_as_list(data, tag)
        dictionary, main_did = self.initial_did_parse(results)
        did_dict = {}
        for value in dictionary.values():
            destinations = self.get_office_destination(value[Result])
            temp_dict = {Name: "DID: " + value[Name],
                         Number: value[Number],
                         Forwards_To: destinations,
                         Type: Is_DID}
            did_dict[value[Name]] = temp_dict
        return did_dict

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
                in_bound_rules[number] = did_dict
            external_lines_dict[external_number] = in_bound_rules
        self.print_json(external_lines_dict, Is_DID)
        return external_lines_dict

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
            ivr_item = { Name: name,
                        Number : number,
                        "Timeout Type" : timeout_type,
                        "Timeout DN" : timeout_dn,
                        "Forwards" : forwards
                        }
            ivr_dicts[number] = ivr_item
        
        self.print_json(ivr_dicts, IVR)
        return ivr_dicts
    
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
            q_dict = {
                Name : name,
                Number : number,
                "Destination" :destination,
                "Members" : members,
                "Managers" : managers
            }
            queue_dicts[number] = q_dict
        self.print_json(queue_dicts, Queue)
        return queue_dicts

    def get_full_ringgroups(self, data:str):
        """
        Gets and parses all ring group info into a dictionary to define class objects
        """
        ringgroup_blocks = self.get_tag_instances_as_list(data, RingGroup)
        ringgroup_dicts = {}
        for rg_block in ringgroup_blocks:
            number = self.get_item_number(rg_block)
            name = self.get_item_name(rg_block)
            destination = self.get_destination(rg_block)
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

    def get_full_user_ext(self, data:str):
        user_extensions = self.get_tag_instances_as_list(data, "Extension")
        print(len(user_extensions))
        users_dict = {}
        for user in user_extensions:
            first = self.get_item_tag(user, "FirstName")
            last = self.get_item_tag(user, "LastName")
            vm_pin = self.get_item_tag(user, "VMPIN")
            number = self.get_item_number(user)
            current_status = self.get_item_tag(user, "CurrentProfile")
            user_dict = {
                "First" : first,
                "Last" : last,
                "Number" : number,
                "Current Status" : current_status,
                "VM PIN" : vm_pin
            }
            users_dict[number] = user_dict
        
        self.print_json(users_dict, User)
        return users_dict   

    def get_dict_from_backup(self, testing = False):
        if testing:
            backup_path = self.testing_path
        else:
            backup_path = self.input_path 
        data = self.open_file(backup_path)
        if not data:
            return None

        full_ring_dict = self.get_full_ringgroups(data)
        full_queue_dict = self.get_full_queues(data)
        full_ivrs_dict = self.get_full_IRVs(data)
        full_did_dict = self.get_full_dids(data)
        full_user_extensions = self.get_full_user_ext(data)


        full_parsed_dicts = {
            IVR : full_ivrs_dict,
            Is_DID : full_did_dict,
            Queue : full_queue_dict,
            RingGroup : full_ring_dict,
            User : full_user_extensions
        }

        return full_parsed_dicts