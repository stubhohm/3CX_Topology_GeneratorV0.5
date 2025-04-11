from App_Data.Classes.Constructor.TreeBuilder import TreeBuilder
from App_Data.Classes.Parsing.MergedParser import MergedParser
from App_Data.Classes.Drawing.Drawing import Renderer
from App_Data.Keys import Client
from App_Data.ConfigDict import config_dict
import time

def main():
    ThreeCX_dict = MergedParser(config_dict).parse_xml()
    print("Finished Parse")
    if not ThreeCX_dict:
        print("Parsing was unsuccesful.\nCheck and ensure you have a 3CX XML file in the 'Input' directory.")
        return
    tree = TreeBuilder(config_dict).full_parsing(ThreeCX_dict)
    print("Tree Built")
    renderer = Renderer(tree, config_dict)
    print("Render Populated")
    renderer.root.mainloop()
    print("Rendering Data")
main()