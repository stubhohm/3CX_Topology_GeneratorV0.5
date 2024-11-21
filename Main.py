from App_Data.Classes.Constructor.TreeBuilder import TreeBuilder
from App_Data.Classes.Parsing.Parser import Parser
from App_Data.Classes.Drawing.Drawing import Renderer
from App_Data.Keys import User, Unlinked_DIDs, Merge_DIDs, Dark_Mode, Display_Format, Make_Jsons
from App_Data.Modules import start_time, total_time


show_end_users = False
show_unlinked_dids = True
merge_dids_that_share_a_child = True
display_in_dark_mode = True
show_radial_format = True
make_jsons = True
client_name = "Advent Home Medical"

config_dict = {User: show_end_users,
               Unlinked_DIDs: show_unlinked_dids,
               Merge_DIDs: merge_dids_that_share_a_child,
               Dark_Mode: display_in_dark_mode,
               Display_Format: show_radial_format,
               Make_Jsons : make_jsons
            }
def main():
    ThreeCX_dict = Parser(config_dict).get_dict_from_backup()
    if not ThreeCX_dict:
        print("Parsing was unsuccesful.\nCheck and ensure you have a 3CX XML file in the 'Input' directory.")
        return
    tree = TreeBuilder(config_dict).full_parsing(ThreeCX_dict)
    renderer = Renderer(client_name, tree, config_dict)
    renderer.root.mainloop()

main()