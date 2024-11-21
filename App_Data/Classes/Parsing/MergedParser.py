from .ParentParser.Parser import Parser
from .DIDParser.DIDParser import DIDParser
from .UserParser.UserParser import UserParser
from .IVRParser.IVRParser import IVRParser
from .QueueParser.QueueParser import QueueParser
from .RingGroupParser.RingGroupParser import RingGroupParser
from ...Keys import User, Is_DID, IVR, Queue, RingGroup

class MergedParser():
    def __init__(self, config_dict:dict):
        self.parser = Parser(config_dict)
        self.did = DIDParser(config_dict)
        self.ivr = IVRParser(config_dict)
        self.queue = QueueParser(config_dict)
        self.ringgroup = RingGroupParser(config_dict)
        self.user = UserParser(config_dict)
        

    def parse_xml(self):
        xml_data = self.parser.get_data_from_backup()
        if not xml_data:
            return None
        ivr_dict = self.ivr.get_IVR_dict(xml_data)
        did_dict = self.did.get_DID_dict(xml_data)
        queue_dict = self.queue.get_queue_dict(xml_data)
        ringgroup_dict = self.ringgroup.get_ringgroup_dict(xml_data)
        user_dict = self.user.get_user_dict(xml_data)

        full_dicts = {
            IVR : ivr_dict,
            Is_DID : did_dict,
            Queue : queue_dict,
            RingGroup : ringgroup_dict,
            User : user_dict
        }

        return full_dicts
