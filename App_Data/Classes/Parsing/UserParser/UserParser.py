from ..ParentParser.Parser import Parser
from ....Keys import User

class UserParser(Parser):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def get_full_user_ext(self, data:str):
        user_extensions = self.get_tag_instances_as_list(data, "Extension")
        users_dict = {}
        for user in user_extensions:
            first = self.get_item_tag(user, "FirstName")
            last = self.get_item_tag(user, "LastName")
            vm_pin = self.get_item_tag(user, "VMPIN")
            number = self.get_item_number(user)
            current_status = self.get_item_tag(user, "CurrentProfile")
            phone_mac = self.get_item_tag(user,"MAC")
            phone_model = self.get_item_tag(user, "ProvisioningFilename2")
            phone_pw = ""
            properties = self.get_tag_instances_as_list(user, "DNProperty")
            for property in properties:
                if "Deskphone password" == self.get_item_tag(property, "Description"):
                    phone_pw = self.get_item_tag(property,"Value")
                    break
            user_dict = {
                "First" : first,
                "Last" : last,
                "Number" : number,
                "Current Status" : current_status,
                "VM PIN" : vm_pin,
                "Phone Mac" : phone_mac,
                "Phone Model" : phone_model,
                "Phone Web Password" : phone_pw
            }
            users_dict[number] = user_dict
        
        self.print_json(users_dict, User)
        return users_dict   
   
    def get_user_dict(self, data:str):
        if not data:
            return None

        user_dict = self.get_full_user_ext(data)

        return user_dict