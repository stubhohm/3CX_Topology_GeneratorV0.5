from ....Modules import os, re, glob, json, shutil, filedialog, time
from ....Keys import Client
from ....Keys import Make_Jsons, Scrub_Auth_IDs

class Parser():
    def __init__(self, config_dict:dict):
        self.root_path:str = os.path.abspath(__file__).replace(os.path.join("App_Data","Classes", "Parsing", "ParentParser","Parser.py"), "")
        self.input_path:str = os.path.join(self.root_path, "App_Data", "Input", "*.xml")
        self.testing_path:str = os.path.join(self.root_path,"App_Data", "Input", "ExampleInput.json")
        self.make_json = config_dict.get(Make_Jsons)
        self.scrub_credentials = config_dict.get(Scrub_Auth_IDs)
        self.client_name = config_dict.get(Client)

    def select_with_tk(self):
        file_path = filedialog.askopenfilename().replace("/", "\\")
        print(file_path)
        return file_path

    def open_file(self, path:str):
        """ Opens XML file from the Input directory."""
        xml_files = glob.glob(path)
        if xml_files:
            xml_file = xml_files[0]
        else:
            print(f"File not Found via path: {path}")
            xml_file = self.select_with_tk()
            if not xml_file:
                return None
        try:
            with open(xml_file, "rb") as file:
                text = file.read()
                string_text = text.decode("utf-8")
            if self.scrub_credentials and "scrubbed" not in xml_file:
                new_path = path.replace("*.xml", "")
                destination = os.path.join(new_path, "old")
                shutil.move(xml_file, destination)
            else: self.scrub_credentials = False
            return string_text
        except FileNotFoundError:
            print(f"Not able to find file with given path: {path}")
            time.sleep(10)
            return None

    def write_xml(self, data_string:str):
        output_path = os.path.join(self.root_path, "App_Data", "Input", f"{self.client_name}_scrubbed.xml")
        with open(output_path, "wb") as file:
            encoded_data = data_string.encode("utf-8")
            file.write(encoded_data)

    def print_json(self, dictionary:dict, file_name):
        if not self.make_json:
            return
        output_path = os.path.join(self.root_path, "App_Data", "Output", f"{file_name}.json")
        with open(output_path, "w") as file:
            json.dump(dictionary, file, indent=4)

    def regex_DN(self, data:str):
        """performs a regex search and returns all numbers in the pattern as an array."""
        pattern = r'DN="(.*?)"'
        items = re.findall(pattern, data)
        return items

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

    def scrub_credentials_from_data(self, data:str):
        if not self.scrub_credentials:
            return data
        authids = self.get_tag_instances_as_list(data, "AuthID")
        authpw = self.get_tag_instances_as_list(data, "AuthPassword")
        print(f"Scrubbing out {len(authids)} user IDs.")
        for id in authids:
            data = data.replace(id, "")
        print(f"Scrubbing out {len(authpw)} user passwords.")
        for pw in authpw:
            data = data.replace(pw, "")
        self.write_xml(data)
        return data

    def get_outside_hours_destination(self, data:str):
        """Takes an Node and finds the after hours forward destinations of that IVR."""
        fwd_destinations = self.get_item_tag(data, "OutOfOfficeHoursRoute")
        pattern = r'(\d+)'
        if not fwd_destinations:
            return "Proceed Without Exception"
        destinations = re.findall(pattern, fwd_destinations)
        if len(destinations) > 0:
            destination = destinations[0]
        else: destination = "Proceed Without Exception"
        return destination 

    def get_data_from_backup(self, testing = False):
        if testing:
            backup_path = self.testing_path
        else:
            backup_path = self.input_path 
        data = self.open_file(backup_path)
        if not data:
            return None

        scrubbed_data = self.scrub_credentials_from_data(data)

        return scrubbed_data