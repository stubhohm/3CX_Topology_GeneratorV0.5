class DataType():
    def __init__(self) -> None:
        self.data_type = "Undefined DataType"

    def is_int(self, test_int):
        """
        Returns True if test_input is of type float if not, returns False. 
        \nMainly used for input validation.
        """
        if type(test_int) != int:
            return False
        else:
           return True
    
    def is_float(self, test_input):
        """
        Returns True if test_input is of type float if not, returns False. 
        \nMainly used for input validation.
        """
        if type(test_input) != (float):
            return False
        else:
            return True
    
    def is_int_or_float(self, test_input):
        """
        Returns True if test_input is of type float or int if not, returns False.  
        \nMainly used for input validation.
        """
        if self.is_int(test_input) or self.is_float(test_input):
            return True
        else:
            return False

    def is_bool(self, test_state):
        """
        Returns True if test_input is of type bool if not, returns False. 
        \nMainly used for input validation.
        """
        if type(test_state) != bool:
            return False
        return True

    def is_string(self, test_input):
        """
        Returns True if test_input is of type str if not, returns False. 
        \nMainly used for input validation.
        """
        if type(test_input) != str:
            return False
        return True

    def type(self):
        return self.data_type
    
    def set_type(self, type:str):
        if not self.is_string(type):
            return
        self.data_type = type