from App_Data.Keys import User, Unlinked_DIDs, Merge_DIDs, Dark_Mode, Display_Format, Make_Jsons, Scrub_Auth_IDs, Client, Link_Holiday

show_end_users = True
show_unlinked_dids = True
merge_dids_that_share_a_child = False
display_in_dark_mode = True
show_radial_format = True
make_jsons = True
scrub_auth_ids = False
link_holiday = True
client_name = "none"

config_dict = {Client :client_name,
               User: show_end_users,
               Unlinked_DIDs: show_unlinked_dids,
               Merge_DIDs: merge_dids_that_share_a_child,
               Dark_Mode: display_in_dark_mode,
               Display_Format: show_radial_format,
               Make_Jsons : make_jsons,
               Scrub_Auth_IDs : scrub_auth_ids,
               Link_Holiday : link_holiday
            }