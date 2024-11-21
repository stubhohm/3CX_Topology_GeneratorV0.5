from App_Data.Classes.Constructor.TreeBuilder import TreeBuilder
from App_Data.Classes.Parsing.MergedParser import MergedParser
from App_Data.Classes.Drawing.Drawing import Renderer
from App_Data.Keys import Client
from App_Data.ConfigDict import config_dict

def main():
    config_dict[Client] = input("What is the Clients name: ").replace(" ", "_")
    ThreeCX_dict = MergedParser(config_dict).parse_xml()
    if not ThreeCX_dict:
        print("Parsing was unsuccesful.\nCheck and ensure you have a 3CX XML file in the 'Input' directory.")
        return
    tree = TreeBuilder(config_dict).full_parsing(ThreeCX_dict)
    renderer = Renderer(tree, config_dict)
    renderer.root.mainloop()

main()