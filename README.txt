+++++++++++++Setup+++++++++++

Create A a virtual python environment in python version 3.12
    To do so run the command "python -m venv "desired name of your venv""
    Then run the command to activate it. "your venv name"\Scripts\activate
    your terminal should now show you are in a venv

Script currently has no external dependencies.

Run python main.py



---------Usage-----------
Sign into the 3cx admin portal for the account you would like to map. 
Download the most recent backup of the system that is in the state you would like to map.
Unzip the backup and put the .xml file into the "Input" directory.
In the Main.py toggle on or off via True/False if you would like to see end user numbers listed or not.
Run the script.

Nodes can be dragged and moved about for formatting purposes.

Interactions:
- Left clicking allows you to drag a selected node.
- Right clicking will highlight that node and all the children
    it can reach via the directed graph.

While clicking and holding a node with either L or R Click
    - "j" or scrolling down pulls direct children to the parent
    - "k" or scrolling up pushes direct children from the parent
    - "l" will lock the node to prevent pushing or pulling
        but it can still be dragged manually


While only left clicking and holding a node
    - "i" will print an info dump to terminal depnding on the node
    - This feature will be added as a popup in the main GUI


NOTE:
Any .xml you put in the Input folder or Input/old is ignored via gitignore.
This is both as a general security measure to prevent 3CX backup data from being
on github as well as to keep that folder from getting cluttered.